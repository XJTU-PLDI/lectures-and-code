from dataclasses import dataclass

@dataclass
class Token(object):
    type: str
    text: str

# 简单的遍历一遍构造出所有 token
def tokenize(source_code: str) -> list[Token]:
    tokens: list[Token] = []
    offset = 0
    maxlen = len(source_code)

    # 判断当前是否还有可用字符，判断后才能调用获取，不然会报错的
    def available():
        nonlocal maxlen, offset
        return offset < maxlen

    # 获取当前字符
    def current():
        nonlocal source_code, offset
        return source_code[offset]

    # 前进 n 个字符，默认为 1
    def advance(count: int = 1):
        nonlocal offset
        offset += count

    # 构造一个新词元并加到返回值中
    def add_token(type: str, text: str = ''):
        nonlocal tokens
        tokens.append(Token(type, text))

    # 循环扫描字符直到字符耗尽
    while available():
        char = current()

        # 跳过空白符，不产生词元
        if char.isspace():
            while available() and current().isspace():
                advance()
            continue

        # 跳过注释，不产生词元
        if char == '#':
            while available() and current() != '\n':
                advance()
            continue

        # 先尝试匹配 为固定的字符串 的词元
        match char:
            case ',': advance(); add_token(','); continue
            case ';': advance(); add_token(';'); continue
            case '(': advance(); add_token('('); continue
            case ')': advance(); add_token(')'); continue
            case '{': advance(); add_token('{'); continue
            case '}': advance(); add_token('}'); continue

            case '+': advance(); add_token('+'); continue
            case '-': advance(); add_token('-'); continue
            case '*': advance(); add_token('*'); continue
            case '/': advance(); add_token('/'); continue

            case '=':
                advance()
                if available() and current() == '=':
                    advance()
                    add_token('==')
                else:
                    add_token('=')
                continue
            case '!':
                advance()
                if available() and current() == '=':
                    advance()
                    add_token('!=')
                else:
                    add_token('!')
                continue
            case '<':
                advance()
                if available() and current() == '=':
                    advance()
                    add_token('<=')
                else:
                    add_token('<')
                continue
            case '>':
                advance()
                if available() and current() == '=':
                    advance()
                    add_token('>=')
                else:
                    add_token('>')
                continue
            case _:
                pass # fall through
        
        # 尝试匹配标识符
        if char.isalpha():
            start = offset
            while available() and current().isalnum():
                advance()

            # 关键字要挑出来，防止使用关键字当变量 / 函数名
            match source_code[start:offset]:
                case 'function': add_token('function')
                case 'if': add_token('if')
                case 'else': add_token('else')
                case 'while': add_token('while')
                case 'continue': add_token('continue')
                case 'break': add_token('break')
                case 'return': add_token('return')
                case text: add_token('identifier', text)

        # 尝试匹配数字
        elif char.isdigit():
            start = offset
            while available() and current().isdigit():
                advance()
            
            # 注意小数处理
            if available() and current() == '.':
                advance()
                while available() and current().isdigit():
                    advance()
            
            add_token('number', source_code[start:offset])

        # 都不行，报错
        else:
            raise NotImplementedError(f"Unknown character: {char}")
        
    return tokens

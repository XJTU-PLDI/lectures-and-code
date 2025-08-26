from dataclasses import dataclass

@dataclass
class Token(object):
    type: str
    text: str

# 简单的遍历一遍构造出所有 token
def tokenize(source_code: str):
    tokens: list[Token] = []
    offset = 0
    maxlen = len(source_code)

    def available():
        nonlocal maxlen, offset
        return offset < maxlen

    def current():
        nonlocal source_code, offset
        return source_code[offset]

    def advance(count: int = 1):
        nonlocal offset
        offset += count

    def add_token(type: str, text: str = ''):
        nonlocal tokens
        tokens.append(Token(type, text))

    while available():
        char = current()

        # 跳过空白符
        if char.isspace():
            while available() and current().isspace():
                advance()
            continue

        # 跳过注释
        if char == '#':
            while available() and current() != '\n':
                advance()
            continue

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
        
        if char.isalpha():
            start = offset
            while available() and current().isalnum():
                advance()

            match source_code[start:offset]:
                case 'function': add_token('function')
                case 'if': add_token('if')
                case 'else': add_token('else')
                case 'while': add_token('while')
                case 'continue': add_token('continue')
                case 'break': add_token('break')
                case 'return': add_token('return')
                case text: add_token('identifier', text)

        elif char.isdigit():
            start = offset
            while available() and current().isdigit():
                advance()
            
            # for float numbers
            if available() and current() == '.':
                advance()
                while available() and current().isdigit():
                    advance()
            
            add_token('number', source_code[start:offset])

        else:
            raise NotImplementedError(f"Unknown character: {char}")
        
    return tokens

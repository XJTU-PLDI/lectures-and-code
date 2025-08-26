from dataclasses import dataclass
from tokenizer import Token

class SyntaxTreeNode:
    pass

class StatementNode(SyntaxTreeNode):
    pass

class ExpressionNode(SyntaxTreeNode):
    pass

@dataclass
class ModuleNode(SyntaxTreeNode):
    functions: list['FunctionNode']
    global_vars: list['BinaryExpr']

@dataclass
class FunctionNode(SyntaxTreeNode):
    name: str
    parameters: list[str]
    body: 'BlockStat'

@dataclass
class BlockStat(StatementNode):
    statements: list[StatementNode]

@dataclass
class IfStat(StatementNode):
    condition: ExpressionNode
    branch_true: StatementNode
    branch_false: StatementNode | None = None

@dataclass
class WhileStat(StatementNode):
    condition: ExpressionNode
    body: StatementNode

class ContinueStat(StatementNode):
    pass

class BreakStat(StatementNode):
    pass

@dataclass
class ExprEvalStat(StatementNode):
    expr: ExpressionNode

@dataclass
class ReturnStat(StatementNode):
    return_value: ExpressionNode | None = None

@dataclass
class BinaryExpr(ExpressionNode):
    operator: str
    left: ExpressionNode
    right: ExpressionNode

@dataclass
class UnaryExpr(ExpressionNode):
    operator: str
    operand: ExpressionNode

@dataclass
class Variable(ExpressionNode):
    name: str

@dataclass
class NumberConstant(ExpressionNode):
    value: float

@dataclass
class CallExpr(ExpressionNode):
    callee: str
    arguments: list[ExpressionNode]

# 递归下降解析器
def parse(tokens: list[Token]) -> ModuleNode:
    pos = 0
    maxlen = len(tokens)

    def available(offset: int = 0):
        nonlocal maxlen, pos
        return pos + offset < maxlen

    def advance(count: int = 1):
        nonlocal pos
        pos += count

    def peek_type(offset: int = 0):
        return peek(offset).type

    def peek(offset: int = 0):
        nonlocal tokens, pos
        return tokens[pos + offset]

    def match(expected_type: str):
        token = peek()
        got_type = token.type
        if got_type == expected_type:
            advance()
            return token
        else:
            raise Exception(f"got type {got_type}, but expected {expected_type}")

    def parse_module():
        functions: list[FunctionNode] = []
        global_vars: list[BinaryExpr] = []
        while available():
            token = peek()
            match token.type:
                case 'function':
                    functions.append(parse_function())
                case 'identifier':
                    assign = parse_assign_expr()
                    match(';')
                    assert isinstance(assign, BinaryExpr) and assign.operator == '='
                    global_vars.append(assign)
                case unexpected_type:
                    raise Exception(f"Unexpected token: {unexpected_type}")
        return ModuleNode(functions, global_vars)
    
    def parse_function():
        match('function')
        name = match('identifier').text
        match('(')
        params: list[str] = []
        if peek_type() != ')':
            params.append(match('identifier').text)
            while peek_type() != ')':
                match(',')
                params.append(match('identifier').text)
        match(')')
        body = parse_statements_block()
        return FunctionNode(name, params, body)
    
    def parse_statement() -> StatementNode:
        match peek_type():
            case '{': return parse_statements_block()
            case 'if': return parse_if_statement()
            case 'while': return parse_while_stat()
            case 'continue': return parse_continue_stat()
            case 'break': return parse_break_stat()
            case 'return': return parse_return_stat()
            case _: return parse_expr_eval_stat()

    def parse_statements_block():
        match('{')
        statements: list[StatementNode] = []
        while peek_type() != '}':
            statements.append(parse_statement())
        match('}')
        return BlockStat(statements)

    def parse_if_statement():
        match('if')
        match('(')
        condition = parse_expression()
        match(')')
        branch_true = parse_statement()
        if peek_type() == 'else':
            match('else')
            branch_false = parse_statement()
            return IfStat(condition, branch_true, branch_false)
        else:
            return IfStat(condition, branch_true)
    
    def parse_while_stat():
        match('while')
        match('(')
        condition = parse_expression()
        match(')')
        body = parse_statement()
        return WhileStat(condition, body)

    def parse_continue_stat():
        match('continue')
        match(';')
        return ContinueStat()

    def parse_break_stat():
        match('break')
        match(';')
        return BreakStat()

    def parse_return_stat():
        match('return')
        if peek_type() == ';':
            match(';')
            return ReturnStat()
        else:
            value = parse_expression()
            match(';')
            return ReturnStat(value)
    
    def parse_expr_eval_stat():
        expr = parse_expression()
        match(';')
        return ExprEvalStat(expr)

    def parse_expression() -> ExpressionNode:
        return parse_assign_expr()
    
    def parse_assign_expr() -> ExpressionNode:
        if available(1) and peek_type() == 'identifier' and peek_type(1) == '=':
            var = parse_variable()
            match('=')
            value = parse_expression()
            return BinaryExpr('=', var, value)
        else:
            return parse_compare_expr()
    
    def parse_compare_expr() -> ExpressionNode:
        left = parse_add_expr()
        if available() and peek_type() in ('==', '!=', '<=', '<', '>=', '>'):
            operator = match(peek_type()).type
            right = parse_compare_expr()
            return BinaryExpr(operator, left, right)
        else:
            return left
    
    def parse_add_expr() -> ExpressionNode:
        left = parse_mul_expr()
        if available() and peek_type() in ('+', '-'):
            operator = match(peek_type()).type
            right = parse_add_expr()
            return BinaryExpr(operator, left, right)
        else:
            return left
        
    def parse_mul_expr() -> ExpressionNode:
        left = parse_unary_expr()
        if available() and peek_type() in ('*', '/'):
            operator = match(peek_type()).type
            right = parse_mul_expr()
            return BinaryExpr(operator, left, right)
        else:
            return left
        
    def parse_unary_expr() -> ExpressionNode:
        match peek_type():
            case '+':
                match('+')
                operand = parse_unary_expr()
                return UnaryExpr('+', operand)
            case '-':
                match('-')
                operand = parse_unary_expr()
                return UnaryExpr('-', operand)
            case '!':
                match('!')
                operand = parse_unary_expr()
                return UnaryExpr('!', operand)
            case _:
                return parse_primary_expr()

    def parse_primary_expr() -> ExpressionNode:
        match peek_type():
            case 'number':
                return parse_number_constant()
            case 'identifier':
                if available(1) and peek_type(1) == '(':
                    return parse_call_expr()
                else :
                    return parse_variable()
            case '(':
                match('(')
                expr = parse_expression()
                match(')')
                return expr
            case unexpected_type:
                raise SyntaxError(f"Unexpected token: {unexpected_type}")
            
    def parse_call_expr() -> ExpressionNode:
        callee = match('identifier').text
        match('(')
        args: list[ExpressionNode] = []
        if peek_type() != ')':
            args.append(parse_expression())
            while peek_type() == ',':
                match(',')
                args.append(parse_expression())
        match(')')
        return CallExpr(callee, args)

    def parse_variable():
        name = match('identifier').text
        return Variable(name)

    def parse_number_constant():
        value = match('number').text
        return NumberConstant(float(value))

    # 调用 起始文法规则 (module) 开始匹配
    try:
        module = parse_module()
    except Exception as e:
        print(f"at: {pos}")
        raise e
    return module

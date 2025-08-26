from parser import *

def interpret(module: ModuleNode):
    class BreakException(Exception): pass
    class ContinueException(Exception): pass
    class ReturnException(Exception): pass

    def get_variable(name: str):
        nonlocal global_vars, local_vars
        if name in local_vars: return local_vars[name]
        elif name in global_vars: return global_vars[name]
        else: raise NameError(f"Variable not found: {name}")

    def set_variable(name: str, value: float):
        nonlocal global_vars, local_vars
        if name in local_vars: local_vars[name] = value
        elif name in global_vars: global_vars[name] = value
        else: local_vars[name] = value

    def call_function(function: FunctionNode, args: list[float]) -> float:
        nonlocal function_map, stored_states, local_vars
        stored_states.append(local_vars)
        local_vars = {}

        assert len(function.parameters) == len(args)
        for i in range(len(args)):
            local_vars[function.parameters[i]] = args[i]

        try:
            exec_block_stat(function.body)
        except ReturnException:
            pass

        return_value = local_vars.get('return-value', 0.0)
        local_vars = stored_states.pop()
        return return_value
    
    def exec_stat(stat: StatementNode):
        match stat:
            case BlockStat(): exec_block_stat(stat)
            case IfStat(): exec_if_stat(stat)
            case WhileStat(): exec_while_stat(stat)
            case BreakStat(): exec_break_stat(stat)
            case ContinueStat(): exec_continue_stat(stat)
            case ExprEvalStat(): exec_expr_eval_stat(stat)
            case ReturnStat(): exec_return_stat(stat)
            case _: raise NotImplementedError(f"Unknown statement: {stat}")

    def exec_block_stat(stats: BlockStat):
        for stat in stats.statements:
            exec_stat(stat)

    def exec_if_stat(stat: IfStat):
        condition = eval_expr(stat.condition)
        if condition:
            exec_stat(stat.branch_true)
        else:
            if stat.branch_false is not None:
                exec_stat(stat.branch_false)
    
    def exec_while_stat(stat: WhileStat):
        while eval_expr(stat.condition):
            try:
                exec_stat(stat.body)
            except BreakException:
                break
            except ContinueException:
                continue

    def exec_break_stat(stat: BreakStat):
        raise BreakException()

    def exec_continue_stat(stat: ContinueStat):
        raise ContinueException()

    def exec_expr_eval_stat(stat: ExprEvalStat):
        eval_expr(stat.expr)

    def exec_return_stat(stat: ReturnStat):
        if stat.return_value is not None:
            local_vars['return-value'] = eval_expr(stat.return_value)
        raise ReturnException()

    def eval_expr(expr: ExpressionNode) -> float:
        match expr:
            case NumberConstant(value): return value
            case BinaryExpr(): return eval_binary_expr(expr)
            case UnaryExpr(): return eval_unary_expr(expr)
            case CallExpr(): return eval_call_expr(expr)
            case Variable(name): return get_variable(name)
            case _: raise NotImplementedError(f"Unknown expression: {expr}")

    def eval_binary_expr(expr: BinaryExpr) -> float:
        # 赋值表达式
        if expr.operator == '=' and isinstance(expr.left, Variable):
            value = eval_expr(expr.right)
            set_variable(expr.left.name, value)
            return value
        left = eval_expr(expr.left)
        right = eval_expr(expr.right)
        match expr.operator:
            case '+': return left + right
            case '-': return left - right
            case '*': return left * right
            case '/': return left / right
            case '==': return float(left == right)
            case '!=': return float(left != right)
            case '<': return float(left < right)
            case '<=': return float(left <= right)
            case '>': return float(left > right)
            case '>=': return float(left >= right)
            case unexpected_op: raise NotImplementedError(f"Unknown operator: {unexpected_op}")

    def eval_unary_expr(expr: UnaryExpr) -> float:
        operand = eval_expr(expr.operand)
        match expr.operator:
            case '+': return operand
            case '-': return -operand
            case '!': return float(not operand)
            case unexpected_op: raise NotImplementedError(f"Unknown operator: {unexpected_op}")

    def eval_call_expr(expr: CallExpr) -> float:
        args = [eval_expr(arg) for arg in expr.arguments]
        if expr.callee == 'print':
            print(*args)
            return 0.0
        func = function_map[expr.callee]
        return call_function(func, args)

    function_map: dict[str, FunctionNode] = {}
    global_vars: dict[str, float] = {}
    stored_states: list[dict[str, float]] = []
    local_vars: dict[str, float] = {}

    for function in module.functions:
        function_map[function.name] = function
    for var in module.global_vars:
        assert var.operator == '=' and isinstance(var.left, Variable)
        global_vars[var.left.name] = eval_expr(var.right)

    if 'main' in function_map:
        main = function_map['main']
        return_value = call_function(main, [])
        return return_value
    else:
        return 0.0

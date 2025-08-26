grammar slang_grammar;

// 词法

// 注释不生成词元
Comment: '#' ~[\n]* -> skip;
// 空格不生成词元
Whitespace: [ \r\n\t] -> skip;

fragment Alphabet: [a-zA-Z];
fragment Digit: [0-9];

// 名字 = 字母 (字母 | 数字)*
Identifier: Alphabet (Alphabet | Digit)*;
// 数 = 数字+ ('.' 数字+)?
Number: Digit+ ('.' Digit+)?;

// 语法

// 模块 = 全局声明*
module: global_declaration*;
// 全局声明 = 函数声明 | 全局变量声明
global_declaration: function | assignment_expr ';';

// 函数 = 'function' 名字 '(' (形参 (',' 形参)* )? ')' '{' 语句* '}'
function: 'function' Identifier '(' (Identifier (',' Identifier)*)? ')' statement_block;

// 语句
statement
: statement_block
| if_stat
| while_stat
| break_stat
| continue_stat
| expr_eval_stat
| return_stat
;
// 语句块 = '{' 语句* '}'
statement_block: '{' statement* '}';
// if语句 = 'if' '(' 条件 ')' 语句 ('else' 语句)?
if_stat: 'if' '(' expression ')' statement ('else' statement)?;
// while语句 = 'while' '(' 条件 ')' 语句
while_stat: 'while' '(' expression ')' statement;
break_stat: 'break' ';';
continue_stat: 'continue' ';';
// 表达式求值语句 = 表达式 ';'
expr_eval_stat: expression ';';
// 返回语句 = 'return' 表达式?
return_stat: 'return' expression?;

// 表达式按照运算符优先级的升序来匹配，先匹配优先级低的
expression: assignment_expr;
assignment_expr: variable '=' expression;
// 二元运算符表达式，消除左递归并依次匹配
compare_expr: add_expr (('==' | '!=' | '<=' | '<' | '>=' | '>') compare_expr)?;
add_expr: mul_expr (('+' | '-') add_expr)?;
mul_expr: unary_expr (('*' | '/') mul_expr)?;
unary_expr: ('+' | '-' | '!')? primary_expr;
// 调用表达式 = 函数名 '(' 实参 (',' 实参)* ')'
call_expr: Identifier '(' (expression (',' expression)*)? ')';
variable: Identifier;
number_constant: Number;
// 不能分割出去一个运算符的表达式，就是 primary expression
// 比如 数字常量，调用表达式，取变量值表达式，括号括起来的表达式
primary_expr
: number_constant
| call_expr
| variable
| '(' expression ')'
;

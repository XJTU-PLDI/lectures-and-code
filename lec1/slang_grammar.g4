grammar slang_grammar;

// tokenizing rules

Comment: '#' ~[\n]* -> skip;
Whitespace: [ \r\n\t] -> skip;

fragment Alphabet: [a-zA-Z];
fragment Digit: [0-9];

Identifier: Alphabet (Alphabet | Digit)*;
Number: Digit+ ('.' Digit+)?;

// parsing rules

module: global_declaration*;
global_declaration: function | assignment_expr ';';

function: 'function' Identifier '(' (Identifier (',' Identifier)*)? ')' statement_block;

statement
: statement_block
| if_stat
| while_stat
| break_stat
| expr_eval_stat
| return_stat
;
statement_block: '{' statement* '}';
if_stat: 'if' '(' expression ')' statement ('else' statement)?;
while_stat: 'while' '(' expression ')' statement;
break_stat: 'break' ';';
expr_eval_stat: expression ';';
return_stat: 'return' expression?;

expression: assignment_expr;
assignment_expr: variable '=' expression;
compare_expr: add_expr (('==' | '!=' | '<=' | '<' | '>=' | '>') compare_expr)?;
add_expr: mul_expr (('+' | '-') add_expr)?;
mul_expr: unary_expr (('*' | '/') mul_expr)?;
unary_expr: ('+' | '-' | '!')? primary_expr;
call_expr: Identifier '(' (expression (',' expression)*)? ')';
variable: Identifier;
number_constant: Number;
primary_expr
: number_constant
| call_expr
| variable
| '(' expression ')'
;

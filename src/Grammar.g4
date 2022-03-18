grammar Grammar;

prog: stat+ ;

stat: expr ';'                              # exprStat
    | prim ID '=' expr ';'                  # initStat
    | lhs=ID '=' rhs=expr ';'               # assignStat
    ;

expr
    : '(' expr ')'                          # parensExpr
    | op=('+'|'-'|'!') expr                 # unaryExpr
    | left=expr op=('*'|'/') right=expr     # binExpr
    | left=expr op=('+'|'-') right=expr     # binExpr
    | left=expr op=('>'|'<') right=expr     # binExpr
    | left=expr op=('=='|'>=') right=expr   # binExpr
    | left=expr op=('<='|'!=') right=expr   # binExpr
    | left=expr op=('||'|'&&') right=expr   # binExpr
    | value=ID                              # idExpr
    | value=lit                             # litExpr
    ;

lit
    : lit_prim=(CHAR|INT|FLOAT)             # primLit
    ;

prim
    : KEY_CHAR                              # charPrim
    | KEY_FLOAT                             # floatPrim
    | KEY_INT                               # intPrim
    ;

MUL : '*' ;
DIV : '/' ;
ADD : '+' ;
SUB : '-' ;
GRT : '>' ;
LST : '<' ;
EQ  : '==';
GEQ : '>=';
LEQ : '<=';
NEQ : '!=';
NOT : '!' ;
AND : '&&';
OR  : '||';

KEY_CHAR : 'char' ;
KEY_INT : 'int' ;
KEY_FLOAT : 'float' ;

CHAR : [.~] ;
INT : [0-9]+ ;
FLOAT : [0-9]+ '.' [0-9]+ ;
ID  : [a-zA-Z]+ ;
WS: [ \n\t\r]+ -> skip;
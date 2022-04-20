grammar Grammar;

prog: stat+ ;

stat: expr ';'                                                  # exprStat
    | KEY_CONST prim ID '=' expr ';'                 # constInitStat
    | prim ID '=' expr ';'                 # initStat
    | ID '=' rhs=expr ';'                                   # assignStat
    ;

expr
    : '(' expr ')'                          # parensExpr
    | op=('+'|'-'|'!'|'*'|'&') expr         # unaryExpr
    | left=expr op=('*'|'/') right=expr     # binExpr
    | left=expr op=('+'|'-'|'%') right=expr # binExpr
    | left=expr op=('>'|'<') right=expr     # binExpr
    | left=expr op=('=='|'>=') right=expr   # binExpr
    | left=expr op=('<='|'!=') right=expr   # binExpr
    | left=expr op=('||'|'&&') right=expr   # binExpr
    | ID                                    # idExpr
    | value=lit                             # litExpr
    | 'printf' '(' (ID | lit) ')'           # PrintExpr
    ;

lit
    : lit_prim=(BOOL|CHAR|INT|FLOAT)             # primLit
    ;

prim
    : KEY_CHAR                              # charPrim
    | KEY_FLOAT                             # floatPrim
    | KEY_INT                               # intPrim
    | KEY_CHARPTR                           # charptrPrim
    | KEY_FLOATPTR                          # floatptrPrim
    | KEY_INTPTR                            # intptrPrim
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
MOD : '%' ;
DRF : '&' ;

KEY_CHARPTR : 'char' '*' ;
KEY_FLOATPTR    : 'float' '*' ;
KEY_INTPTR :'int' '*' ;
KEY_CHAR : 'char' ;
KEY_INT : 'int' ;
KEY_FLOAT : 'float' ;

KEY_CONST : 'const' ;

MULTICOMMENT : '/*' .*? '*/' -> skip;
SINGLECOMMENT: '//' .*? '\n' -> skip;
CHAR : [.~] ;
INT : [0-9]+ ;
FLOAT : [0-9]+ '.' [0-9]+ ;
BOOL 
    : 'true'
    | 'false'
    ;
ID  : [a-zA-Z_]{1}[a-zA-Z0-9_]* ;
WS: [ \n\t\r]+ -> skip;
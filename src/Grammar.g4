grammar Grammar;

prog: (KEY_INCLUDE LIB)* decl+ ;

decl: KEY_CONST? prim ID ('['INT']')? ( ( '=' expr ) | ( '=' '{' expr (',' expr)* '}' ) )? ';'      #varDecl
    | (prim | KEY_VOID) ID '('( ( (prim ID)(','prim ID)* ) | prim ID )?')' ';'                      #funcheadsupDecl           
    | (prim | KEY_VOID) ID '(' ( ( (prim ID)(','prim ID)* ) | prim ID )? ')' '{' stat* '}'          #funcDecl
    ;

stat: expr ';'                                                                                      # exprStat
    | KEY_CONST? prim ID ('['INT']')? ( ( '=' expr ) | ( '=' '{' expr (',' expr)* '}' ) )? ';'      # declStat
    | KEY_WHILE '(' expr ')' '{' stat* '}'                                                          # whileStat
    | KEY_IF '(' expr ')' '{' stat* '}' (KEY_ELSE '{' alias '}')?                                   # ifStat
    | KEY_RETURN expr ';'                                                                           # returnStat
    ;

alias: stat* ;

expr
    : '(' expr ')'                          # parensExpr
    | op=('+'|'-'|'!'|'*'|'&') expr         # unaryExpr
    | left=expr op=('*'|'/') right=expr     # binExpr
    | left=expr op=('+'|'-'|'%') right=expr # binExpr
    | left=expr op=('>'|'<') right=expr     # binExpr
    | left=expr op=('=='|'>=') right=expr   # binExpr
    | left=expr op=('<='|'!=') right=expr   # binExpr
    | left=expr op=('||'|'&&') right=expr   # binExpr
    | left=expr op='=' right=expr           # binExpr
    | ID '(' ( ( ((expr))(','(expr))* ) | (expr) )? ')'   # callExpr
    | ID                                    # idExpr
    | value=lit                             # litExpr
    ;

lit
    : lit_prim=(STRING|CHAR|INT|FLOAT)             # primLit
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
ASS : '=' ;
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
KEY_VOID : 'void' ;

KEY_CONST : 'const' ;
KEY_INCLUDE : '#include' ;
KEY_FOR : 'for' ;
KEY_WHILE : 'while' ;
KEY_IF : 'if' ;
KEY_ELSE : 'else' ;
KEY_RETURN : 'return' ;
KEY_BREAK : 'break' ;
KEY_CONTINUE : 'continue' ;

MULTICOMMENT : '/*' .*? '*/' -> skip;
SINGLECOMMENT: '//' .*? '\n' -> skip;
CHAR : ['] . ['] ;
STRING : ["] .*? ["] ;
INT : [0-9]+ ;
FLOAT : [0-9]+ '.' [0-9]+ ;
BOOL 
    : 'true'
    | 'false'
    ;
ID  : [a-zA-Z_]{1}[a-zA-Z0-9_]* ;
LIB : '<' [a-z]+ '.h>' ;
WS: [ \n\t\r]+ -> skip;
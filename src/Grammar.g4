grammar Grammar;

prog: (KEY_INCLUDE LIB)* decl+ ;

decl: prim varhelp (COMMA varhelp)* SEMICOLON      #varDecl
    | (prim | KEY_VOID) ID OPEN_PAR (((func_arg)(COMMA func_arg)* ) | func_arg)? CLOSE_PAR SEMICOLON                   #funcheadsupDecl           
    | (prim | KEY_VOID) ID OPEN_PAR (((func_arg)(COMMA func_arg)*) | func_arg)? CLOSE_PAR OPEN_CURLY stat* CLOSE_CURLY       #funcDecl
    ;

varhelp: ID (OPEN_BRACKET expr CLOSE_BRACKET)? ((ASS expr) | (ASS OPEN_CURLY expr(COMMA expr)* CLOSE_CURLY))? ; 

func_arg: prim ID (OPEN_BRACKET INT? CLOSE_BRACKET)? ;

stat: expr SEMICOLON                                                                                                    # exprStat
    | prim varhelp (COMMA varhelp)* SEMICOLON                                                                           # declStat
    | KEY_WHILE OPEN_PAR expr CLOSE_PAR OPEN_CURLY stat* CLOSE_CURLY                                                    # whileStat
    | KEY_FOR OPEN_PAR (stat | SEMICOLON) expr SEMICOLON expr? CLOSE_PAR OPEN_CURLY alias CLOSE_CURLY      # forStat
    | KEY_IF OPEN_PAR expr CLOSE_PAR OPEN_CURLY stat* CLOSE_CURLY (KEY_ELSE OPEN_CURLY alias CLOSE_CURLY)?              # ifStat
    | KEY_RETURN expr? SEMICOLON                                                                                        # returnStat
    | KEY_BREAK SEMICOLON                                                                                               # breakStat
    | KEY_CONTINUE SEMICOLON                                                                                            # continueStat
    | OPEN_CURLY stat* CLOSE_CURLY                                                                                      # unnamedScopeStat
    ;

alias: stat* ;

expr
    : OPEN_PAR expr CLOSE_PAR                                       # parensExpr
    | op=(ADD|SUB|NOT|MUL|DRF|MPP|PPP) expr                         # preUnaryExpr
    | expr op=(PPP|MPP)                                             # postUnaryExpr
    | left=expr op=(MUL|DIV) right=expr                             # binExpr
    | left=expr op=(ADD|SUB|MOD) right=expr                         # binExpr
    | left=expr op=(GRT|LST) right=expr                             # binExpr
    | left=expr op=(EQ|GEQ) right=expr                              # binExpr
    | left=expr op=(LEQ|NEQ) right=expr                             # binExpr
    | left=expr op=(OR|AND) right=expr                              # binExpr
    | left=expr op=ASS right=expr                                   # binExpr
    | ID OPEN_PAR ((((expr)) (COMMA (expr))*) | (expr))? CLOSE_PAR  # callExpr
    | ID (OPEN_BRACKET (expr|INT) CLOSE_BRACKET)?                   # idExpr
    | value=lit                                                     # litExpr
    ;

lit
    : lit_prim=(STRING|CHAR|INT|FLOAT)             # primLit
    ;

prim
    : KEY_CONST? KEY_CHAR (MUL+)? KEY_CONST?    # charPrim
    | KEY_CONST? KEY_FLOAT (MUL+)? KEY_CONST?   # floatPrim
    | KEY_CONST? KEY_INT (MUL+)? KEY_CONST?     # intPrim
    ;

COMMA : ',' ;
SEMICOLON : ';' ;
OPEN_CURLY : '{' ;
CLOSE_CURLY : '}' ;
OPEN_PAR : '(' ;
CLOSE_PAR : ')' ;
OPEN_BRACKET : '[' ;
CLOSE_BRACKET : ']' ;

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
PPP : '++';
MPP : '--';

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
ID  : [a-zA-Z_]{1}[a-zA-Z0-9_]* ;
LIB : '<' [a-z]+ '.h>' ;
WS: [ \n\t\r]+ -> skip;
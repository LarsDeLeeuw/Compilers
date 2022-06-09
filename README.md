# Compilers

My grammar is in src/Grammar.g4,
    
To run python main.py input.c

TODO: Throw syntax error when break or continue statement not in loop/switch scope
      Implement DeadCode/Unreachable Code, my break and continue depend on it, break/return/continueStmt node should be last stmtnode of a scope
      forwardDeclaration.c works but is not fully implemented yet for example arguments arent checked yet when init an decl function
      Need to implement for-loop
      Need to add type implicitcasts for binaryop expr
      

Grammar:
      TODO: 
            * Add const support.
            * Add unnamed scope support, should not be allot of work. These are illegal in global scope. But could recognise them and throw sementic error after.
            * Add For-loop support, should be straightforward if I can create a while-loop that does the same thing.
            * (Optional) Maybe implement switch, can be converted to if-else so not allot of work.



# Features

## Grammar

| Description                                                                                    | ?   |
| ---------------------------------------------------------------------------------------------- | --- |
| (mandatory) Binary operations +, -, *, and /.                                                  | V   |
| (mandatory) Binary operations >, <, and ==.                                                    | V   |
| (mandatory) Unary operators + and -                                                            | V   |
| (mandatory) Brackets to overwrite the order of operations.                                     | V   |
| (mandatory) Logical operators c-style "and", "or", and !.                                      | V   |
| (optional) Comparison operators >=, <=, and !=.                                                | V   |
| (optional) Binary operator %.                                                                  | V   |
| (mandatory) Types.                                                                             | V   |
| (mandatory) Reserved word: "const"                                                             | -   |
| (mandatory) Variables.                                                                         | V   |
| (mandatory) Pointer Operations * and &.                                                        | V   |
| (optional) Identifier Operations -- and ++                                                     | V   |
| (optional) Conversions. Implicit casts with warnings where needed. No explicit cast supported. | V   |
| (mandatory) Comments. Comments are ignored.                                                    | V   |
| (mandatory) Reserved word: "if"                                                                | V   |
| (mandatory) Reserved word: "else"                                                              | V   |
| (mandatory) Reserved word: "while"                                                             | V   |
| (mandatory) Reserved word: "for"                                                               | -   |
| (mandatory) Reserved word: "break"                                                             | V   |
| (mandatory) Reserved word: "continue"                                                          | V   |
| (optional) Reserved words: "switch", "case" and "default"                                      | X   |
| (mandatory) Scope: "unnamed scope"                                                             | -   |
| (mandatory) Scopes: "conditional", "loop" and "function"                                       | V   |
| (mandatory) Local and global variables                                                         | V   |
| (mandatory) Functions                                                                          | V   |
| (mandatory) Arrays.                                                                            | V   |
| (optional) Assignments of complete arrays or rows in case of multidimensional arrays.          | X   |
| (optional) Dynamic arrays.                                                                     | X   |
| (mandatory) Import.                                                                            | V   |
| (mandatory) \<stdio.h\> printf()                                                               | V   |
| (mandatory) \<stdio.h\> scanf()                                                                | V   |

## Visualisation

My compiler provides the option to generate a visualisation of the generated AST and STT. 
This visualisation returns two formats: the structure in dot format and a jpg interpreted from the dot file
Disclaimer, this visualisation is a dev feature and I don't guarantee that the generated visualisation 
matches the structure perfectly. For example the VarDeclNode of the AST appears to have 3 seperate children: 
it's type, it's identifier and the init_expr. But in reality the only child of the VarDeclNode is the init_expr.

| Description                           | ?   |
| ------------------------------------- | --- |
| (optional) Abstract Syntax Tree (AST) | V   |
| (optional) Symbol Table Tree (STT)    | V   |

## Optimizations

| Description                                                              | ?   |
| ------------------------------------------------------------------------ | --- |
| (optional) Constant Folding                                              | -   |
| (optional) Constant Propagation                                          | -   |
| (mandatory) Unreachable code and dead code: after return in a function   | -   |
| (mandatory) Unreachable code and dead code: break and continue in a loop | -   |
| (optional) Unreachable code and dead code: unused variables              | -   |
| (optional) Unreachable code and dead code: always false conditionals     | -   |


## Code generation

| Description | LLVM | MIPS |
| ----------- | ---- | ---- |
|             |      |      |
This compiler is written in python and attempts to succesfully compile a subset of the C language to MIPS instructions using ANTLR.

V: Werkend  
-: Deels werkend met gekende problemen (onderaan beschreven)  
X: Niet werkend of niet geïmplementeerd  
(blanco): TODO  


|       | Functionaliteit           | Status |
|-------|--------------------------------|---|
| 1     | Grammar                        | - |
| 1.1   | BinOp Mandatory                | - |
|       | +,-,*,/,>,<,==,&&,\|\|         | V |
|       | BinOp Optional                 | V |
|       | >=, <=, !=, %,                 | V |
| 1.2.1 | UnaryOp Mandatory              | V |
|       | +,-,!                          | V |
|       | &,*                            | V |
| 1.2.2 | UnaryOp Optional               | X |
|       | ++, --                         | X |
| 1.3.1 | Reserved Words Mandatory       | - |
|       | char, int, float               | V |
|       | const                          | V |
|       | if, else, while                | V |
|       | for, break, continue           | - |
|       | return, void                   | V |
| 1.3.2 | Reserved Words Optional        | X |
|       | switch, case, default          | X |
| 1.4   | Variables                      | V |
| 1.5   | Explicit Casting               | X |
| 1.6   | Comments                       | V |
|       | ignored                        | V |
| 1.7   | Scopes                         | V |
|       | conditional scopes             | V |
|       | function scopes                | V |
|       | local and global variabls      | V |
| 1.8   | Functions                      | V |
| 1.9   | Arrays                         | - | 
| 1.10  | Import                         | V |
| 2     | Abstract Syntax Tree           | - |
|       | visualisation                  | - |
|       | builder                        | - |
|       | implicit type conversions      | - |
| 3     | Symbol Table                   | - |
|       | visualisation                  | - |
|       | scoping                        | V |
| 4     | Optimizations                  | - |
|       | constant folding               | - |
|       | constant propagation           | X |
|       | unreachable/dead code analysis | X |
| 5     | Syntax Errors                  | - |
| 6     | Sementics Errors               | - |
| 7     | LLVM                           | - |
|       | comments (ignored)             | V |
|       | printf                         | V |
|       | scanf                          | X |
| 8     | MIPS                           | X |


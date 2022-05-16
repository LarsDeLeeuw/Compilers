# Compilers

My grammar is in src/Grammar.g4,
    
To run python main.py input.c

TODO: Throw syntax error when break or continue statement not in loop/switch scope
      Implement DeadCode/Unreachable Code, my break and continue depend on it, break/return/continueStmt node should be last stmtnode of a scope
      forwardDeclaration.c works but is not fully implemented yet for example arguments arent checked yet when init an decl function
      Need to implement for-loop
      Need to add type implicitcasts for binaryop expr
      

# About
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


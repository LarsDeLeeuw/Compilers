# Compilers

I use magick and dot so these may need to be installed for visualisation generation.

My grammar is in src/Grammar.g4,

To run execute: 
python src/main.py -f "inputlocation.c"

For help python main.py -h

To run LLVM benchmark:
Run from tests/CorrectCodeBenchmarkLLVM:

python -m unittest -v

To run MIPS benchmark:
Run from tests/CorrectCodeBenchmarkMIPS:

python -m unittest -v






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
| (mandatory) Reserved word: "const"                                                             | V   |
| (mandatory) Variables.                                                                         | V   |
| (mandatory) Pointer Operations * and &.                                                        | V   |
| (optional) Identifier Operations -- and ++                                                     | V   |
| (optional) Conversions. Implicit casts with warnings where needed. No explicit cast supported. | V   |
| (mandatory) Comments. Comments are ignored.                                                    | V   |
| (mandatory) Reserved word: "if"                                                                | V   |
| (mandatory) Reserved word: "else"                                                              | V   |
| (mandatory) Reserved word: "while"                                                             | V   |
| (mandatory) Reserved word: "for"                                                               | V   |
| (mandatory) Reserved word: "break"                                                             | V   |
| (mandatory) Reserved word: "continue"                                                          | V   |
| (optional) Reserved words: "switch", "case" and "default"                                      | X   |
| (mandatory) Scope: "unnamed scope"                                                             | V   |
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
| (optional) Constant Propagation                                          | X   |
| (mandatory) Unreachable code and dead code: after return in a function   | V   |
| (mandatory) Unreachable code and dead code: break and continue in a loop | V   |
| (optional) Unreachable code and dead code: unused variables              | X   |
| (optional) Unreachable code and dead code: always false conditionals     | X   |

* Limited form of constant folding, explained in presentation.

## Semantic Errors

| Description                       | ?   | Notes                                                            |
| --------------------------------- | --- | ---------------------------------------------------------------- |
| arrayAccessTypeMismatch.c         | V   |                                                                  |
| arrayAccessTypeMismatch2.c        | V   |                                                                  |
| arrayCompareError.c               | V   |                                                                  |
| arraySizeTypeMismatch.c           | V   |                                                                  |
| declarationDeclarationMismatch1.c | V   |                                                                  |
| declarationDeclarationMismatch2.c | V   |                                                                  |
| declarationDeclarationMismatch3.c | V   |                                                                  |
| declarationDefinitionMismatch1.c  | -   | Caught but definition is seen as original                        |
| declarationDefinitionMismatch2.c  | -   | Caught but definition is seen as original                        |
| declarationDefinitionMismatch3.c  | -   | Caught but definition is seen as original                        |
| definitionInLocalScope.c          | X   |                                                                  |
| dereferenceTypeMismatch1.c        | X   |                                                                  |
| dereferenceTypeMismatch2.c        | X   |                                                                  |
| functionCallargumentMismatch1.c   | X   |                                                                  |
| functionCallargumentMismatch2.c   | X   |                                                                  |
| functionCallargumentMismatch3.c   | X   |                                                                  |
| functionCallargumentMismatch4.c   | X   |                                                                  |
| functionRedefinition1.c           | X   |                                                                  |
| functionRedefinition2.c           | X   |                                                                  |
| functionRedefinition3.c           | X   |                                                                  |
| incompatibleTypes1.c              | X   |                                                                  |
| incompatibleTypes2.c              | X   |                                                                  |
| incompatibleTypes3.c              | X   |                                                                  |
| incompatibleTypes4.c              | X   |                                                                  |
| incompatibleTypes5.c              | X   |                                                                  |
| incompatibleTypes6.c              | X   |                                                                  |
| incompatibleTypes7.c              | X   |                                                                  |
| invalidIncludeError.c             | X   |                                                                  |
| invalidLoopControlStatement.c     | X   |                                                                  |
| invalidUnaryOperation.c           | X   |                                                                  |
| mainNotFound.c                    | X   | Bad example of no main IMO, also does error but in parsing phase |
| parameterRedefinition1.c          | X   |                                                                  |
| parameterRedefinition2.c          | X   |                                                                  |
| parameterRedefinition3.c          | X   |                                                                  |
| pointerOperationError.c           | X   |                                                                  |
| returnOutsideFunction.c           | X   |                                                                  |
| returnTypeMismatch.c              | X   |                                                                  |
| undeclaredVariable1.c             | X   |                                                                  |
| undeclaredVariable2.c             | X   |                                                                  |
| undeclaredVariable3.c             | X   |                                                                  |
| variableRedefinition1.c           | V   |                                                                  |
| variableRedefinition2.c           | V   |                                                                  |
| variableRedefinition3.c           | V   |                                                                  |
| variableRedefinition4.c           | V   |                                                                  |
| variableRedefinition5.c           | -   | Gets caught but global error message not fully accurate.         |
| variableRedefinition6.c           | -   | Gets caught but als catches legal init cause globalscope         |
|                                   |     |                                                                  |


## Code generation

| Description                                                                                    | LLVM    | MIPS  |
| ---------------------------------------------------------------------------------------------- | ------- | ----- |
| (mandatory) Binary operations +, -, *, and /.                                                  | (old) V | V     |
| (mandatory) Binary operations >, <, and ==.                                                    | (old) V | V     |
| (mandatory) Unary operators + and -                                                            | V       | V     |
| (mandatory) Brackets to overwrite the order of operations.                                     | V       | V     |
| (mandatory) Logical operators c-style "and", "or", and !.                                      | (old) V | V     |
| (optional) Comparison operators >=, <=, and !=.                                                | (old) V | V     |
| (optional) Binary operator %.                                                                  | V       | V     |
| (mandatory) Types.                                                                             | V       | V     |
| (mandatory) Reserved word: "const"                                                             | V       | V     |
| (mandatory) Variables.                                                                         | V       | V     |
| (mandatory) Pointer Operations * and &.                                                        | V       | V     |
| (optional) Identifier Operations -- and ++                                                     | V       | V     |
| (optional) Conversions. Implicit casts with warnings where needed. No explicit cast supported. | V       | V     |
| (mandatory) Comments. Comments are ignored.                                                    | V       | V     |
| (mandatory) Reserved word: "if"                                                                | V       | V     |
| (mandatory) Reserved word: "else"                                                              | V       | V     |
| (mandatory) Reserved word: "while"                                                             | V       | V     |
| (mandatory) Reserved word: "for"                                                               | V       | V     |
| (mandatory) Reserved word: "break"                                                             | V       | V     |
| (mandatory) Reserved word: "continue"                                                          | V       | V     |
| (optional) Reserved words: "switch", "case" and "default"                                      | X       | X     |
| (mandatory) Scope: "unnamed scope"                                                             | V       | V     |
| (mandatory) Scopes: "conditional", "loop" and "function"                                       | V       | V     |
| (mandatory) Local and global variables                                                         | V       | V     |
| (mandatory) Functions                                                                          | V       | V     |
| (mandatory) Arrays.                                                                            | V       | V     |
| (optional) Assignments of complete arrays or rows in case of multidimensional arrays.          | X       | X     |
| (optional) Dynamic arrays.                                                                     | X       | X     |
| (mandatory) Import.                                                                            | V       | V     |
| (mandatory) \<stdio.h\> printf()                                                               | V       | V     |
| (mandatory) \<stdio.h\> scanf()                                                                | V       | -     |
| ---------------------------------------------------------------------------------------------- | ------- | ----- |
| BenchmarkCorrectCode                                                                           | 32/32   | 30/32 |
| * unaryOperations.c and scanf2.c dont work for MIPS                                            |         |       |




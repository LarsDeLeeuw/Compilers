import sys
from antlr4 import *
from GrammarLexer import GrammarLexer
from GrammarParser import GrammarParser
from BuildASTVisitor import BuildASTVisitor
from VisualASTVisitor import VisualASTVisitor

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = GrammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = GrammarParser(stream)
    cst = parser.prog()
    builder = BuildASTVisitor()
    builder.visit(cst)
    AST = builder.getAST()
    ASTVisualDOT = VisualASTVisitor()
    print(AST.root)
    AST.accept(ASTVisualDOT)
    outputdotfile = open("output.dot", 'w')
    outputdotfile.write("digraph {" + ASTVisualDOT.labelbuffer + ASTVisualDOT.edgebuffer + "}")

    print(ASTVisualDOT.labelbuffer)
    print(ASTVisualDOT.edgebuffer)

if __name__ == '__main__':
    main(sys.argv)
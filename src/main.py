import sys
from antlr4 import *
from GrammarLexer import GrammarLexer
from GrammarParser import GrammarParser
from BuildASTVisitor import BuildASTVisitor
from VisualASTVisitor import VisualASTVisitor
from ConstFoldingASTVisitor import ConstFoldingASTVisitor
from AST import AST
from subprocess import check_call

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = GrammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = GrammarParser(stream)
    cst = parser.prog()
    builder = BuildASTVisitor()
    builder.visit(cst)
    ASTree= builder.getAST()
    ASTVisualDOT = VisualASTVisitor()
    ASTConstFolding = ConstFoldingASTVisitor()
    ASTree.accept(ASTConstFolding)
    ASTree.accept(ASTVisualDOT)
    ASTree.save("AST_ex_ass.xml")
    outputdotfile = open("output.dot", 'w')
    outputdotfile.write("digraph {" + ASTVisualDOT.labelbuffer + ASTVisualDOT.edgebuffer + "}")    
    # print(ASTVisualDOT.labelbuffer)
    # print(ASTVisualDOT.edgebuffer)import pydot
    outputdotfile.close()

    check_call(['dot','-Tpng','output.dot','-o','OutputFile.png'])

if __name__ == '__main__':
    main(sys.argv)
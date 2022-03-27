import sys
from antlr4 import *
from GrammarLexer import GrammarLexer
from GrammarParser import GrammarParser
from BuildASTVisitor import BuildASTVisitor
from VisualASTVisitor import VisualASTVisitor
from ConstFoldingASTVisitor import ConstFoldingASTVisitor
from AST import AST

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
    # AST.accept(ASTConstFolding)
    ASTree.accept(ASTVisualDOT)
    ASTree.save("AST_bin_op_1.xml")
    outputdotfile = open("output.dot", 'w')
    outputdotfile.write("digraph {" + ASTVisualDOT.labelbuffer + ASTVisualDOT.edgebuffer + "}")    
    # print(ASTVisualDOT.labelbuffer)
    # print(ASTVisualDOT.edgebuffer)

if __name__ == '__main__':
    main(sys.argv)
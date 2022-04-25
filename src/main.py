import sys
from antlr4 import *
from GrammarLexer import GrammarLexer
from GrammarParser import GrammarParser
from BuildASTVisitor import BuildASTVisitor
from VisualASTVisitor import VisualASTVisitor
# from ConstFoldingASTVisitor import ConstFoldingASTVisitor
from AST import AST
from LLVMASTVisitor import LLVMASTVisitor
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
    ASTree.stt.generateImage()
    ASTVisualDOT = VisualASTVisitor()
    #ASTConstFolding = ConstFoldingASTVisitor()
    ASTLLVM = LLVMASTVisitor()
    #ASTree.accept(ASTConstFolding)
    ASTree.accept(ASTLLVM)
    ASTree.accept(ASTVisualDOT)
    #ASTree.save("AST_ex_ass.xml")
    outputdotfile = open("output.dot", 'w')
    outputdotfile.write("digraph {" + ASTVisualDOT.labelbuffer + ASTVisualDOT.edgebuffer + "}")
    outputdotfile.close()

    check_call(['dot','-Tjpg','output.dot','-o','OutputFile.jpg'])
    # Convert to darkmode to spare my eyes.
    check_call(['magick','OutputFile.jpg','-negate','OutputFile.jpg'])

    check_call(['lli','main.ll'])

if __name__ == '__main__':
    main(sys.argv)
import sys
from antlr4 import *
from GrammarLexer import GrammarLexer
from GrammarParser import GrammarParser
from BuildASTVisitor import BuildASTVisitor
from VisualASTVisitor import VisualASTVisitor
from ConstFoldingASTVisitor import ConstFoldingASTVisitor
from AST import AST
from LLVMASTVisitor import LLVMASTVisitor
from subprocess import call, check_call
import argparse

# Argument parsing
parser = argparse.ArgumentParser()

# -f INPUT -c CONFIG { 0 : (default, generates LLVM code for single inputfile), 1 : (folder, generates LLVM code for all inputfiles in folder)}
# -v VISUALS {True, False} -o OPTIMIZATIONS
parser.add_argument("-f", "--input", dest = "path", default = "No input", help = "Input path")
parser.add_argument("-c", "--config", dest = "config", default=0, help="Config 0 for single inputfile, 1 for folder, 2 devmode", type=int)
parser.add_argument("-v", "--visualize", dest = "visual", default=0, help="Visualization level: 0 (default) no visuals, 1 AST visuals, 2 AST + STT visuals", type=int)
parser.add_argument("-o", "--optimizations", dest="optimizations", default=0, help="Optimization level: 0 (default) no optimizations, 1 placeholder, 2 max optimizations", type=int)

args = parser.parse_args()

def main(argv):
    input_stream = FileStream(args.path)
    lexer = GrammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = GrammarParser(stream)
    cst = parser.prog()
    builder = BuildASTVisitor()
    builder.visit(cst)
    ASTree= builder.getAST()
    STTree = builder.getSTT()

    if args.optimizations == 2:
        ASTConstFolding = ConstFoldingASTVisitor()
        ASTree.accept(ASTConstFolding)
    if args.visual >= 1:
        ASTVisualDOT = VisualASTVisitor()
        ASTree.accept(ASTVisualDOT)
        # TODO: write generateImage()
        outputdotfile = open("output.dot", 'w')
        outputdotfile.write("digraph {" + ASTVisualDOT.labelbuffer + ASTVisualDOT.edgebuffer + "}")
        outputdotfile.close()
        check_call(['dot','-Tjpg','output.dot','-o','OutputFile.jpg'])
        # Convert to darkmode
        check_call(['magick','OutputFile.jpg','-negate','OutputFile.jpg'])
    if args.visual == 2:
        STTree.generateImage()
    
    ASTLLVM = LLVMASTVisitor()
    ASTLLVM.loadSTT(STTree)
    ASTree.accept(ASTLLVM)

    if args.config == 2:
        call(['lli','main.ll'])
    
    return 0

if __name__ == '__main__':
    main(sys.argv)
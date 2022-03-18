# Generated from Grammar.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .GrammarParser import GrammarParser
else:
    from GrammarParser import GrammarParser

# This class defines a complete listener for a parse tree produced by GrammarParser.
class GrammarListener(ParseTreeListener):

    # Enter a parse tree produced by GrammarParser#prog.
    def enterProg(self, ctx:GrammarParser.ProgContext):
        pass

    # Exit a parse tree produced by GrammarParser#prog.
    def exitProg(self, ctx:GrammarParser.ProgContext):
        pass


    # Enter a parse tree produced by GrammarParser#exprStat.
    def enterExprStat(self, ctx:GrammarParser.ExprStatContext):
        pass

    # Exit a parse tree produced by GrammarParser#exprStat.
    def exitExprStat(self, ctx:GrammarParser.ExprStatContext):
        pass


    # Enter a parse tree produced by GrammarParser#initStat.
    def enterInitStat(self, ctx:GrammarParser.InitStatContext):
        pass

    # Exit a parse tree produced by GrammarParser#initStat.
    def exitInitStat(self, ctx:GrammarParser.InitStatContext):
        pass


    # Enter a parse tree produced by GrammarParser#assignStat.
    def enterAssignStat(self, ctx:GrammarParser.AssignStatContext):
        pass

    # Exit a parse tree produced by GrammarParser#assignStat.
    def exitAssignStat(self, ctx:GrammarParser.AssignStatContext):
        pass


    # Enter a parse tree produced by GrammarParser#binExpr.
    def enterBinExpr(self, ctx:GrammarParser.BinExprContext):
        pass

    # Exit a parse tree produced by GrammarParser#binExpr.
    def exitBinExpr(self, ctx:GrammarParser.BinExprContext):
        pass


    # Enter a parse tree produced by GrammarParser#unaryExpr.
    def enterUnaryExpr(self, ctx:GrammarParser.UnaryExprContext):
        pass

    # Exit a parse tree produced by GrammarParser#unaryExpr.
    def exitUnaryExpr(self, ctx:GrammarParser.UnaryExprContext):
        pass


    # Enter a parse tree produced by GrammarParser#parensExpr.
    def enterParensExpr(self, ctx:GrammarParser.ParensExprContext):
        pass

    # Exit a parse tree produced by GrammarParser#parensExpr.
    def exitParensExpr(self, ctx:GrammarParser.ParensExprContext):
        pass


    # Enter a parse tree produced by GrammarParser#litExpr.
    def enterLitExpr(self, ctx:GrammarParser.LitExprContext):
        pass

    # Exit a parse tree produced by GrammarParser#litExpr.
    def exitLitExpr(self, ctx:GrammarParser.LitExprContext):
        pass


    # Enter a parse tree produced by GrammarParser#idExpr.
    def enterIdExpr(self, ctx:GrammarParser.IdExprContext):
        pass

    # Exit a parse tree produced by GrammarParser#idExpr.
    def exitIdExpr(self, ctx:GrammarParser.IdExprContext):
        pass


    # Enter a parse tree produced by GrammarParser#primLit.
    def enterPrimLit(self, ctx:GrammarParser.PrimLitContext):
        pass

    # Exit a parse tree produced by GrammarParser#primLit.
    def exitPrimLit(self, ctx:GrammarParser.PrimLitContext):
        pass


    # Enter a parse tree produced by GrammarParser#charPrim.
    def enterCharPrim(self, ctx:GrammarParser.CharPrimContext):
        pass

    # Exit a parse tree produced by GrammarParser#charPrim.
    def exitCharPrim(self, ctx:GrammarParser.CharPrimContext):
        pass


    # Enter a parse tree produced by GrammarParser#floatPrim.
    def enterFloatPrim(self, ctx:GrammarParser.FloatPrimContext):
        pass

    # Exit a parse tree produced by GrammarParser#floatPrim.
    def exitFloatPrim(self, ctx:GrammarParser.FloatPrimContext):
        pass


    # Enter a parse tree produced by GrammarParser#intPrim.
    def enterIntPrim(self, ctx:GrammarParser.IntPrimContext):
        pass

    # Exit a parse tree produced by GrammarParser#intPrim.
    def exitIntPrim(self, ctx:GrammarParser.IntPrimContext):
        pass



del GrammarParser
# Generated from Grammar.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .GrammarParser import GrammarParser
else:
    from GrammarParser import GrammarParser

# This class defines a complete generic visitor for a parse tree produced by GrammarParser.

class GrammarVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by GrammarParser#prog.
    def visitProg(self, ctx:GrammarParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#exprStat.
    def visitExprStat(self, ctx:GrammarParser.ExprStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#initStat.
    def visitInitStat(self, ctx:GrammarParser.InitStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#assignStat.
    def visitAssignStat(self, ctx:GrammarParser.AssignStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#binExpr.
    def visitBinExpr(self, ctx:GrammarParser.BinExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#unaryExpr.
    def visitUnaryExpr(self, ctx:GrammarParser.UnaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#parensExpr.
    def visitParensExpr(self, ctx:GrammarParser.ParensExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#litExpr.
    def visitLitExpr(self, ctx:GrammarParser.LitExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#idExpr.
    def visitIdExpr(self, ctx:GrammarParser.IdExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#primLit.
    def visitPrimLit(self, ctx:GrammarParser.PrimLitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#charPrim.
    def visitCharPrim(self, ctx:GrammarParser.CharPrimContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#floatPrim.
    def visitFloatPrim(self, ctx:GrammarParser.FloatPrimContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#intPrim.
    def visitIntPrim(self, ctx:GrammarParser.IntPrimContext):
        return self.visitChildren(ctx)



del GrammarParser
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


    # Visit a parse tree produced by GrammarParser#varDecl.
    def visitVarDecl(self, ctx:GrammarParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#funcheadsupDecl.
    def visitFuncheadsupDecl(self, ctx:GrammarParser.FuncheadsupDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#funcDecl.
    def visitFuncDecl(self, ctx:GrammarParser.FuncDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#exprStat.
    def visitExprStat(self, ctx:GrammarParser.ExprStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#declStat.
    def visitDeclStat(self, ctx:GrammarParser.DeclStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#whileStat.
    def visitWhileStat(self, ctx:GrammarParser.WhileStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#ifStat.
    def visitIfStat(self, ctx:GrammarParser.IfStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#returnStat.
    def visitReturnStat(self, ctx:GrammarParser.ReturnStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#alias.
    def visitAlias(self, ctx:GrammarParser.AliasContext):
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


    # Visit a parse tree produced by GrammarParser#callExpr.
    def visitCallExpr(self, ctx:GrammarParser.CallExprContext):
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


    # Visit a parse tree produced by GrammarParser#charptrPrim.
    def visitCharptrPrim(self, ctx:GrammarParser.CharptrPrimContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#floatptrPrim.
    def visitFloatptrPrim(self, ctx:GrammarParser.FloatptrPrimContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#intptrPrim.
    def visitIntptrPrim(self, ctx:GrammarParser.IntptrPrimContext):
        return self.visitChildren(ctx)



del GrammarParser
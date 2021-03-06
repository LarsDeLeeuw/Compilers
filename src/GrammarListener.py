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


    # Enter a parse tree produced by GrammarParser#varDecl.
    def enterVarDecl(self, ctx:GrammarParser.VarDeclContext):
        pass

    # Exit a parse tree produced by GrammarParser#varDecl.
    def exitVarDecl(self, ctx:GrammarParser.VarDeclContext):
        pass


    # Enter a parse tree produced by GrammarParser#funcheadsupDecl.
    def enterFuncheadsupDecl(self, ctx:GrammarParser.FuncheadsupDeclContext):
        pass

    # Exit a parse tree produced by GrammarParser#funcheadsupDecl.
    def exitFuncheadsupDecl(self, ctx:GrammarParser.FuncheadsupDeclContext):
        pass


    # Enter a parse tree produced by GrammarParser#funcDecl.
    def enterFuncDecl(self, ctx:GrammarParser.FuncDeclContext):
        pass

    # Exit a parse tree produced by GrammarParser#funcDecl.
    def exitFuncDecl(self, ctx:GrammarParser.FuncDeclContext):
        pass


    # Enter a parse tree produced by GrammarParser#varhelp.
    def enterVarhelp(self, ctx:GrammarParser.VarhelpContext):
        pass

    # Exit a parse tree produced by GrammarParser#varhelp.
    def exitVarhelp(self, ctx:GrammarParser.VarhelpContext):
        pass


    # Enter a parse tree produced by GrammarParser#func_arg.
    def enterFunc_arg(self, ctx:GrammarParser.Func_argContext):
        pass

    # Exit a parse tree produced by GrammarParser#func_arg.
    def exitFunc_arg(self, ctx:GrammarParser.Func_argContext):
        pass


    # Enter a parse tree produced by GrammarParser#exprStat.
    def enterExprStat(self, ctx:GrammarParser.ExprStatContext):
        pass

    # Exit a parse tree produced by GrammarParser#exprStat.
    def exitExprStat(self, ctx:GrammarParser.ExprStatContext):
        pass


    # Enter a parse tree produced by GrammarParser#declStat.
    def enterDeclStat(self, ctx:GrammarParser.DeclStatContext):
        pass

    # Exit a parse tree produced by GrammarParser#declStat.
    def exitDeclStat(self, ctx:GrammarParser.DeclStatContext):
        pass


    # Enter a parse tree produced by GrammarParser#whileStat.
    def enterWhileStat(self, ctx:GrammarParser.WhileStatContext):
        pass

    # Exit a parse tree produced by GrammarParser#whileStat.
    def exitWhileStat(self, ctx:GrammarParser.WhileStatContext):
        pass


    # Enter a parse tree produced by GrammarParser#forStat.
    def enterForStat(self, ctx:GrammarParser.ForStatContext):
        pass

    # Exit a parse tree produced by GrammarParser#forStat.
    def exitForStat(self, ctx:GrammarParser.ForStatContext):
        pass


    # Enter a parse tree produced by GrammarParser#ifStat.
    def enterIfStat(self, ctx:GrammarParser.IfStatContext):
        pass

    # Exit a parse tree produced by GrammarParser#ifStat.
    def exitIfStat(self, ctx:GrammarParser.IfStatContext):
        pass


    # Enter a parse tree produced by GrammarParser#returnStat.
    def enterReturnStat(self, ctx:GrammarParser.ReturnStatContext):
        pass

    # Exit a parse tree produced by GrammarParser#returnStat.
    def exitReturnStat(self, ctx:GrammarParser.ReturnStatContext):
        pass


    # Enter a parse tree produced by GrammarParser#breakStat.
    def enterBreakStat(self, ctx:GrammarParser.BreakStatContext):
        pass

    # Exit a parse tree produced by GrammarParser#breakStat.
    def exitBreakStat(self, ctx:GrammarParser.BreakStatContext):
        pass


    # Enter a parse tree produced by GrammarParser#continueStat.
    def enterContinueStat(self, ctx:GrammarParser.ContinueStatContext):
        pass

    # Exit a parse tree produced by GrammarParser#continueStat.
    def exitContinueStat(self, ctx:GrammarParser.ContinueStatContext):
        pass


    # Enter a parse tree produced by GrammarParser#unnamedScopeStat.
    def enterUnnamedScopeStat(self, ctx:GrammarParser.UnnamedScopeStatContext):
        pass

    # Exit a parse tree produced by GrammarParser#unnamedScopeStat.
    def exitUnnamedScopeStat(self, ctx:GrammarParser.UnnamedScopeStatContext):
        pass


    # Enter a parse tree produced by GrammarParser#alias.
    def enterAlias(self, ctx:GrammarParser.AliasContext):
        pass

    # Exit a parse tree produced by GrammarParser#alias.
    def exitAlias(self, ctx:GrammarParser.AliasContext):
        pass


    # Enter a parse tree produced by GrammarParser#binExpr.
    def enterBinExpr(self, ctx:GrammarParser.BinExprContext):
        pass

    # Exit a parse tree produced by GrammarParser#binExpr.
    def exitBinExpr(self, ctx:GrammarParser.BinExprContext):
        pass


    # Enter a parse tree produced by GrammarParser#postUnaryExpr.
    def enterPostUnaryExpr(self, ctx:GrammarParser.PostUnaryExprContext):
        pass

    # Exit a parse tree produced by GrammarParser#postUnaryExpr.
    def exitPostUnaryExpr(self, ctx:GrammarParser.PostUnaryExprContext):
        pass


    # Enter a parse tree produced by GrammarParser#preUnaryExpr.
    def enterPreUnaryExpr(self, ctx:GrammarParser.PreUnaryExprContext):
        pass

    # Exit a parse tree produced by GrammarParser#preUnaryExpr.
    def exitPreUnaryExpr(self, ctx:GrammarParser.PreUnaryExprContext):
        pass


    # Enter a parse tree produced by GrammarParser#parensExpr.
    def enterParensExpr(self, ctx:GrammarParser.ParensExprContext):
        pass

    # Exit a parse tree produced by GrammarParser#parensExpr.
    def exitParensExpr(self, ctx:GrammarParser.ParensExprContext):
        pass


    # Enter a parse tree produced by GrammarParser#callExpr.
    def enterCallExpr(self, ctx:GrammarParser.CallExprContext):
        pass

    # Exit a parse tree produced by GrammarParser#callExpr.
    def exitCallExpr(self, ctx:GrammarParser.CallExprContext):
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
# Generated from Grammar.g4 by ANTLR 4.9.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\33")
        buf.write("K\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\3\2\6\2\16\n")
        buf.write("\2\r\2\16\2\17\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3")
        buf.write("\3\3\3\3\3\3\3\3\5\3 \n\3\3\4\3\4\3\4\3\4\3\4\3\4\3\4")
        buf.write("\3\4\3\4\5\4+\n\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4")
        buf.write("\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\7\4?\n\4\f\4\16\4")
        buf.write("B\13\4\3\5\3\5\3\6\3\6\3\6\5\6I\n\6\3\6\2\3\6\7\2\4\6")
        buf.write("\b\n\2\n\4\2\t\n\21\21\3\2\7\b\3\2\t\n\3\2\13\f\3\2\r")
        buf.write("\16\3\2\17\20\3\2\22\23\3\2\27\31\2S\2\r\3\2\2\2\4\37")
        buf.write("\3\2\2\2\6*\3\2\2\2\bC\3\2\2\2\nH\3\2\2\2\f\16\5\4\3\2")
        buf.write("\r\f\3\2\2\2\16\17\3\2\2\2\17\r\3\2\2\2\17\20\3\2\2\2")
        buf.write("\20\3\3\2\2\2\21\22\5\6\4\2\22\23\7\3\2\2\23 \3\2\2\2")
        buf.write("\24\25\5\n\6\2\25\26\7\32\2\2\26\27\7\4\2\2\27\30\5\6")
        buf.write("\4\2\30\31\7\3\2\2\31 \3\2\2\2\32\33\7\32\2\2\33\34\7")
        buf.write("\4\2\2\34\35\5\6\4\2\35\36\7\3\2\2\36 \3\2\2\2\37\21\3")
        buf.write("\2\2\2\37\24\3\2\2\2\37\32\3\2\2\2 \5\3\2\2\2!\"\b\4\1")
        buf.write("\2\"#\7\5\2\2#$\5\6\4\2$%\7\6\2\2%+\3\2\2\2&\'\t\2\2\2")
        buf.write("\'+\5\6\4\13(+\7\32\2\2)+\5\b\5\2*!\3\2\2\2*&\3\2\2\2")
        buf.write("*(\3\2\2\2*)\3\2\2\2+@\3\2\2\2,-\f\n\2\2-.\t\3\2\2.?\5")
        buf.write("\6\4\13/\60\f\t\2\2\60\61\t\4\2\2\61?\5\6\4\n\62\63\f")
        buf.write("\b\2\2\63\64\t\5\2\2\64?\5\6\4\t\65\66\f\7\2\2\66\67\t")
        buf.write("\6\2\2\67?\5\6\4\b89\f\6\2\29:\t\7\2\2:?\5\6\4\7;<\f\5")
        buf.write("\2\2<=\t\b\2\2=?\5\6\4\6>,\3\2\2\2>/\3\2\2\2>\62\3\2\2")
        buf.write("\2>\65\3\2\2\2>8\3\2\2\2>;\3\2\2\2?B\3\2\2\2@>\3\2\2\2")
        buf.write("@A\3\2\2\2A\7\3\2\2\2B@\3\2\2\2CD\t\t\2\2D\t\3\2\2\2E")
        buf.write("I\7\24\2\2FI\7\26\2\2GI\7\25\2\2HE\3\2\2\2HF\3\2\2\2H")
        buf.write("G\3\2\2\2I\13\3\2\2\2\b\17\37*>@H")
        return buf.getvalue()


class GrammarParser ( Parser ):

    grammarFileName = "Grammar.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "';'", "'='", "'('", "')'", "'*'", "'/'", 
                     "'+'", "'-'", "'>'", "'<'", "'=='", "'>='", "'<='", 
                     "'!='", "'!'", "'&&'", "'||'", "'char'", "'int'", "'float'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "MUL", "DIV", "ADD", "SUB", "GRT", "LST", 
                      "EQ", "GEQ", "LEQ", "NEQ", "NOT", "AND", "OR", "KEY_CHAR", 
                      "KEY_INT", "KEY_FLOAT", "CHAR", "INT", "FLOAT", "ID", 
                      "WS" ]

    RULE_prog = 0
    RULE_stat = 1
    RULE_expr = 2
    RULE_lit = 3
    RULE_prim = 4

    ruleNames =  [ "prog", "stat", "expr", "lit", "prim" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    MUL=5
    DIV=6
    ADD=7
    SUB=8
    GRT=9
    LST=10
    EQ=11
    GEQ=12
    LEQ=13
    NEQ=14
    NOT=15
    AND=16
    OR=17
    KEY_CHAR=18
    KEY_INT=19
    KEY_FLOAT=20
    CHAR=21
    INT=22
    FLOAT=23
    ID=24
    WS=25

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stat(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GrammarParser.StatContext)
            else:
                return self.getTypedRuleContext(GrammarParser.StatContext,i)


        def getRuleIndex(self):
            return GrammarParser.RULE_prog

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProg" ):
                listener.enterProg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProg" ):
                listener.exitProg(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProg" ):
                return visitor.visitProg(self)
            else:
                return visitor.visitChildren(self)




    def prog(self):

        localctx = GrammarParser.ProgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_prog)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 11 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 10
                self.stat()
                self.state = 13 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << GrammarParser.T__2) | (1 << GrammarParser.ADD) | (1 << GrammarParser.SUB) | (1 << GrammarParser.NOT) | (1 << GrammarParser.KEY_CHAR) | (1 << GrammarParser.KEY_INT) | (1 << GrammarParser.KEY_FLOAT) | (1 << GrammarParser.CHAR) | (1 << GrammarParser.INT) | (1 << GrammarParser.FLOAT) | (1 << GrammarParser.ID))) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return GrammarParser.RULE_stat

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ExprStatContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.StatContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(GrammarParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExprStat" ):
                listener.enterExprStat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExprStat" ):
                listener.exitExprStat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExprStat" ):
                return visitor.visitExprStat(self)
            else:
                return visitor.visitChildren(self)


    class InitStatContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.StatContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def prim(self):
            return self.getTypedRuleContext(GrammarParser.PrimContext,0)

        def ID(self):
            return self.getToken(GrammarParser.ID, 0)
        def expr(self):
            return self.getTypedRuleContext(GrammarParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInitStat" ):
                listener.enterInitStat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInitStat" ):
                listener.exitInitStat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInitStat" ):
                return visitor.visitInitStat(self)
            else:
                return visitor.visitChildren(self)


    class AssignStatContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.StatContext
            super().__init__(parser)
            self.lhs = None # Token
            self.rhs = None # ExprContext
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(GrammarParser.ID, 0)
        def expr(self):
            return self.getTypedRuleContext(GrammarParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignStat" ):
                listener.enterAssignStat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignStat" ):
                listener.exitAssignStat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignStat" ):
                return visitor.visitAssignStat(self)
            else:
                return visitor.visitChildren(self)



    def stat(self):

        localctx = GrammarParser.StatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_stat)
        try:
            self.state = 29
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                localctx = GrammarParser.ExprStatContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 15
                self.expr(0)
                self.state = 16
                self.match(GrammarParser.T__0)
                pass

            elif la_ == 2:
                localctx = GrammarParser.InitStatContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 18
                self.prim()
                self.state = 19
                self.match(GrammarParser.ID)
                self.state = 20
                self.match(GrammarParser.T__1)
                self.state = 21
                self.expr(0)
                self.state = 22
                self.match(GrammarParser.T__0)
                pass

            elif la_ == 3:
                localctx = GrammarParser.AssignStatContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 24
                localctx.lhs = self.match(GrammarParser.ID)
                self.state = 25
                self.match(GrammarParser.T__1)
                self.state = 26
                localctx.rhs = self.expr(0)
                self.state = 27
                self.match(GrammarParser.T__0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return GrammarParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class BinExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.op = None # Token
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GrammarParser.ExprContext)
            else:
                return self.getTypedRuleContext(GrammarParser.ExprContext,i)

        def MUL(self):
            return self.getToken(GrammarParser.MUL, 0)
        def DIV(self):
            return self.getToken(GrammarParser.DIV, 0)
        def ADD(self):
            return self.getToken(GrammarParser.ADD, 0)
        def SUB(self):
            return self.getToken(GrammarParser.SUB, 0)
        def GRT(self):
            return self.getToken(GrammarParser.GRT, 0)
        def LST(self):
            return self.getToken(GrammarParser.LST, 0)
        def EQ(self):
            return self.getToken(GrammarParser.EQ, 0)
        def GEQ(self):
            return self.getToken(GrammarParser.GEQ, 0)
        def LEQ(self):
            return self.getToken(GrammarParser.LEQ, 0)
        def NEQ(self):
            return self.getToken(GrammarParser.NEQ, 0)
        def OR(self):
            return self.getToken(GrammarParser.OR, 0)
        def AND(self):
            return self.getToken(GrammarParser.AND, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBinExpr" ):
                listener.enterBinExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBinExpr" ):
                listener.exitBinExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBinExpr" ):
                return visitor.visitBinExpr(self)
            else:
                return visitor.visitChildren(self)


    class UnaryExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(GrammarParser.ExprContext,0)

        def ADD(self):
            return self.getToken(GrammarParser.ADD, 0)
        def SUB(self):
            return self.getToken(GrammarParser.SUB, 0)
        def NOT(self):
            return self.getToken(GrammarParser.NOT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnaryExpr" ):
                listener.enterUnaryExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnaryExpr" ):
                listener.exitUnaryExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryExpr" ):
                return visitor.visitUnaryExpr(self)
            else:
                return visitor.visitChildren(self)


    class ParensExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(GrammarParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParensExpr" ):
                listener.enterParensExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParensExpr" ):
                listener.exitParensExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParensExpr" ):
                return visitor.visitParensExpr(self)
            else:
                return visitor.visitChildren(self)


    class LitExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.ExprContext
            super().__init__(parser)
            self.value = None # LitContext
            self.copyFrom(ctx)

        def lit(self):
            return self.getTypedRuleContext(GrammarParser.LitContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLitExpr" ):
                listener.enterLitExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLitExpr" ):
                listener.exitLitExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLitExpr" ):
                return visitor.visitLitExpr(self)
            else:
                return visitor.visitChildren(self)


    class IdExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.ExprContext
            super().__init__(parser)
            self.value = None # Token
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(GrammarParser.ID, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdExpr" ):
                listener.enterIdExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdExpr" ):
                listener.exitIdExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIdExpr" ):
                return visitor.visitIdExpr(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = GrammarParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 4
        self.enterRecursionRule(localctx, 4, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 40
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [GrammarParser.T__2]:
                localctx = GrammarParser.ParensExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 32
                self.match(GrammarParser.T__2)
                self.state = 33
                self.expr(0)
                self.state = 34
                self.match(GrammarParser.T__3)
                pass
            elif token in [GrammarParser.ADD, GrammarParser.SUB, GrammarParser.NOT]:
                localctx = GrammarParser.UnaryExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 36
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << GrammarParser.ADD) | (1 << GrammarParser.SUB) | (1 << GrammarParser.NOT))) != 0)):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 37
                self.expr(9)
                pass
            elif token in [GrammarParser.ID]:
                localctx = GrammarParser.IdExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 38
                localctx.value = self.match(GrammarParser.ID)
                pass
            elif token in [GrammarParser.CHAR, GrammarParser.INT, GrammarParser.FLOAT]:
                localctx = GrammarParser.LitExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 39
                localctx.value = self.lit()
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 62
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 60
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
                    if la_ == 1:
                        localctx = GrammarParser.BinExprContext(self, GrammarParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 42
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 43
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==GrammarParser.MUL or _la==GrammarParser.DIV):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 44
                        localctx.right = self.expr(9)
                        pass

                    elif la_ == 2:
                        localctx = GrammarParser.BinExprContext(self, GrammarParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 45
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 46
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==GrammarParser.ADD or _la==GrammarParser.SUB):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 47
                        localctx.right = self.expr(8)
                        pass

                    elif la_ == 3:
                        localctx = GrammarParser.BinExprContext(self, GrammarParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 48
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 49
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==GrammarParser.GRT or _la==GrammarParser.LST):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 50
                        localctx.right = self.expr(7)
                        pass

                    elif la_ == 4:
                        localctx = GrammarParser.BinExprContext(self, GrammarParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 51
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 52
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==GrammarParser.EQ or _la==GrammarParser.GEQ):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 53
                        localctx.right = self.expr(6)
                        pass

                    elif la_ == 5:
                        localctx = GrammarParser.BinExprContext(self, GrammarParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 54
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 55
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==GrammarParser.LEQ or _la==GrammarParser.NEQ):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 56
                        localctx.right = self.expr(5)
                        pass

                    elif la_ == 6:
                        localctx = GrammarParser.BinExprContext(self, GrammarParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 57
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 58
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==GrammarParser.AND or _la==GrammarParser.OR):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 59
                        localctx.right = self.expr(4)
                        pass

             
                self.state = 64
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class LitContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return GrammarParser.RULE_lit

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class PrimLitContext(LitContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.LitContext
            super().__init__(parser)
            self.lit_prim = None # Token
            self.copyFrom(ctx)

        def CHAR(self):
            return self.getToken(GrammarParser.CHAR, 0)
        def INT(self):
            return self.getToken(GrammarParser.INT, 0)
        def FLOAT(self):
            return self.getToken(GrammarParser.FLOAT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrimLit" ):
                listener.enterPrimLit(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrimLit" ):
                listener.exitPrimLit(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrimLit" ):
                return visitor.visitPrimLit(self)
            else:
                return visitor.visitChildren(self)



    def lit(self):

        localctx = GrammarParser.LitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_lit)
        self._la = 0 # Token type
        try:
            localctx = GrammarParser.PrimLitContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 65
            localctx.lit_prim = self._input.LT(1)
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << GrammarParser.CHAR) | (1 << GrammarParser.INT) | (1 << GrammarParser.FLOAT))) != 0)):
                localctx.lit_prim = self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return GrammarParser.RULE_prim

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class CharPrimContext(PrimContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.PrimContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def KEY_CHAR(self):
            return self.getToken(GrammarParser.KEY_CHAR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCharPrim" ):
                listener.enterCharPrim(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCharPrim" ):
                listener.exitCharPrim(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCharPrim" ):
                return visitor.visitCharPrim(self)
            else:
                return visitor.visitChildren(self)


    class FloatPrimContext(PrimContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.PrimContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def KEY_FLOAT(self):
            return self.getToken(GrammarParser.KEY_FLOAT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFloatPrim" ):
                listener.enterFloatPrim(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFloatPrim" ):
                listener.exitFloatPrim(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFloatPrim" ):
                return visitor.visitFloatPrim(self)
            else:
                return visitor.visitChildren(self)


    class IntPrimContext(PrimContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.PrimContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def KEY_INT(self):
            return self.getToken(GrammarParser.KEY_INT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIntPrim" ):
                listener.enterIntPrim(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIntPrim" ):
                listener.exitIntPrim(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIntPrim" ):
                return visitor.visitIntPrim(self)
            else:
                return visitor.visitChildren(self)



    def prim(self):

        localctx = GrammarParser.PrimContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_prim)
        try:
            self.state = 70
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [GrammarParser.KEY_CHAR]:
                localctx = GrammarParser.CharPrimContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 67
                self.match(GrammarParser.KEY_CHAR)
                pass
            elif token in [GrammarParser.KEY_FLOAT]:
                localctx = GrammarParser.FloatPrimContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 68
                self.match(GrammarParser.KEY_FLOAT)
                pass
            elif token in [GrammarParser.KEY_INT]:
                localctx = GrammarParser.IntPrimContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 69
                self.match(GrammarParser.KEY_INT)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[2] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 8)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 3)
         





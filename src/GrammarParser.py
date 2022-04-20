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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3%")
        buf.write("\\\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\3\2\6\2\16")
        buf.write("\n\2\r\2\16\2\17\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3")
        buf.write("\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\5\3\'\n")
        buf.write("\3\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4")
        buf.write("\5\4\66\n\4\3\4\5\49\n\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3")
        buf.write("\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\7\4M\n\4\f")
        buf.write("\4\16\4P\13\4\3\5\3\5\3\6\3\6\3\6\3\6\3\6\3\6\5\6Z\n\6")
        buf.write("\3\6\2\3\6\7\2\4\6\b\n\2\n\6\2\b\b\n\13\22\22\26\26\3")
        buf.write("\2\b\t\4\2\n\13\25\25\3\2\f\r\3\2\16\17\3\2\20\21\3\2")
        buf.write("\23\24\3\2 #\2j\2\r\3\2\2\2\4&\3\2\2\2\68\3\2\2\2\bQ\3")
        buf.write("\2\2\2\nY\3\2\2\2\f\16\5\4\3\2\r\f\3\2\2\2\16\17\3\2\2")
        buf.write("\2\17\r\3\2\2\2\17\20\3\2\2\2\20\3\3\2\2\2\21\22\5\6\4")
        buf.write("\2\22\23\7\3\2\2\23\'\3\2\2\2\24\25\7\35\2\2\25\26\5\n")
        buf.write("\6\2\26\27\7$\2\2\27\30\7\4\2\2\30\31\5\6\4\2\31\32\7")
        buf.write("\3\2\2\32\'\3\2\2\2\33\34\5\n\6\2\34\35\7$\2\2\35\36\7")
        buf.write("\4\2\2\36\37\5\6\4\2\37 \7\3\2\2 \'\3\2\2\2!\"\7$\2\2")
        buf.write("\"#\7\4\2\2#$\5\6\4\2$%\7\3\2\2%\'\3\2\2\2&\21\3\2\2\2")
        buf.write("&\24\3\2\2\2&\33\3\2\2\2&!\3\2\2\2\'\5\3\2\2\2()\b\4\1")
        buf.write("\2)*\7\5\2\2*+\5\6\4\2+,\7\6\2\2,9\3\2\2\2-.\t\2\2\2.")
        buf.write("9\5\6\4\f/9\7$\2\2\609\5\b\5\2\61\62\7\7\2\2\62\65\7\5")
        buf.write("\2\2\63\66\7$\2\2\64\66\5\b\5\2\65\63\3\2\2\2\65\64\3")
        buf.write("\2\2\2\66\67\3\2\2\2\679\7\6\2\28(\3\2\2\28-\3\2\2\28")
        buf.write("/\3\2\2\28\60\3\2\2\28\61\3\2\2\29N\3\2\2\2:;\f\13\2\2")
        buf.write(";<\t\3\2\2<M\5\6\4\f=>\f\n\2\2>?\t\4\2\2?M\5\6\4\13@A")
        buf.write("\f\t\2\2AB\t\5\2\2BM\5\6\4\nCD\f\b\2\2DE\t\6\2\2EM\5\6")
        buf.write("\4\tFG\f\7\2\2GH\t\7\2\2HM\5\6\4\bIJ\f\6\2\2JK\t\b\2\2")
        buf.write("KM\5\6\4\7L:\3\2\2\2L=\3\2\2\2L@\3\2\2\2LC\3\2\2\2LF\3")
        buf.write("\2\2\2LI\3\2\2\2MP\3\2\2\2NL\3\2\2\2NO\3\2\2\2O\7\3\2")
        buf.write("\2\2PN\3\2\2\2QR\t\t\2\2R\t\3\2\2\2SZ\7\32\2\2TZ\7\34")
        buf.write("\2\2UZ\7\33\2\2VZ\7\27\2\2WZ\7\30\2\2XZ\7\31\2\2YS\3\2")
        buf.write("\2\2YT\3\2\2\2YU\3\2\2\2YV\3\2\2\2YW\3\2\2\2YX\3\2\2\2")
        buf.write("Z\13\3\2\2\2\t\17&\658LNY")
        return buf.getvalue()


class GrammarParser ( Parser ):

    grammarFileName = "Grammar.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "';'", "'='", "'('", "')'", "'printf'", 
                     "'*'", "'/'", "'+'", "'-'", "'>'", "'<'", "'=='", "'>='", 
                     "'<='", "'!='", "'!'", "'&&'", "'||'", "'%'", "'&'", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "'char'", "'int'", 
                     "'float'", "'const'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "MUL", "DIV", "ADD", "SUB", 
                      "GRT", "LST", "EQ", "GEQ", "LEQ", "NEQ", "NOT", "AND", 
                      "OR", "MOD", "DRF", "KEY_CHARPTR", "KEY_FLOATPTR", 
                      "KEY_INTPTR", "KEY_CHAR", "KEY_INT", "KEY_FLOAT", 
                      "KEY_CONST", "MULTICOMMENT", "SINGLECOMMENT", "CHAR", 
                      "INT", "FLOAT", "BOOL", "ID", "WS" ]

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
    T__4=5
    MUL=6
    DIV=7
    ADD=8
    SUB=9
    GRT=10
    LST=11
    EQ=12
    GEQ=13
    LEQ=14
    NEQ=15
    NOT=16
    AND=17
    OR=18
    MOD=19
    DRF=20
    KEY_CHARPTR=21
    KEY_FLOATPTR=22
    KEY_INTPTR=23
    KEY_CHAR=24
    KEY_INT=25
    KEY_FLOAT=26
    KEY_CONST=27
    MULTICOMMENT=28
    SINGLECOMMENT=29
    CHAR=30
    INT=31
    FLOAT=32
    BOOL=33
    ID=34
    WS=35

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
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << GrammarParser.T__2) | (1 << GrammarParser.T__4) | (1 << GrammarParser.MUL) | (1 << GrammarParser.ADD) | (1 << GrammarParser.SUB) | (1 << GrammarParser.NOT) | (1 << GrammarParser.DRF) | (1 << GrammarParser.KEY_CHARPTR) | (1 << GrammarParser.KEY_FLOATPTR) | (1 << GrammarParser.KEY_INTPTR) | (1 << GrammarParser.KEY_CHAR) | (1 << GrammarParser.KEY_INT) | (1 << GrammarParser.KEY_FLOAT) | (1 << GrammarParser.KEY_CONST) | (1 << GrammarParser.CHAR) | (1 << GrammarParser.INT) | (1 << GrammarParser.FLOAT) | (1 << GrammarParser.BOOL) | (1 << GrammarParser.ID))) != 0)):
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


    class ConstInitStatContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.StatContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def KEY_CONST(self):
            return self.getToken(GrammarParser.KEY_CONST, 0)
        def prim(self):
            return self.getTypedRuleContext(GrammarParser.PrimContext,0)

        def ID(self):
            return self.getToken(GrammarParser.ID, 0)
        def expr(self):
            return self.getTypedRuleContext(GrammarParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConstInitStat" ):
                listener.enterConstInitStat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConstInitStat" ):
                listener.exitConstInitStat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConstInitStat" ):
                return visitor.visitConstInitStat(self)
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
            self.state = 36
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
                localctx = GrammarParser.ConstInitStatContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 18
                self.match(GrammarParser.KEY_CONST)
                self.state = 19
                self.prim()
                self.state = 20
                self.match(GrammarParser.ID)
                self.state = 21
                self.match(GrammarParser.T__1)
                self.state = 22
                self.expr(0)
                self.state = 23
                self.match(GrammarParser.T__0)
                pass

            elif la_ == 3:
                localctx = GrammarParser.InitStatContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 25
                self.prim()
                self.state = 26
                self.match(GrammarParser.ID)
                self.state = 27
                self.match(GrammarParser.T__1)
                self.state = 28
                self.expr(0)
                self.state = 29
                self.match(GrammarParser.T__0)
                pass

            elif la_ == 4:
                localctx = GrammarParser.AssignStatContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 31
                self.match(GrammarParser.ID)
                self.state = 32
                self.match(GrammarParser.T__1)
                self.state = 33
                localctx.rhs = self.expr(0)
                self.state = 34
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
        def MOD(self):
            return self.getToken(GrammarParser.MOD, 0)
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
        def MUL(self):
            return self.getToken(GrammarParser.MUL, 0)
        def DRF(self):
            return self.getToken(GrammarParser.DRF, 0)

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


    class PrintExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(GrammarParser.ID, 0)
        def lit(self):
            return self.getTypedRuleContext(GrammarParser.LitContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrintExpr" ):
                listener.enterPrintExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrintExpr" ):
                listener.exitPrintExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrintExpr" ):
                return visitor.visitPrintExpr(self)
            else:
                return visitor.visitChildren(self)


    class IdExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.ExprContext
            super().__init__(parser)
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
            self.state = 54
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [GrammarParser.T__2]:
                localctx = GrammarParser.ParensExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 39
                self.match(GrammarParser.T__2)
                self.state = 40
                self.expr(0)
                self.state = 41
                self.match(GrammarParser.T__3)
                pass
            elif token in [GrammarParser.MUL, GrammarParser.ADD, GrammarParser.SUB, GrammarParser.NOT, GrammarParser.DRF]:
                localctx = GrammarParser.UnaryExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 43
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << GrammarParser.MUL) | (1 << GrammarParser.ADD) | (1 << GrammarParser.SUB) | (1 << GrammarParser.NOT) | (1 << GrammarParser.DRF))) != 0)):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 44
                self.expr(10)
                pass
            elif token in [GrammarParser.ID]:
                localctx = GrammarParser.IdExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 45
                self.match(GrammarParser.ID)
                pass
            elif token in [GrammarParser.CHAR, GrammarParser.INT, GrammarParser.FLOAT, GrammarParser.BOOL]:
                localctx = GrammarParser.LitExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 46
                localctx.value = self.lit()
                pass
            elif token in [GrammarParser.T__4]:
                localctx = GrammarParser.PrintExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 47
                self.match(GrammarParser.T__4)
                self.state = 48
                self.match(GrammarParser.T__2)
                self.state = 51
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [GrammarParser.ID]:
                    self.state = 49
                    self.match(GrammarParser.ID)
                    pass
                elif token in [GrammarParser.CHAR, GrammarParser.INT, GrammarParser.FLOAT, GrammarParser.BOOL]:
                    self.state = 50
                    self.lit()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 53
                self.match(GrammarParser.T__3)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 76
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 74
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
                    if la_ == 1:
                        localctx = GrammarParser.BinExprContext(self, GrammarParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 56
                        if not self.precpred(self._ctx, 9):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 9)")
                        self.state = 57
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==GrammarParser.MUL or _la==GrammarParser.DIV):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 58
                        localctx.right = self.expr(10)
                        pass

                    elif la_ == 2:
                        localctx = GrammarParser.BinExprContext(self, GrammarParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 59
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 60
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << GrammarParser.ADD) | (1 << GrammarParser.SUB) | (1 << GrammarParser.MOD))) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 61
                        localctx.right = self.expr(9)
                        pass

                    elif la_ == 3:
                        localctx = GrammarParser.BinExprContext(self, GrammarParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 62
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 63
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==GrammarParser.GRT or _la==GrammarParser.LST):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 64
                        localctx.right = self.expr(8)
                        pass

                    elif la_ == 4:
                        localctx = GrammarParser.BinExprContext(self, GrammarParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 65
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 66
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==GrammarParser.EQ or _la==GrammarParser.GEQ):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 67
                        localctx.right = self.expr(7)
                        pass

                    elif la_ == 5:
                        localctx = GrammarParser.BinExprContext(self, GrammarParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 68
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 69
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==GrammarParser.LEQ or _la==GrammarParser.NEQ):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 70
                        localctx.right = self.expr(6)
                        pass

                    elif la_ == 6:
                        localctx = GrammarParser.BinExprContext(self, GrammarParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 71
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 72
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==GrammarParser.AND or _la==GrammarParser.OR):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 73
                        localctx.right = self.expr(5)
                        pass

             
                self.state = 78
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

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

        def BOOL(self):
            return self.getToken(GrammarParser.BOOL, 0)
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
            self.state = 79
            localctx.lit_prim = self._input.LT(1)
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << GrammarParser.CHAR) | (1 << GrammarParser.INT) | (1 << GrammarParser.FLOAT) | (1 << GrammarParser.BOOL))) != 0)):
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



    class FloatptrPrimContext(PrimContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.PrimContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def KEY_FLOATPTR(self):
            return self.getToken(GrammarParser.KEY_FLOATPTR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFloatptrPrim" ):
                listener.enterFloatptrPrim(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFloatptrPrim" ):
                listener.exitFloatptrPrim(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFloatptrPrim" ):
                return visitor.visitFloatptrPrim(self)
            else:
                return visitor.visitChildren(self)


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


    class CharptrPrimContext(PrimContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.PrimContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def KEY_CHARPTR(self):
            return self.getToken(GrammarParser.KEY_CHARPTR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCharptrPrim" ):
                listener.enterCharptrPrim(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCharptrPrim" ):
                listener.exitCharptrPrim(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCharptrPrim" ):
                return visitor.visitCharptrPrim(self)
            else:
                return visitor.visitChildren(self)


    class IntptrPrimContext(PrimContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.PrimContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def KEY_INTPTR(self):
            return self.getToken(GrammarParser.KEY_INTPTR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIntptrPrim" ):
                listener.enterIntptrPrim(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIntptrPrim" ):
                listener.exitIntptrPrim(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIntptrPrim" ):
                return visitor.visitIntptrPrim(self)
            else:
                return visitor.visitChildren(self)



    def prim(self):

        localctx = GrammarParser.PrimContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_prim)
        try:
            self.state = 87
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [GrammarParser.KEY_CHAR]:
                localctx = GrammarParser.CharPrimContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 81
                self.match(GrammarParser.KEY_CHAR)
                pass
            elif token in [GrammarParser.KEY_FLOAT]:
                localctx = GrammarParser.FloatPrimContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 82
                self.match(GrammarParser.KEY_FLOAT)
                pass
            elif token in [GrammarParser.KEY_INT]:
                localctx = GrammarParser.IntPrimContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 83
                self.match(GrammarParser.KEY_INT)
                pass
            elif token in [GrammarParser.KEY_CHARPTR]:
                localctx = GrammarParser.CharptrPrimContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 84
                self.match(GrammarParser.KEY_CHARPTR)
                pass
            elif token in [GrammarParser.KEY_FLOATPTR]:
                localctx = GrammarParser.FloatptrPrimContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 85
                self.match(GrammarParser.KEY_FLOATPTR)
                pass
            elif token in [GrammarParser.KEY_INTPTR]:
                localctx = GrammarParser.IntptrPrimContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 86
                self.match(GrammarParser.KEY_INTPTR)
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
                return self.precpred(self._ctx, 9)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 8)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 4)
         





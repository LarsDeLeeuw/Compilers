from antlr4 import *
if __name__ is not None and "." in __name__:
    from .GrammarParser import GrammarParser
else:
    from GrammarParser import GrammarParser

from AST import AST
from Nodes import *
from GrammarLexer import GrammarLexer
from GrammarVisitor import GrammarVisitor


class BuildASTVisitor(GrammarVisitor):

    def __init__(self):
        self.AST = AST()
        self.memory = {}

    def getAST(self):
        return self.AST

    # Visit a parse tree produced by GrammarParser#prog.
    def visitProg(self, ctx:GrammarParser.ProgContext):
        node = ProgNode()
        for Statement in ctx.stat():
            stat_node = self.visit(Statement)
            stat_node.setParent(node)
            node.StatementNodes.append(stat_node)
        self.AST.root = node
        return 0


    # Visit a parse tree produced by GrammarParser#exprStat.
    def visitExprStat(self, ctx:GrammarParser.ExprStatContext):
        return self.visit(ctx.expr())

    # Visit a parse tree produced by GrammarParser#initStat.
    def visitInitStat(self, ctx:GrammarParser.InitStatContext):
        if (ctx.ID().getText() in self.memory):
            return -1
        
        node = IdNode()
        
        node.ID = ctx.ID().getText()

        prim_node = self.visit(ctx.prim())
        prim_node.setParent(node)
        node.PrimitiveNode = prim_node


        lit_node = self.visit(ctx.expr())
        lit_node.setParent(node)
        node.LiteralNode = lit_node

        return node


    # Visit a parse tree produced by GrammarParser#assignStat.
    def visitAssignStat(self, ctx:GrammarParser.AssignStatContext):
        
        node = AssignNode()

        id_node = self.visit(ctx.lhs)
        id_node.setParent(node)
        node.IdNode = id_node

        lit_node = self.visit(ctx.rhs)
        lit_node.setParent(node)
        node.LiteralNode = lit_node

        return node


    # Visit a parse tree produced by GrammarParser#binExpr.
    def visitBinExpr(self, ctx:GrammarParser.BinExprContext):
        switcher = {
            GrammarLexer.ADD : AdditionNode(),
            GrammarLexer.SUB : SubstractionNode(),
            GrammarLexer.MUL : MultiplicationNode(),
            GrammarLexer.DIV : DivisionNode(),
            GrammarLexer.GRT : GreaterThanNode(),
            GrammarLexer.LST : LessThanNode(),
            GrammarLexer.EQ : IsEqualNode(),
            GrammarLexer.NEQ : IsNotEqualNode(),
            GrammarLexer.GEQ : GreaterOrEqualNode(),
            GrammarLexer.LEQ : LessOrEqualNode(),
            GrammarLexer.AND : AndNode(),
            GrammarLexer.OR : OrNode()
        }
        node = BinaryExpressionNode()
        
        node_lhs = self.visit(ctx.left)
        node_lhs.setParent(node)
        node.lhs = node_lhs

        node_rhs = self.visit(ctx.right)
        node_rhs.setParent(node)
        node.rhs = node_rhs

        node_op = switcher.get(ctx.op.type, None)
        node_op.setParent(node)
        node.op = node_op

        return node


    # Visit a parse tree produced by GrammarParser#unaryExpr.
    def visitUnaryExpr(self, ctx:GrammarParser.UnaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#parensExpr.
    def visitParensExpr(self, ctx:GrammarParser.ParensExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#litExpr.
    def visitLitExpr(self, ctx:GrammarParser.LitExprContext):
        return self.visit(ctx.value)

    # Visit a parse tree produced by GrammarParser#idExpr.
    def visitIdExpr(self, ctx:GrammarParser.IdExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#charLit.
    def visitPrimLit(self, ctx:GrammarParser.PrimLitContext):
        switcher = {
            GrammarLexer.CHAR  : CharNode(),
            GrammarLexer.INT   : IntegerNode(),
            GrammarLexer.FLOAT : FloatNode()
        }
        node = switcher.get(ctx.lit_prim.type, 'None')
        node.value = ctx.getText()
        # node.value not currently typetested
        return node


    # Visit a parse tree produced by GrammarParser#charPrim.
    def visitCharPrim(self, ctx:GrammarParser.CharPrimContext):
        return PrimitiveCharNode()


    # Visit a parse tree produced by GrammarParser#floatPrim.
    def visitFloatPrim(self, ctx:GrammarParser.FloatPrimContext):
        return PrimitiveFloatNode()


    # Visit a parse tree produced by GrammarParser#intFloat.
    def visitIntPrim(self, ctx:GrammarParser.IntPrimContext):
        return PrimitiveIntNode()



del GrammarParser
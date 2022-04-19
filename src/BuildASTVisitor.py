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
        self.serial = -1
    
    def claimSerial(self):
        self.serial += 1
        return self.serial

    def getAST(self):
        return self.AST

    # Visit a parse tree produced by GrammarParser#prog.
    def visitProg(self, ctx:GrammarParser.ProgContext):
        node = ProgNode()
        node.serial = self.claimSerial()
        for Statement in ctx.stat():
            # Create a container node for statement.
            statement_node = StatementNode()
            statement_node.setParent(node)
            statement_node.serial = self.claimSerial()

            stat_node = self.visit(Statement)
            stat_node.setParent(statement_node)
            stat_node.serial = self.claimSerial()

            statement_node.InnerNode = stat_node

            node.StatementNodes.append(statement_node)

        self.AST.root = node
        return 0


    # Visit a parse tree produced by GrammarParser#exprStat.
    def visitExprStat(self, ctx:GrammarParser.ExprStatContext):
        return self.visit(ctx.expr())

    # Visit a parse tree produced by GrammarParser#initStat.
    def visitInitStat(self, ctx:GrammarParser.InitStatContext):
        if (ctx.ID().getText() in self.memory):
            return -1
        
        print(ctx.start.line)
        node = IdNode()
        
        node.ID = ctx.ID().getText()

        prim_node = self.visit(ctx.prim())
        prim_node.setParent(node)
        prim_node.serial = self.claimSerial()
        node.PrimitiveNode = prim_node

        lit_node = self.visit(ctx.expr())
        lit_node.setParent(node)
        lit_node.serial = self.claimSerial()
        node.ExpressionNode = lit_node
        self.memory[node.ID] = ctx.expr()

        return node


    # Visit a parse tree produced by GrammarParser#assignStat.
    def visitAssignStat(self, ctx:GrammarParser.AssignStatContext):
        
        node = AssignNode()

        id_node = self.visit(ctx.lhs)
        id_node.setParent(node)
        id_node.serial = self.claimSerial()
        node.IdNode = id_node

        lit_node = self.visit(ctx.rhs)
        lit_node.setParent(node)
        lit_node.serial = self.claimSerial()
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
            GrammarLexer.OR : OrNode(),
            GrammarLexer.MOD : ModulusNode()
        }

        node = BinaryExpressionNode()
        
        node_lhs = self.visit(ctx.left)
        node_lhs.setParent(node)
        node_lhs.serial = self.claimSerial()
        node.lhs = node_lhs

        node_rhs = self.visit(ctx.right)
        node_rhs.setParent(node)
        node_rhs.serial = self.claimSerial()
        node.rhs = node_rhs

        node_op = switcher.get(ctx.op.type, None)
        node_op.setParent(node)
        node_op.serial = self.claimSerial()
        node.op = node_op

        return node


    # Visit a parse tree produced by GrammarParser#unaryExpr.
    def visitUnaryExpr(self, ctx:GrammarParser.UnaryExprContext):
        if (ctx.op.type == GrammarLexer.ADD):
            return self.visit(ctx.expr())
        else:
            node = NegateNode()
            node_expr = self.visit(ctx.expr())
            node_expr.serial = self.claimSerial()
            node_expr.setParent(node)
            node.InnerNode = node_expr
            node.serial = self.claimSerial()
            if ctx.op.type == GrammarLexer.NOT:
                node.boolean = True
            else:
                node.boolean = False
            return node
        


    # Visit a parse tree produced by GrammarParser#parensExpr.
    def visitParensExpr(self, ctx:GrammarParser.ParensExprContext):
        return self.visit(ctx.expr())


    # Visit a parse tree produced by GrammarParser#litExpr.
    def visitLitExpr(self, ctx:GrammarParser.LitExprContext):
        return self.visit(ctx.value)

    # Visit a parse tree produced by GrammarParser#idExpr.
    def visitIdExpr(self, ctx:GrammarParser.IdExprContext):
        if ctx.ID().getText() in self.memory:
            return self.visit(self.memory[ctx.ID().getText()])
        
        print("Use of undeclared identifier")
        return None


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
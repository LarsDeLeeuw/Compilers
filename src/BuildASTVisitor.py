from antlr4 import *
if __name__ is not None and "." in __name__:
    from .GrammarParser import GrammarParser
else:
    from GrammarParser import GrammarParser

from AST import AST
from STT import STT, STNode
from ASTNodes import *
from GrammarLexer import GrammarLexer
from GrammarVisitor import GrammarVisitor


class BuildASTVisitor(GrammarVisitor):

    def __init__(self):
        self.AST = AST()
        self.STT = STT()
        self.currentST = STNode()
        self.STT.root = self.currentST
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
        # TODO: Process include header(s)
        # print(ctx.LIB()[0].getText())
        for Decl in ctx.decl():
            decl_node = self.visit(Decl)
            decl_node.parent = node
            node.children.append(decl_node)
        self.AST.root = node
        return 0


    # Visit a parse tree produced by GrammarParser#varDecl.
    def visitVarDecl(self, ctx:GrammarParser.VarDeclContext):
        node = VarDeclNode()
        node.id = ctx.ID().getText()
        node.line = ctx.start.line
        node.type = ctx.prim().getText()
        if(ctx.expr() is None):
            pass
        else:
            node.init_expr = self.visit(ctx.expr())
            node.init = True
        return node


    # Visit a parse tree produced by GrammarParser#funcheadsupDecl.
    def visitFuncheadsupDecl(self, ctx:GrammarParser.FuncheadsupDeclContext):
        node = FunctionDeclNode()
        node.line = ctx.start.line
        if(ctx.KEY_VOID() is None):
            node.return_type = ctx.prim()[0].getText()
        node.id = ctx.ID()[0].getText()
        if(len(ctx.prim()) > 1):
            for i in range(len(ctx.prim())-1):
                parm_type = ctx.prim()[i+1].getText()
                parm_id = ctx.ID()[i+1].getText()
                node.signature.append(parm_type)
                parm_var = ParmVarDeclNode()
                parm_var.type = parm_type
                parm_var.id = parm_id
                node.children.append(parm_var)

        return node


    # Visit a parse tree produced by GrammarParser#funcDecl.
    def visitFuncDecl(self, ctx:GrammarParser.FuncDeclContext):
        node = FunctionDeclNode()
        node.line = ctx.start.line
        if(ctx.KEY_VOID() is None):
            node.return_type = ctx.prim()[0].getText()
        node.id = ctx.ID()[0].getText()
        if(len(ctx.prim()) > 1):
            for i in range(len(ctx.prim())-1):
                parm_type = ctx.prim()[i+1].getText()
                parm_id = ctx.ID()[i+1].getText()
                node.signature.append(parm_type)
                parm_var = ParmVarDeclNode()
                parm_var.type = parm_type
                parm_var.id = parm_id
                parm_var.parent = node
                node.children.append(parm_var)
        
        scope_node = ScopeStmtNode()
        scope_node.parent = node
        for Statement in ctx.stat():
            stat_node = self.visit(Statement)
            stat_node.parent = scope_node
            scope_node.children.append(stat_node)
        
        node.children.append(scope_node)
        return node


    # Visit a parse tree produced by GrammarParser#exprStat.
    def visitExprStat(self, ctx:GrammarParser.ExprStatContext):
        node = self.visit(ctx.expr())
        return node

    # Visit a parse tree produced by GrammarParser#declStat.
    def visitDeclStat(self, ctx:GrammarParser.DeclStatContext):
        node = DeclStmtNode()
        var_decl = VarDeclNode()
        var_decl.parent = node
        var_decl.id = ctx.ID().getText()
        var_decl.line = ctx.start.line
        node.line = var_decl.line
        var_decl.type = ctx.prim().getText()
        if(ctx.expr() is None):
            pass
        else:
            var_decl.init_expr = self.visit(ctx.expr())
            var_decl.init = True
        node.child = var_decl
        return node


    # Visit a parse tree produced by GrammarParser#whileStat.
    def visitWhileStat(self, ctx:GrammarParser.WhileStatContext):
        node = WhileStmtNode()
        return node


    # Visit a parse tree produced by GrammarParser#ifStat.
    def visitIfStat(self, ctx:GrammarParser.IfStatContext):
        node = IfStmtNode()
        return node


    # Visit a parse tree produced by GrammarParser#returnStat.
    def visitReturnStat(self, ctx:GrammarParser.ReturnStatContext):
        node = ReturnStmtNode()
        return node


    # Visit a parse tree produced by GrammarParser#binExpr.
    def visitBinExpr(self, ctx:GrammarParser.BinExprContext):
        node = BinExprNode()
        switcher = {
            GrammarLexer.ADD : "+",
            GrammarLexer.SUB : "-",
            GrammarLexer.MUL : "*",
            GrammarLexer.DIV : "/",
            GrammarLexer.GRT : ">",
            GrammarLexer.LST : "<",
            GrammarLexer.EQ : "==",
            GrammarLexer.NEQ : "!=",
            GrammarLexer.GEQ : ">=",
            GrammarLexer.LEQ : "<=",
            GrammarLexer.AND : "&&",
            GrammarLexer.OR : "||",
            GrammarLexer.MOD : "%",
            GrammarLexer.ASS : "="
        }
        # TODO: Op compatible with lhs and rhs?
        #       Expected type?
        node.operation = switcher.get(ctx.op.type, None)
        node.type = "int"
        lhs_node = self.visit(ctx.left)
        lhs_node.parent = node
        rhs_node = self.visit(ctx.right)
        rhs_node.parent = node

        node.lhs_child = lhs_node
        node.rhs_child = rhs_node
        return node


    # Visit a parse tree produced by GrammarParser#unaryExpr.
    def visitUnaryExpr(self, ctx:GrammarParser.UnaryExprContext):
        node = UnaryExprNode()
        return node


    # Visit a parse tree produced by GrammarParser#parensExpr.
    def visitParensExpr(self, ctx:GrammarParser.ParensExprContext):
        return self.visit(ctx.expr())


    # Visit a parse tree produced by GrammarParser#callExpr.
    def visitCallExpr(self, ctx:GrammarParser.CallExprContext):
        node = CallExprNode()
        return node


    # Visit a parse tree produced by GrammarParser#litExpr.
    def visitLitExpr(self, ctx:GrammarParser.LitExprContext):
        node = LiteralNode()
        return node


    # Visit a parse tree produced by GrammarParser#idExpr.
    def visitIdExpr(self, ctx:GrammarParser.IdExprContext):
        node = DeclRefExprNode()
        return node


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
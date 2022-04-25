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
import copy


class BuildASTVisitor(GrammarVisitor):

    def __init__(self):
        self.AST = AST()
        self.STT = STT()
        self.currentST = None
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

        # Create 'global' SymbolTree
        self.currentST = STNode()
        self.STT.root = self.currentST
        self.AST.stt = self.STT
        store_refST = self.currentST     

        if len(ctx.LIB()) > 0:
            if ctx.LIB()[0].getText() == "<stdio.h>":
                node.includes["<stdio.h>"] = ["declare dso_local i32 @printf(i8*, ...)\n"]
                dummy_node = FunctionDeclNode()
                dummy_node.init = True
                dummy_node.id = "printf"
                dummy_node.included = True
                dummy_node.symboltable = self.currentST
                (idIsOk, idIndex) = self.checkCurrentST("printf")
                if idIsOk:
                    self.currentST.symbols["printf"] = [idIndex, dummy_node, copy.deepcopy(dummy_node)]
   
        for Decl in ctx.decl():
            self.currentST = store_refST
            decl_node = self.visit(Decl)
            decl_node.parent = node
            node.children.append(decl_node)
        node.symboltable = store_refST
        self.AST.root = node
        return 0

    def checkCurrentST(self, id):

        if id in self.currentST.symbols:
            return (False, 0)
        index = self.currentST.index
        self.currentST.index += 1
        return (True, index)

    def findST(self, id):
        lookST = self.currentST

        while not lookST is None:
            if id in lookST.symbols:
                return (True, lookST.symbols[id])
            lookST = lookST.parent
        
        return (False, None)


    # Visit a parse tree produced by GrammarParser#varDecl.
    def visitVarDecl(self, ctx:GrammarParser.VarDeclContext):
        node = VarDeclNode()
        node.id = ctx.ID().getText()
        node.line = ctx.start.line
        node.type = ctx.prim().getText()

        if ctx.INT() is None:
            node.array = False
        else:
            node.array = True
            node.len = int(ctx.INT().getText())

        if len(ctx.expr()) == 0:
            node.init = False
        else:
            if node.array:
                init_list_node = InitListExprNode()
                init_list_node.parent = node
                # Check if supplied init array is same len as array
                if node.len != len(ctx.expr()):
                    raise Exception("Array initialised with incorrect amount of elements")
                for Expr in ctx.expr():
                    expr_node = self.visit(Expr)
                    expr_node.parent = init_list_node
                    init_list_node.children.append(expr_node)
                node.init = True
                node.init_expr = init_list_node
            else:
                node.init_expr = self.visit(ctx.expr()[0])
                node.init_expr.parent = node
                node.init = True

        (idIsOk, idIndex) = self.checkCurrentST(node.id)
        if idIsOk:
            self.currentST.symbols[node.id] = [idIndex, node, copy.deepcopy(node)]

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
        node.init = True
        node.id = ctx.ID()[0].getText()

        # Create SymbolTable for function
        newST = STNode()
        newST.parent = self.currentST
        self.currentST.children.append(newST)
        store_refST = self.currentST
        self.currentST = newST

        if(ctx.KEY_VOID() is None):
            node.return_type = ctx.prim()[0].getText()
        if(len(ctx.prim()) > 1):
            for i in range(len(ctx.prim())-1):
                parm_type = ctx.prim()[i+1].getText()
                parm_id = ctx.ID()[i+1].getText()
                node.arg_types.append(parm_type)
                parm_var = ParmVarDeclNode()
                parm_var.type = parm_type
                parm_var.id = parm_id
                parm_var.parent = node
                node.children.append(parm_var)
        
        for Parm in node.children:
            (idIsOk, idIndex) = self.checkCurrentST(Parm.id)
            if idIsOk:
                self.currentST.symbols[Parm.id] = [idIndex, Parm, copy.deepcopy(Parm)]

        scope_node = ScopeStmtNode()
        scope_node.parent = node
        store_thisST = self.currentST
        for Statement in ctx.stat():
            self.currentST = store_thisST
            stat_node = self.visit(Statement)
            stat_node.parent = scope_node
            scope_node.children.append(stat_node)
        
        scope_node.symboltable = store_thisST
        node.children.append(scope_node)

        self.currentST = store_refST
        (idIsOk, idIndex) = self.checkCurrentST(node.id)
        if idIsOk:
            self.currentST.symbols[node.id] = [idIndex, node, copy.deepcopy(node)]
        return node


    # Visit a parse tree produced by GrammarParser#exprStat.
    def visitExprStat(self, ctx:GrammarParser.ExprStatContext):
        node = ExprStmtNode()
        expr_node = self.visit(ctx.expr())
        expr_node.parent = node
        node.child = expr_node
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

        if ctx.INT() is None:
            var_decl.array = False
        else:
            var_decl.array = True
            var_decl.len = int(ctx.INT().getText())

        if len(ctx.expr()) == 0:
            var_decl.init = False
        else:
            if var_decl.array:
                init_list_node = InitListExprNode()
                init_list_node.parent = var_decl
                # Check if supplied init array is same len as array
                if var_decl.len != len(ctx.expr()):
                    raise Exception("Array initialised with incorrect amount of elements")
                for Expr in ctx.expr():
                    expr_node = self.visit(Expr)
                    expr_node.parent = init_list_node
                    init_list_node.children.append(expr_node)
                var_decl.init = True
                var_decl.init_expr = init_list_node
            else:
                var_decl.init_expr = self.visit(ctx.expr()[0])
                var_decl.init_expr.parent = var_decl
                var_decl.init = True
                if var_decl.type == var_decl.init_expr.type:
                    pass
                else:
                    cast_node = ImplicitCastExprNode()
                    cast_node.parent = var_decl
                    cast_node.type = var_decl.type
                    cast_node.cast = var_decl.init_expr
                    var_decl.init_expr = cast_node

        node.child = var_decl

        (idIsOk, idIndex) = self.checkCurrentST(var_decl.id)
        if idIsOk:
            self.currentST.symbols[var_decl.id] = [idIndex, var_decl, copy.deepcopy(var_decl)]


        return node


    # Visit a parse tree produced by GrammarParser#whileStat.
    def visitWhileStat(self, ctx:GrammarParser.WhileStatContext):
        node = WhileStmtNode()
        return node


    # Visit a parse tree produced by GrammarParser#ifStat.
    def visitIfStat(self, ctx:GrammarParser.IfStatContext):
        node = IfStmtNode()
        cond_node = self.visit(ctx.expr())
        cond_node.parent = node
        node.children.append(cond_node)

        # Create SymbolTable for ifblock
        newST = STNode()
        newST.parent = self.currentST
        self.currentST.children.append(newST)
        store_refST = self.currentST
        self.currentST = newST

        if_scope = ScopeStmtNode()
        if_scope.parent = node
        store_ifST = newST
        for Statement in ctx.stat():
            self.currentST = store_ifST
            stat_node = self.visit(Statement)
            stat_node.parent = if_scope
            if_scope.children.append(stat_node)
        node.children.append(if_scope)

        self.currentST = store_refST

        if ctx.KEY_ELSE() is None:
            pass
        else:
             # Create SymbolTable for fblock
            newST = STNode()
            newST.parent = self.currentST
            self.currentST.children.append(newST)
            self.currentST = newST

            node.has_else = True
            else_scope = ScopeStmtNode()
            else_scope.parent = node
            store_elseST = newST
            for Statement in ctx.alias().stat():
                self.currentST = store_elseST
                stat_node = self.visit(Statement)
                stat_node.parent = else_scope
                else_scope.children.append(stat_node)
            node.children.append(else_scope)
            self.currentST = store_refST

        return node


    # Visit a parse tree produced by GrammarParser#returnStat.
    def visitReturnStat(self, ctx:GrammarParser.ReturnStatContext):
        node = ReturnStmtNode()
        if ctx.expr() is None:
            raise Exception("Return of empty expr not supported")
        return_expr = self.visit(ctx.expr())
        return_expr.parent = node
        node.child = return_expr
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
        if node.operation == "=":
            try:
                ref_id = ctx.left.ID().getText()
                (IdDecl, Ref) = self.findST(ref_id)
                if(IdDecl):
                    Ref[1].init = True
                    expr_node = self.visit(ctx.right)
                    expr_node.parent = Ref[1]
                    Ref[2].init = True
                    Ref[2].init_expr = expr_node
                    node.lhs_child = DeclRefExprNode()
                    node.lhs_child.symboltable = self.currentST
                    node.lhs_child.parent = node
                    node.lhs_child.ref = Ref[2]
                    node.lhs_child.id = ref_id
                    if Ref[2].type == expr_node.type:
                        node.rhs_child = expr_node
                    else:
                        cast_node = ImplicitCastExprNode()
                        cast_node.parent = node
                        cast_node.type = Ref[2].type
                        cast_node.cast = expr_node
                        node.rhs_child = cast_node
                else:
                    print("Undeclared ID")

                return node
            except AttributeError:
                print("caught")
        else:    
            lhs_node = self.visit(ctx.left)
            lhs_node.parent = node
            rhs_node = self.visit(ctx.right)
            rhs_node.parent = node

            node.lhs_child = lhs_node
            node.rhs_child = rhs_node
            if node.operation == "&&" or node.operation == "||" or node.operation == "!=":
                node.type = 'int'
            elif node.operation == ">" or node.operation == "<" or node.operation == ">=" or node.operation == "<=":
                node.type = 'int'
            else:
                node.type = node.lhs_child.type
            return node


    # Visit a parse tree produced by GrammarParser#unaryExpr.
    def visitUnaryExpr(self, ctx:GrammarParser.UnaryExprContext):
        node = UnaryExprNode()
        switcher = {
            GrammarLexer.ADD : "+",
            GrammarLexer.SUB : "-",
            GrammarLexer.NOT : "!",
            GrammarLexer.DRF : "&",
            GrammarLexer.MUL : "*"
        }
        expr_node = self.visit(ctx.expr())
        expr_node.parent = node
        node.operation = switcher.get(ctx.op.type, None)
        if node.operation == "!":
                node.type = 'int'
        else:
                node.type = node.child.type
        node.child = expr_node
        return node


    # Visit a parse tree produced by GrammarParser#parensExpr.
    def visitParensExpr(self, ctx:GrammarParser.ParensExprContext):
        return self.visit(ctx.expr())


    # Visit a parse tree produced by GrammarParser#callExpr.
    def visitCallExpr(self, ctx:GrammarParser.CallExprContext):
        node = CallExprNode()
        call_id = ctx.ID().getText()
        node.line = ctx.start.line
        (IdDecl, Ref) = self.findST(call_id)
        if(IdDecl):
            node.children.append(Ref[1])
        
        for arg in ctx.expr():
            arg_node = self.visit(arg)
            arg_node.parent = node
            node.children.append(arg_node)

        return node


    # Visit a parse tree produced by GrammarParser#litExpr.
    def visitLitExpr(self, ctx:GrammarParser.LitExprContext):
        return self.visit(ctx.value)


    # Visit a parse tree produced by GrammarParser#idExpr.
    def visitIdExpr(self, ctx:GrammarParser.IdExprContext):
        node = DeclRefExprNode()
        node.symboltable = self.currentST

        (IdDecl, Ref) = self.findST(ctx.ID().getText())
        if(IdDecl):
            node.ref = Ref[2]
            Ref[1].used = True
            node.id = Ref[1].id
            node.type = Ref[1].type
        else:
            print("undeclared idvisited")

        return node

    # Visit a parse tree produced by GrammarParser#primLit.
    def visitPrimLit(self, ctx:GrammarParser.PrimLitContext):

        if ctx.lit_prim.type == GrammarLexer.CHAR:
            node = CharacterLiteralNode()
            node.setValue(ctx.getText()[1:-1])
        elif ctx.lit_prim.type == GrammarLexer.INT:
            node = IntergerLiteralNode()
            node.setValue(ctx.getText())
        elif ctx.lit_prim.type == GrammarLexer.FLOAT:
            node = FloatingLiteralNode()
            node.setValue(ctx.getText())
        elif ctx.lit_prim.type == GrammarLexer.STRING:
            node = StringLiteralNode()
            node.setValue(ctx.getText())
        else:
            node = AbstractNode()

        return node


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
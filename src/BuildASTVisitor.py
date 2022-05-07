from antlr4 import *
if __name__ is not None and "." in __name__:
    from .GrammarParser import GrammarParser
else:
    from GrammarParser import GrammarParser

from AST import AST
from STT import STT
from ASTNodes import *
from GrammarLexer import GrammarLexer
from GrammarVisitor import GrammarVisitor
import copy


class BuildASTVisitor(GrammarVisitor):

    def __init__(self):
        self.AST = AST()
        self.STT = STT()
        self.serial = -1
    
    def claimSerial(self):
        self.serial += 1
        return self.serial

    def getAST(self):
        return self.AST

    def getSTT(self):
        return self.STT

        # Visit a parse tree produced by GrammarParser#prog.
    def visitProg(self, ctx:GrammarParser.ProgContext):
        node = ProgNode()
        # Create 'global' SymbolTree
        self.STT.new_scope()

        if len(ctx.LIB()) > 0:
            if ctx.LIB()[0].getText() == "<stdio.h>":
                node.includes["<stdio.h>"] = ["declare dso_local i32 @printf(i8*, ...)\n"]
                dummy_node = FunctionDeclNode()
                dummy_node.init = True
                dummy_node.id = "printf"
                dummy_node.included = True
                dummy_node.return_type = "void"
                result = self.STT.insert("printf")
                if result is None:
                    raise Exception("Failed to insert library function in symboltable")
                else:
                    self.STT.set_attribute("printf", "ast_node", dummy_node)
                    self.STT.set_attribute("printf", "object", "Function")

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

        if ctx.KEY_CONST() is None:
            node.const = False
        else:
            node.const = True

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
                init_list_node.type = node.type
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

        result = self.STT.insert(node.id)
        if result is None:
            raise Exception("Failed to insert {} in symboltable".format(node.id))
        else:
            self.STT.set_attribute(node.id, "ast_node", node)
            self.STT.set_attribute(node.id, "object", "lvalue Var")
            self.STT.set_attribute(node.id, "global", True)
            self.STT.set_attribute(node.id, "serial", self.claimSerial())

        
        return node


    # Visit a parse tree produced by GrammarParser#funcheadsupDecl.
    def visitFuncheadsupDecl(self, ctx:GrammarParser.FuncheadsupDeclContext):
        # TODO
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
        self.STT.new_scope()

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
        
        for parmvar_node in node.children:
            result = self.STT.insert(parmvar_node.id)
            if result is None:
                raise Exception("Failed to insert ParmVar '{}' in symboltable".format(parmvar_node.id))
            else:
                self.STT.set_attribute(parmvar_node.id, "ast_node", parmvar_node)
                self.STT.set_attribute(parmvar_node.id, "object", "lvalue ParmVar")
                self.STT.set_attribute(parmvar_node.id, "serial", self.claimSerial())
  

        scope_node = ScopeStmtNode()
        scope_node.parent = node
        for Statement in ctx.stat():
            stat_node = self.visit(Statement)
            stat_node.parent = scope_node
            scope_node.children.append(stat_node)
        
        node.children.append(scope_node)
        
        # Go back to scope where Function was declared
        self.STT.prev_scope()

        result = self.STT.insert(node.id)
        if result is None:
            raise Exception("Failed to insert Function '{}' in symboltable".format(node.id))
        else:
            self.STT.set_attribute(node.id, "ast_node", node)
            self.STT.set_attribute(node.id, "object", "Function")

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

        if ctx.KEY_CONST() is None:
            var_decl.const = False
        else:
            var_decl.const = True

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

        result = self.STT.insert(node.child.id)
        if result is None:
            raise Exception("Failed to insert Var '{}' in symboltable".format(node.child.id))
        else:
            self.STT.set_attribute(node.child.id, "ast_node", node.child)
            self.STT.set_attribute(node.child.id, "object", "lvalue Var")
            self.STT.set_attribute(node.child.id, "global", False)
            self.STT.set_attribute(node.child.id, "serial", self.claimSerial())
        
        return node


    # Visit a parse tree produced by GrammarParser#whileStat.
    def visitWhileStat(self, ctx:GrammarParser.WhileStatContext):
        # TODO
        node = WhileStmtNode()
        return node

    # Visit a parse tree produced by GrammarParser#ifStat.
    def visitIfStat(self, ctx:GrammarParser.IfStatContext):
        node = IfStmtNode()
        node.line = ctx.start.line
        cond_node = self.visit(ctx.expr())
        cond_node.parent = node
        node.children.append(cond_node)

        # Create SymbolTable for ifblock
        self.STT.new_scope()

        if_scope = ScopeStmtNode()
        if_scope.parent = node
        for Statement in ctx.stat():
            stat_node = self.visit(Statement)
            stat_node.parent = if_scope
            if_scope.children.append(stat_node)
        node.children.append(if_scope)

        # Return to symboltable where if statement declared
        self.STT.prev_scope()

        if ctx.KEY_ELSE() is None:
            pass
        else:
             # Create SymbolTable for fblock
            self.STT.new_scope()

            node.has_else = True
            else_scope = ScopeStmtNode()
            else_scope.parent = node
            for Statement in ctx.alias().stat():
                stat_node = self.visit(Statement)
                stat_node.parent = else_scope
                else_scope.children.append(stat_node)
            node.children.append(else_scope)
            # Return to symboltable where else statement declared
            self.STT.prev_scope()

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

    # Visit a parse tree produced by GrammarParser#breakStat.
    def visitBreakStat(self, ctx:GrammarParser.BreakStatContext):
        node = BreakStmtNode()
        node.line = ctx.start.line
        return node

    # Visit a parse tree produced by GrammarParser#continueStat.
    def visitContinueStat(self, ctx:GrammarParser.ContinueStatContext):
        node = ContinueStmtNode()
        node.line = ctx.start.line
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
        node.line = ctx.start.line 
        if node.operation == "=":
            lhs_id = ctx.left.ID()[0].getText()
            result = self.STT.lookup(lhs_id)
            if result is None:
                raise Exception("Referenced ID {} not found in symboltable".format(lhs_id))
            else:
                if result["object"] != "Function":
                    result["ast_node"].used = True
                    if result["ast_node"].array:
                        array_node = self.visit(ctx.left)
                        array_node.parent = node
                        # array_node = ArraySubscriptExprNode()
                        # array_node.parent = node
                        # array_node.type = result["ast_node"].type
                        # array_node.array_child = result
                        # if ctx.left.INT() is None:
                        #     array_node.index_child = self.visit(ctx.left.ID()[1])
                        # else:
                        #     array_node.index_child = self.visit(ctx.left.INT())
                        node.lhs_child = array_node

                        expr_node = self.visit(ctx.right)
                        if expr_node.type == array_node.type:
                            expr_node.parent = node
                            node.rhs_child = expr_node
                        else:
                            cast_node = ImplicitCastExprNode()
                            cast_node.parent = node
                            cast_node.type = ref_node.type
                            cast_node.cast = expr_node
                            expr_node.parent = cast_node
                            node.rhs_child = cast_node

                        return node
                    else:
                        ref_node = DeclRefExprNode()
                        ref_node.ref = result
                        ref_node.id = lhs_id
                        ref_node.type = result["ast_node"].type
                        ref_node.parent = node
                        node.lhs_child = ref_node

                        expr_node = self.visit(ctx.right)
                        if expr_node.type == ref_node.type:
                            expr_node.parent = node
                            node.rhs_child = expr_node
                        else:
                            cast_node = ImplicitCastExprNode()
                            cast_node.parent = node
                            cast_node.type = ref_node.type
                            cast_node.cast = expr_node
                            expr_node.parent = cast_node
                            node.rhs_child = cast_node
                        return node
                else:
                    raise Exception("Semantics blahblah 328 buildast")         
        else:    
            lhs_node = self.visit(ctx.left)
            lhs_node.parent = node
            rhs_node = self.visit(ctx.right)
            rhs_node.parent = node

            node.lhs_child = lhs_node
            node.rhs_child = rhs_node
            if node.operation == "&&" or node.operation == "||" or node.operation == "!=" or node.operation == "==":
                node.type = 'bool'
            elif node.operation == ">" or node.operation == "<" or node.operation == ">=" or node.operation == "<=":
                node.type = 'bool'
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
        node.child = expr_node
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

        result = self.STT.lookup(call_id)
        if result is None:
            raise Exception("Function {} not found in symboltable".format(call_id))
        else:
            functionref_node = DeclRefExprNode()
            functionref_node.parent = node
            functionref_node.ref = result
            functionref_node.id = result["ast_node"].id
            functionref_node.type = result["ast_node"].return_type
            functionref_node.function = True
            functionref_node.signature = result["ast_node"].getSignature()
            node.children.append(functionref_node)
   
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
        call_id = ctx.ID()[0].getText()
        if ctx.INT() is None and len(ctx.ID()) == 1:
            result = self.STT.lookup(call_id)
            if result is None:
                raise Exception("Referenced ID {} not found in symboltable".format(call_id))
            else:
                node.id = result["ast_node"].id
                node.ref = result
                if result["object"] == "Function":
                    node.type = result["ast_node"].return_type
                    node.function = True
                    node.signature = result["ast_node"].getSignature()
                else:
                    node.type = result["ast_node"].type
                node.ref["ast_node"].used = True
        else:
            if ctx.INT() is None:
                node = ArraySubscriptExprNode()
                result = self.STT.lookup(call_id)
                if result is None:
                    raise Exception("Referenced ID {} not found in symboltable".format(call_id))
                else:
                    node.array_child = result
                    node.type = result["ast_node"].type
                    node.index_child = self.visit(ctx.ID()[1])
                    node.index_child.parent = node
            else:
                node = ArraySubscriptExprNode()
                result = self.STT.lookup(call_id)
                if result is None:
                    raise Exception("Referenced ID {} not found in symboltable".format(call_id))
                else:
                    node.array_child = result
                    node.type = result["ast_node"].type
                    node.index_child = IntergerLiteralNode()
                    node.index_child.setValue(ctx.INT().getText())
                    node.index_child.parent = node
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
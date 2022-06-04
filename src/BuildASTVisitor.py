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
                dummy_node.type = "void"
                result = self.STT.insert("printf")
                if result is None:
                    raise Exception("Failed to insert library function in symboltable")
                else:
                    self.STT.set_attribute("printf", "ast_node", dummy_node)
                    self.STT.set_attribute("printf", "object", "Function")
                node.includes["<stdio.h>"] += ["declare i32 @__isoc99_scanf(i8*, ...)\n"]
                dummy_node = FunctionDeclNode()
                dummy_node.init = True
                dummy_node.id = "scanf"
                dummy_node.included = True
                dummy_node.type = "void"
                result = self.STT.insert("scanf")
                if result is None:
                    raise Exception("Failed to insert library function in symboltable")
                else:
                    self.STT.set_attribute("scanf", "ast_node", dummy_node)
                    self.STT.set_attribute("scanf", "object", "Function")

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
        node.column = ctx.start.column

        if ctx.KEY_CONST() is None:
            node.const = False
        else:
            node.const = True
        
        temp = ctx.prim().getText().split('*')
        node.type = temp[0]
        if len(temp) >= 2:
            node.type += " "
            node.type += (len(temp)-1)*"*"

        if ctx.INT() is None:
            node.array = False
        else:
            node.array = True
            node.len = int(ctx.INT().getText())
            node.type += "[" + ctx.INT().getText() + "]"

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
                if type(node.init_expr) is DeclRefExprNode or type(node.init_expr) is ArraySubscriptExprNode:
                    cast_node = ImplicitCastExprNode()
                    cast_node.cast = "<LValueToRValue>"
                    cast_node.child = node.init_expr
                    cast_node.child.parent = cast_node
                    cast_node.type = cast_node.child.type
                    cast_node.line = cast_node.child.line
                    cast_node.column = cast_node.child.column
                    node.init_expr = cast_node
                node.init_expr.parent = node
                node.init = True
                if node.type == node.init_expr.type:
                    pass
                else:
                    cast_node = ImplicitCastExprNode()
                    cast_node.parent = node
                    if node.type == "int" and node.init_expr.type == "float":
                        cast_node.cast = "<FloatingToIntegral>"
                        print("Line {} Column {}".format(node.init_expr.line, node.init_expr.column))
                    elif node.type == "float" and node.init_expr.type == "int":
                        cast_node.cast = "<IntegralToFloating>"
                    else:
                        print("Need to cast in line {} but dont know this cast yet".format(ctx.start.line))
                    cast_node.type = node.type
                    cast_node.child = node.init_expr
                    cast_node.child.parent = cast_node
                    node.init_expr = cast_node

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
        node = FunctionDeclNode()
        node.line = ctx.ID().getSymbol().line
        node.column = ctx.ID().getSymbol().column
        node.init = False
        if(ctx.KEY_VOID() is None):
            node.type = ctx.prim().getText()
        else:
            node.type = "void"
        node.id = ctx.ID().getText()
        if(len(ctx.func_arg()) > 0):
            for i in range(len(ctx.func_arg())):
                parm_type = ctx.func_arg()[i].prim().getText()
                parm_id = ctx.func_arg()[i].ID().getText()
                node.arg_types.append(parm_type)
                parm_var = ParmVarDeclNode()
                parm_var.type = parm_type
                parm_var.id = parm_id
                node.children.append(parm_var)
        
        result = self.STT.insert(node.id)
        if result is None:
            pass
            # raise Exception("Failed to insert Function '{}' in symboltable".format(node.id))
        else:
            self.STT.set_attribute(node.id, "ast_node", node)
            self.STT.set_attribute(node.id, "object", "Function")

        return node


    # Visit a parse tree produced by GrammarParser#funcDecl.
    def visitFuncDecl(self, ctx:GrammarParser.FuncDeclContext):
        node = FunctionDeclNode()
        node.line = ctx.ID().getSymbol().line
        node.column = ctx.ID().getSymbol().column
        node.init = True
        node.id = ctx.ID().getText()

        result = self.STT.insert(node.id)
        if result is None:
            check_declared = self.STT.lookup(node.id)
            if check_declared is None:
                raise Exception("Failed to insert Function '{}' in symboltable".format(node.id))
            else:
                self.STT.set_attribute(node.id, "ast_node", node)
                self.STT.set_attribute(node.id, "object", "Function")
                self.STT.set_attribute(node.id, "global", True)

        else:
            self.STT.set_attribute(node.id, "ast_node", node)
            self.STT.set_attribute(node.id, "object", "Function")
            self.STT.set_attribute(node.id, "global", True)


        # Create SymbolTable for function
        self.STT.new_scope()

        if(ctx.KEY_VOID() is None):
            node.type = ctx.prim().getText()
        else:
            node.type = "void"
        if(len(ctx.func_arg()) > 0):
            for i in range(len(ctx.func_arg())):
                parm_type = ctx.func_arg()[i].prim().getText()
                temp = parm_type.split('*')
                parm_type = temp[0]
                if len(temp) >= 2:
                    parm_type += " "
                    parm_type += (len(temp)-1)*"*"

                if len(ctx.func_arg()[i].getText().split("[")) >= 2:
                    if ctx.func_arg()[i].INT() is None:
                        parm_type += "[]"
                    else:
                        parm_type += "[" + str(ctx.func_arg()[i].INT().getText()) + "]"
                
                parm_id = ctx.func_arg()[i].ID().getText()
                node.arg_types.append(parm_type)
                parm_var = ParmVarDeclNode()
                parm_var.line = ctx.func_arg()[i].start.line
                parm_var.column = ctx.func_arg()[i].start.column
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
                self.STT.set_attribute(parmvar_node.id, "global", False)

  

        scope_node = ScopeStmtNode()
        scope_node.parent = node
        for Statement in ctx.stat():
            stat_node = self.visit(Statement)
            stat_node.parent = scope_node
            scope_node.children.append(stat_node)
        
        node.children.append(scope_node)
        
        # Go back to scope where Function was declared
        self.STT.prev_scope()

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
        var_decl.column = ctx.start.column
        node.line = var_decl.line
        node.column = var_decl.column
        temp = ctx.prim().getText().split('*')
        var_decl.type = temp[0]
        if len(temp) >= 2:
            var_decl.type += " "
            var_decl.type += (len(temp)-1)*"*"

        if ctx.INT() is None:
            var_decl.array = False
        else:
            var_decl.array = True
            var_decl.len = int(ctx.INT().getText())
            var_decl.type += "[" + ctx.INT().getText() + "]"

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
                if type(var_decl.init_expr) is DeclRefExprNode or type(var_decl.init_expr) is ArraySubscriptExprNode:
                    cast_node = ImplicitCastExprNode()
                    cast_node.cast = "<LValueToRValue>"
                    cast_node.child = var_decl.init_expr
                    cast_node.child.parent = cast_node
                    cast_node.type = cast_node.child.type
                    cast_node.line = cast_node.child.line
                    cast_node.column = cast_node.child.column
                    var_decl.init_expr = cast_node
                var_decl.init_expr.parent = var_decl
                var_decl.init = True
                if var_decl.type == var_decl.init_expr.type:
                    pass
                else:
                    cast_node = ImplicitCastExprNode()
                    cast_node.parent = var_decl
                    if var_decl.type == "int" and var_decl.init_expr.type == "float":
                        cast_node.cast = "<FloatingToIntegral>"
                    elif var_decl.type == "float" and var_decl.init_expr.type == "int":
                        cast_node.cast = "<IntegralToFloating>"
                    else:
                        print("Need to cast ({}) in line {} but dont know this cast yet".format(var_decl.init_expr.type,ctx.start.line))
                    cast_node.type = var_decl.type
                    cast_node.child = var_decl.init_expr
                    cast_node.line = cast_node.child.line
                    cast_node.column = cast_node.child.column
                    cast_node.child.parent = cast_node
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
        node = WhileStmtNode()
        node.line = ctx.start.line
        node.column = ctx.start.column
        cond_node = self.visit(ctx.expr())
        cond_node.parent = node
        node.children.append(cond_node)

        # Create SymbolTable for WhileBlock
        self.STT.new_scope()

        while_scope = ScopeStmtNode()
        while_scope.parent = node
        for stat in ctx.stat():
            stat_node = self.visit(stat)
            stat_node.parent = while_scope
            while_scope.children.append(stat_node)
        node.children.append(while_scope)

        # Return to SymbolTable where WhileBlock declared
        self.STT.prev_scope()

        return node

    # Visit a parse tree produced by GrammarParser#ifStat.
    def visitIfStat(self, ctx:GrammarParser.IfStatContext):
        node = IfStmtNode()
        node.line = ctx.start.line
        node.column = ctx.start.column
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
            pass
        else:
            return_expr = self.visit(ctx.expr())
            if type(return_expr) is DeclRefExprNode or type(return_expr) is ArraySubscriptExprNode:
                    cast_node = ImplicitCastExprNode()
                    cast_node.cast = "<LValueToRValue>"
                    cast_node.child = return_expr
                    cast_node.child.parent = cast_node
                    cast_node.type = cast_node.child.type
                    return_expr = cast_node
            return_expr.parent = node
            node.child = return_expr
        return node

    # Visit a parse tree produced by GrammarParser#breakStat.
    def visitBreakStat(self, ctx:GrammarParser.BreakStatContext):
        node = BreakStmtNode()
        node.line = ctx.start.line
        node.column = ctx.start.column
        return node

    # Visit a parse tree produced by GrammarParser#continueStat.
    def visitContinueStat(self, ctx:GrammarParser.ContinueStatContext):
        node = ContinueStmtNode()
        node.line = ctx.start.line
        node.column = ctx.start.column
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
        node.column = ctx.op.column
        
        lhs_node = self.visit(ctx.left)
        if (not (node.operation == "=") ) and ((type(lhs_node) is DeclRefExprNode) or (type(lhs_node) is ArraySubscriptExprNode)):
            cast_node = ImplicitCastExprNode()
            cast_node.type = lhs_node.type
            cast_node.cast = "<LValueToRValue>"
            cast_node.child = lhs_node
            lhs_node.parent = cast_node
            lhs_node = cast_node
        else:
            pass
        lhs_node.parent = node
        rhs_node = self.visit(ctx.right)
        if ((type(rhs_node) is DeclRefExprNode) or (type(rhs_node) is ArraySubscriptExprNode)):
            cast_node = ImplicitCastExprNode()
            cast_node.type = rhs_node.type
            cast_node.cast = "<LValueToRValue>"
            cast_node.child = rhs_node
            rhs_node.parent = cast_node
            rhs_node = cast_node
        else:
            pass
        rhs_node.parent = node

        node.lhs_child = lhs_node
        node.rhs_child = rhs_node

        if node.operation == "=":
            node.type = node.lhs_child.type
            parsed_type = lhs_node.parseType()
            lhs_type_noarr = parsed_type[2]
            if parsed_type[0]:
                rhs_type_noarr += parsed_type[3]
            if lhs_type_noarr == rhs_node.type:
                pass
            else:
                cast_node = ImplicitCastExprNode()
                cast_node.parent = node
                cast_node.type = lhs_node.type
                if lhs_node.type == "int" and rhs_node.type == "float":
                    cast_node.cast = "<FloatingToIntegral>"
                elif lhs_node.type == "float" and rhs_node.type == "int":
                    cast_node.cast = "<IntegralToFloating>"
                else:
                    print("Need to cast but dont know this cast yet", lhs_node.type, rhs_node.type)
                cast_node.child = rhs_node
                rhs_node.parent = cast_node
                node.rhs_child = cast_node
        elif node.operation == "+" or node.operation == "-" or node.operation == "*" or node.operation == "/":
            lhs_type = lhs_node.parseType()
            rhs_type = rhs_node.parseType()
            
            if lhs_type[2] == rhs_type[2]:
                pass
            else:
                type_switch = {
                "char" : 0,
                "int"  : 1,
                "float": 2,
                }
                if type_switch.get(lhs_type[2], None) > type_switch.get(rhs_type[2], None):
                    if lhs_type[2] == "float":
                        if rhs_type[2] == "int":
                            cast_node = ImplicitCastExprNode()
                            cast_node.parent = node
                            cast_node.type = lhs_node.type
                            cast_node.cast = "<IntegralToFloating>"
                            cast_node.child = rhs_node
                            rhs_node.parent = cast_node
                            node.rhs_child = cast_node
                        else:
                            pass
                    else:
                        # lhs_type is larger and is not float, thus lhs_type is int and rhs_type is char.
                        pass
                else:
                    if rhs_type[2] == "float":
                        if lhs_type[2] == "int":
                            cast_node = ImplicitCastExprNode()
                            cast_node.parent = node
                            cast_node.type = rhs_node.type
                            cast_node.cast = "<IntegralToFloating>"
                            cast_node.child = lhs_node
                            lhs_node.parent = cast_node
                            node.lhs_child = cast_node
                        else:
                            pass
                    else:
                        # lhs_type is larger and is not float, thus lhs_type is int and rhs_type is char.
                        pass
            node.type = node.lhs_child.type
        else:
            node.type = "int"

        return node

    # Visit a parse tree produced by GrammarParser#postUnaryExpr.
    def visitPostUnaryExpr(self, ctx:GrammarParser.PostUnaryExprContext):
        node = UnaryExprNode()
        switcher = {
            GrammarLexer.PPP : "++",
            GrammarLexer.MPP : "--"
        }
        expr_node = self.visit(ctx.expr())
        expr_node.parent = node
        node.child = expr_node
        node.prefix = False
        node.lvalue = True
        node.operation = switcher.get(ctx.op.type, None)
        node.type = node.child.type
        node.child = expr_node
        return node


    # Visit a parse tree produced by GrammarParser#preUnaryExpr.
    def visitPreUnaryExpr(self, ctx:GrammarParser.PreUnaryExprContext):
        node = UnaryExprNode()
        switcher = {
            GrammarLexer.ADD : "+",
            GrammarLexer.SUB : "-",
            GrammarLexer.NOT : "!",
            GrammarLexer.DRF : "&",
            GrammarLexer.MUL : "*",
            GrammarLexer.PPP : "++",
            GrammarLexer.MPP : "--"
        }
        node.prefix = True
        node.operation = switcher.get(ctx.op.type, None)
        expr_node = self.visit(ctx.expr())
        node.lvalue = False
        if (not (node.operation == "&" or node.operation == "*" or node.operation == "++" or node.operation == "--")) and ((type(expr_node) is DeclRefExprNode) or (type(expr_node) is ArraySubscriptExprNode)):
            cast_node = ImplicitCastExprNode()
            cast_node.type = expr_node.type
            cast_node.cast = "<LValueToRValue>"
            cast_node.child = expr_node
            expr_node.parent = cast_node
            expr_node = cast_node
            node.lvalue = False
        # Temp 
        if (node.operation == "++" or node.operation == "--"):
            node.lvalue = True
        expr_node.parent = node
        node.child = expr_node
        node.line = ctx.start.line
        node.column = ctx.start.column
        
        if node.operation == "!":
                node.type = 'int'
        elif node.operation == "&":
            temp = node.child.parseType()
            if temp[0]:
                if temp[1]:
                    node.type = temp[2] +" "+"*"*(len(temp[3])+1) + "[" + temp[4][0] + "]"
                else:
                    node.type = temp[2] +" "+"*"*(len(temp[3])+1)
            else:
                if temp[1]:
                    node.type = temp[2] + " *" + "[" + temp[4][0] + "]"
                else:
                    node.type = temp[2] + " *"    
        elif node.operation == "*":
            temp = node.child.type.split(" ")
            if len(temp) == 1:
                raise Exception("Syntax error: Cannot dereference rvalue line {}".format(node.child.type))
            else:
                if len(temp[1]) == 1:
                    node.type = temp[0]
                else: 
                    node.type = temp[0] + " " + "*"*(len(temp[1])-1)
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
        node.column = ctx.start.column

        result = self.STT.lookup(call_id)
        if result is None:
            raise Exception("Function {} not found in symboltable".format(call_id))
        else:
            result["ast_node"].used = True
            functionref_node = DeclRefExprNode()
            functionref_node.parent = node
            functionref_node.ref = result
            functionref_node.id = result["ast_node"].id
            functionref_node.type = result["ast_node"].type
            functionref_node.function = True
            functionref_node.line = ctx.ID().getSymbol().line
            functionref_node.column = ctx.ID().getSymbol().column
            functionref_node.signature = result["ast_node"].getSignature()
            node.children.append(functionref_node)
            node.type = functionref_node.type
   
        for arg in ctx.expr():
            arg_node = self.visit(arg)
            arg_node.line = arg.start.line
            arg_node.column = arg.start.column
            if type(arg_node) is DeclRefExprNode:
                cast_node = ImplicitCastExprNode()
                temp_split = arg_node.parseType()
                if temp_split[1]:
                    cast_node.cast = "<ArrayToPointerDecay>"
                    if temp_split[0]:
                        cast_node.type = temp_split[2] + " "+ temp_split[3] + "*" +  "[" + temp_split[4][0] + "]"
                    else:
                        cast_node.type = temp_split[2] + " *" + "[" + temp_split[4][0] + "]"
                else:
                    cast_node.cast = "<LValueToRValue>"
                    cast_node.type = arg_node.type
                cast_node.child = arg_node
                arg_node.parent = cast_node
                cast_node.parent = node
                node.children.append(cast_node)
            elif type(arg_node) is ArraySubscriptExprNode:
                cast_node = ImplicitCastExprNode()
                cast_node.type = arg_node.type
                cast_node.cast = "<LValueToRValue>"
                cast_node.child = arg_node
                arg_node.parent = cast_node
                cast_node.parent = node
                node.children.append(cast_node)
            elif type(arg_node) is UnaryExprNode:
                if arg_node.operation == "*":
                    cast_node = ImplicitCastExprNode()
                    cast_node.type = arg_node.type
                    cast_node.cast = "<LValueToRValue>"
                    cast_node.child = arg_node
                    arg_node.parent = cast_node
                    cast_node.parent = node
                    node.children.append(cast_node)
                else:
                    arg_node.parent = node
                    node.children.append(arg_node)
            elif type(arg_node) is StringLiteralNode:
                cast_node = ImplicitCastExprNode()
                cast_node.type = arg_node.type
                temp_split = arg_node.parseType()
                cast_node.cast = "<ArrayToPointerDecay>"
                cast_node.type = "char *"
                cast_node.child = arg_node
                arg_node.parent = cast_node
                cast_node.parent = node
                node.children.append(cast_node)
            else:
                arg_node.parent = node
                node.children.append(arg_node)

        return node


    # Visit a parse tree produced by GrammarParser#litExpr.
    def visitLitExpr(self, ctx:GrammarParser.LitExprContext):
        return self.visit(ctx.value)

    # Visit a parse tree produced by GrammarParser#idExpr.
    def visitIdExpr(self, ctx:GrammarParser.IdExprContext):
        call_id = ctx.ID().getText()
        ref_node = DeclRefExprNode()
        result = self.STT.lookup(call_id)
        if result is None:
            raise Exception("Referenced ID {} not found in symboltable".format(call_id))
        else:
            ref_node.id = result["ast_node"].id
            ref_node.ref = result
            if result["object"] == "Function":
                ref_node.type = result["ast_node"].type
                ref_node.function = True
                ref_node.signature = result["ast_node"].getSignature()
            else:
                ref_node.type = result["ast_node"].type
            ref_node.ref["ast_node"].used = True

        ref_node.type = result["ast_node"].type
        ref_node.line = ctx.ID().getSymbol().line
        ref_node.column = ctx.ID().getSymbol().column

        if ctx.INT() is None and ctx.expr() is None:
            return ref_node
        else:
            node = ArraySubscriptExprNode()
            cast_node = ImplicitCastExprNode()
            cast_node.parent = node
            cast_node.type = ref_node.type
            cast_node.cast = "<ArrayToPointerDecay>"
            cast_node.child = ref_node
            ref_node.parent = cast_node
            node.array_child = cast_node
            node.type = result["ast_node"].type
            if ctx.INT() is None:
                # Array Index is an expr
                if ctx.expr() is None:
                    raise Exception("dl")
                node.index_child = self.visit(ctx.expr())
                node.index_child.parent = node
            else:
                # Array Index is an IntegerLiteral
                node.index_child = IntergerLiteralNode()
                node.index_child.setValue(ctx.INT().getText())
                node.index_child.line = ctx.INT().getSymbol().line
                node.index_child.column = ctx.INT().getSymbol().column
                node.index_child.parent = node
            node.line = ctx.ID().getSymbol().line
            node.column = ctx.ID().getSymbol().column
            return node

        return None

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

        node.line = ctx.start.line
        node.column = ctx.start.column

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





del GrammarParser
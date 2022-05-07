from ASTNodes import *

class ASTVisitor:

    def visitProgNode(self, node):
        pass

    def visitVarDeclNode(self, node):
        pass

    def visitFunctionDeclNode(self, node):
        pass

    def visitParmVarDeclNode(self, node):
        pass

    def visitScopeStmtNode(self, node):
        pass

    def visitDeclStmtNode(self, node):
        pass

    def visitExprStmtNode(self, node):
        pass

    def visitIfStmtNode(self, node):
        pass

    def visitWhileStmtNode(self, node):
        pass

    def visitReturnStmtNode(self, node):
        pass

    def visitBreakStmtNode(self, node):
        pass

    def visitContinueStmtNode(self, node):
        pass

    def visitBinExprNode(self, node):
        pass

    def visitUnaryExprNode(self, node):
        pass

    def visitCallExprNode(self, node):
        pass

    def visitDeclRefExprNode(self, node):
        pass
    
    def visitArraySubscriptExprNode(self, node):
        pass

    def visitImplicitCastExprNode(self, node):
        pass

    def visitInitListExprNode(self, node):
        pass

    def visitIntegerLiteralNode(self, node):
        pass

    def visitFloatingLiteralNode(self, node):
        pass

    def visitCharacterLiteralNode(self, node):
        pass

    def visitStringLiteralNode(self, node):
        pass

    def visit(self, node):

        node_type = type(node)

        if node_type is ProgNode:
            return self.visitProgNode(node)
        elif node_type is VarDeclNode:
            return self.visitVarDeclNode(node)
        elif node_type is FunctionDeclNode:
            return self.visitFunctionDeclNode(node)
        elif node_type is ParmVarDeclNode:
            return self.visitParmVarDeclNode(node)
        elif node_type is ScopeStmtNode:
            return self.visitScopeStmtNode(node)
        elif node_type is DeclStmtNode:
            return self.visitDeclStmtNode(node) 
        elif node_type is ExprStmtNode():
            return self.visitExprStmtNode(node)
        elif node_type is IfStmtNode:
            return self.visitIfStmtNode(node)
        elif node_type is WhileStmtNode:
            return self.visitWhileStmtNode(node)
        elif node_type is ReturnStmtNode:
            return self.visitReturnStmtNode(node)
        elif node_type is BreakStmtNode:
            return self.visitBreakStmtNode(node)
        elif node_type is ContinueStmtNode:
            return self.visitContinueStmtNode(node)
        elif node_type is ExprStmtNode:
            return self.visitExprStmtNode(node)
        elif node_type is BinExprNode:
            return self.visitBinExprNode(node)
        elif node_type is UnaryExprNode:
            return self.visitUnaryExprNode(node)
        elif node_type is CallExprNode:
            return self.visitCallExprNode(node)  
        elif node_type is DeclRefExprNode:
            return self.visitDeclRefExprNode(node)
        elif node_type is ArraySubscriptExprNode:
            return self.visitArraySubscriptExprNode(node)
        elif node_type is ImplicitCastExprNode:
            return self.visitImplicitCastExprNode(node)
        elif node_type is InitListExprNode:
            return self.visitInitListExprNode(node)
        elif node_type is IntergerLiteralNode:
            return self.visitIntegerLiteralNode(node)
        elif node_type is FloatingLiteralNode:
            return self.visitFloatingLiteralNode(node)
        elif node_type is CharacterLiteralNode:
            return self.visitCharacterLiteralNode(node)
        elif node_type is StringLiteralNode:
            return self.visitStringLiteralNode(node)
        else:
            print("Tried visiting undefined node")
            print(type(node))
            return -1
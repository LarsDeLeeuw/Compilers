from ASTVisitor import ASTVisitor
from ASTNodes import *
import copy

class DeadcodeASTVisitor(ASTVisitor):
    '''Does a single pass through the AST and removes deadcode'''

    def __init__(self):
        self.current_function = None
        
    def visitProgNode(self, node):
        for child in node.children:
            self.visit(child)

    def visitVarDeclNode(self, node):
        if node.init:
            node.init_expr.reachable = True if node.reachable else False
            self.visit(node.init_expr)

    def visitFunctionDeclNode(self, node):
        if node.init:
            self.current_function = node.id
            node.children[-1].reachable = True
            self.visit(node.children[-1])
        

    def visitScopeStmtNode(self, node):
        node.children[0].reachable = True
        self.visit(node.children[0])
        if type(node.children[0]) is ReturnStmtNode:
            node.children[0].normal_terminate = False
            node.children[0].return_terminate = True
            node.normal_terminate = False
            node.return_terminate = True
            node.children = node.children[:(node.children.index(node.children[0])+1)]
            return False
        elif type(node.children[0]) is ContinueStmtNode or type(node.children[0]) is BreakStmtNode:
            node.children[0].normal_terminate = False
            node.normal_terminate = False
            node.children = node.children[:(node.children.index(node.children[0])+1)]
            return False

        for child in node.children[1:]:
            index = node.children.index(child)
            child.reachable = True if node.children[index-1].reachable and node.children[index-1].normal_terminate and (not node.children[index-1].return_terminate) else False
            self.visit(child)
            if type(child) is ReturnStmtNode:
                child.normal_terminate = False
                node.normal_terminate = False
                child.return_terminate = True
                node.return_terminate = True
                node.children = node.children[:(node.children.index(child)+1)]
                return False
            elif type(child) is ContinueStmtNode or type(child) is BreakStmtNode:
                child.normal_terminate = False
                node.normal_terminate = False
                node.children = node.children[:(node.children.index(child)+1)]
                return False
            else:
                pass
                        
        node.normal_terminate = True
        return True

    def visitIfStmtNode(self, node):
        node.children[0].reachable = True if node.reachable else False
        node.children[1].reachable = True if node.reachable else False
        self.visit(node.children[0])
        self.visit(node.children[1])
        node.normal_terminate = node.children[1].normal_terminate
        node.return_terminate = node.children[1].return_terminate
        if node.has_else:
            node.children[2].reachable = True if node.reachable else False
            self.visit(node.children[2])
            node.normal_terminate = False if (not node.normal_terminate) and (not node.children[2].normal_terminate) else True
            node.return_terminate = True if (node.return_terminate) and (node.children[2].return_terminate) else False
        else:
            node.normal_terminate = True
            node.return_terminate = False

    def visitWhileStmtNode(self, node):
        node.children[0].reachable = True if node.reachable else False
        node.children[1].reachable = True if node.reachable else False
        self.visit(node.children[0])
        self.visit(node.children[1])
        node.return_terminate = node.children[1].return_terminate

    def visitReturnStmtNode(self, node):
        if node.child is None:
            pass
        else:
            node.child.reachable = True if node.reachable else False
            self.visit(node.child)

    def visitExprStmtNode(self, node):
        node.child.reachable = True if node.reachable else False
        self.visit(node.child)
    
    def visitBinExprNode(self, node):
        node.lhs_child.reachable = True if node.reachable else False
        self.visit(node.lhs_child)
        node.rhs_child.reachable = True if node.reachable else False
        self.visit(node.rhs_child)

    def visitUnaryExprNode(self, node):
        node.child.reachable = True if node.reachable else False
        self.visit(node.child)

    def visitCallExprNode(self, node):
        for child in node.children:
            child.reachable = True if node.reachable else False
            self.visit(child)

    def visitImplicitCastExprNode(self, node):
        node.child.reachable = True if node.reachable else False
        self.visit(node.child)

    def visitDeclRefExprNode(self, node):
        pass

    def visitArraySubscriptExprNode(self, node):
        node.index_child.reachable = True if node.reachable else False
        self.visit(node.index_child)
        node.array_child.reachable = True if node.reachable else False
        self.visit(node.array_child)

    def visitDeclStmtNode(self, node):
        node.child.reachable = True if node.reachable else False
        self.visit(node.child)

    def visitParmVarDeclNode(self, node):
        pass

    def visitIntegerLiteralNode(self, node):
        pass

    def visitCharacterLiteralNode(self, node):
        pass

    def visitFloatingLiteralNode(self, node):
        pass

    def visitStringLiteralNode(self, node):
        pass
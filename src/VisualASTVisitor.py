from ASTVisitor import ASTVisitor
from ASTNodes import *

class VisualASTVisitor(ASTVisitor):

    def __init__(self):
        self.labelbuffer = ""
        self.edgebuffer = ""
        self.nodecount = 0
        self.refcount = 0

    def visitProgNode(self, node):
        self.labelbuffer += "n"+str(self.nodecount)+' [label="File"];\n'
        self.nodecount += 1
        thisnode = "n"+str((self.nodecount-1))
        for StatementNode in node.children:
            self.labelbuffer += "n"+str(self.nodecount)+' [label="Statement"];\n'
            self.refcount = self.nodecount
            storeref = self.refcount
            self.nodecount += 1
            self.edgebuffer += thisnode +" -> "+"n"+str((self.nodecount-1))+"\n"
            self.visit(StatementNode)
            self.refcount = storeref
        return 0

    def visitVarDeclNode(self, node):
        thisnode = "n"+str((self.nodecount))
        self.edgebuffer +=  "n"+str((self.nodecount-1)) +" -> "+ thisnode +"\n"
        self.refcount = self.nodecount
        storeref = self.refcount
        self.nodecount += 1
        self.labelbuffer += thisnode+' [label="'+ str("INIT") +'"];\n'
        
        #self.visit(node.InnerNode.ExpressionNode)
   
        self.refcount = storeref

        self.labelbuffer += "n"+str(self.nodecount)+' [label="'+ node.type +'"];\n'
        self.edgebuffer += thisnode +" -> "+"n"+str((self.nodecount))+"\n"
        self.nodecount += 1
        self.labelbuffer += "n"+str(self.nodecount)+' [label="'+ node.id +'"];\n'
        self.edgebuffer += thisnode +" -> "+"n"+str((self.nodecount))+"\n"
        self.nodecount += 1

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

    def visitBinExprNode(self, node):
        pass

    def visitUnaryExprNode(self, node):
        pass

    def visitCallExprNode(self, node):
        pass

    def visitDeclRefExprNode(self, node):
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
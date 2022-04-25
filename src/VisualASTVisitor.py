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
        thisnode = "n"+str((self.nodecount))
        storeref = self.nodecount
        for DeclNode in node.children:
            self.refcount = storeref
            self.nodecount += 1
            self.visit(DeclNode)
        return 0

    def visitVarDeclNode(self, node):
        thisnode = "n"+str((self.nodecount))
        self.edgebuffer +=  "n"+str((self.refcount)) +" -> "+ thisnode +"\n"
        self.refcount = self.nodecount
        storeref = self.refcount
        self.nodecount += 1
        self.labelbuffer += thisnode+' [label="'+ str("VarDecl") +'"];\n'

        if node.array:
            self.labelbuffer += "n"+str(self.nodecount)+' [label="'+ node.type +"["+ str(node.len) +"]"+'"];\n'
            self.edgebuffer += thisnode +" -> "+"n"+str((self.nodecount))+"\n"
            self.nodecount += 1
        else:
            self.labelbuffer += "n"+str(self.nodecount)+' [label="'+ node.type +'"];\n'
            self.edgebuffer += thisnode +" -> "+"n"+str((self.nodecount))+"\n"
            self.nodecount += 1

        self.labelbuffer += "n"+str(self.nodecount)+' [label="'+ node.id +'"];\n'
        self.edgebuffer += thisnode +" -> "+"n"+str((self.nodecount))+"\n"
        self.nodecount += 1

        if not node.init_expr is None:
            self.visit(node.init_expr)

    def visitFunctionDeclNode(self, node):
        thisnode = "n"+str((self.nodecount))
        self.edgebuffer +=  "n"+str((self.refcount)) +" -> "+ thisnode +"\n"
        self.refcount = self.nodecount
        storeref = self.refcount
        self.nodecount += 1
        self.labelbuffer += thisnode+' [label="'+ str("FuncDecl") +'"];\n'
        
        self.labelbuffer += "n"+str(self.nodecount)+' [label="'+ node.getSignature() +'"];\n'
        self.edgebuffer += thisnode +" -> "+"n"+str((self.nodecount))+"\n"
        self.nodecount += 1
        self.labelbuffer += "n"+str(self.nodecount)+' [label="'+ node.id +'"];\n'
        self.edgebuffer += thisnode +" -> "+"n"+str((self.nodecount))+"\n"
        self.nodecount += 1

        scopenode = "n"+str((self.nodecount))
        self.edgebuffer +=  thisnode +" -> "+ scopenode +"\n"
        self.refcount = self.nodecount
        storeref = self.refcount
        self.nodecount += 1
        self.labelbuffer += scopenode+' [label="'+ str("FuncScope") +'"];\n'

        for Child in node.children:
            self.refcount = storeref
            self.nodecount += 1
            self.visit(Child)

    def visitParmVarDeclNode(self, node):
        thisnode = "n"+str((self.nodecount))
        self.edgebuffer +=  "n"+str((self.refcount)) +" -> "+ thisnode +"\n"
        self.refcount = self.nodecount
        storeref = self.refcount
        self.nodecount += 1
        self.labelbuffer += thisnode+' [label="'+ str("ParmVarDecl") +'"];\n'

        self.labelbuffer += "n"+str(self.nodecount)+' [label="'+ node.type +'"];\n'
        self.edgebuffer += thisnode +" -> "+"n"+str((self.nodecount))+"\n"
        self.nodecount += 1
        self.labelbuffer += "n"+str(self.nodecount)+' [label="'+ node.id +'"];\n'
        self.edgebuffer += thisnode +" -> "+"n"+str((self.nodecount))+"\n"
        self.nodecount += 1

    def visitScopeStmtNode(self, node):
        thisnode = "n"+str((self.nodecount))
        self.edgebuffer +=  "n"+str(self.refcount) +" -> "+ thisnode +"\n"
        self.refcount = self.nodecount
        storeref = self.refcount
        self.nodecount += 1
        self.labelbuffer += thisnode+' [label="'+ str("Body") +'"];\n'

        for Child in node.children:
            self.refcount = storeref
            self.nodecount += 1
            self.visit(Child)

    def visitDeclStmtNode(self, node):
        thisnode = "n"+str((self.nodecount))
        self.edgebuffer +=  "n"+str(self.refcount) +" -> "+ thisnode +"\n"
        self.refcount = self.nodecount
        storeref = self.refcount
        self.nodecount += 1
        self.labelbuffer += thisnode+' [label="'+ str("DeclStmt") +'"];\n'

        self.visit(node.child)

    def visitExprStmtNode(self, node):
        thisnode = "n"+str((self.nodecount))
        self.labelbuffer += thisnode+' [label="'+ str("ExprStmt") +'"];\n'
        self.edgebuffer +=  "n"+str(self.refcount) +" -> "+ thisnode +"\n"
        self.refcount = self.nodecount
        storeref = self.refcount
        self.nodecount += 1

        self.visit(node.child)

    def visitIfStmtNode(self, node):
        thisnode = "n"+str((self.nodecount))
        self.edgebuffer +=  "n"+str(self.refcount) +" -> "+ thisnode +"\n"
        self.refcount = self.nodecount
        storeref = self.refcount
        self.nodecount += 1
        self.labelbuffer += thisnode+' [label="'+ str("IfStmt") +'"];\n'

        for Child in node.children:
            self.refcount = storeref
            self.nodecount += 1
            self.visit(Child)

    def visitWhileStmtNode(self, node):
        thisnode = "n"+str((self.nodecount))
        self.edgebuffer +=  "n"+str(self.refcount) +" -> "+ thisnode +"\n"
        self.refcount = self.nodecount
        storeref = self.refcount
        self.nodecount += 1
        self.labelbuffer += thisnode+' [label="'+ str("WhileStmt") +'"];\n'

        for Child in node.children:
            self.refcount = storeref
            self.nodecount += 1
            self.visit(Child)

    def visitReturnStmtNode(self, node):
        thisnode = "n"+str((self.nodecount))
        self.edgebuffer +=  "n"+str(self.refcount) +" -> "+ thisnode +"\n"
        self.refcount = self.nodecount
        storeref = self.refcount
        self.nodecount += 1
        self.labelbuffer += thisnode+' [label="'+ str("ReturnStmt") +'"];\n'

        self.visit(node.child)


    def visitBinExprNode(self, node):
        thisnode = "n"+str((self.nodecount))
        self.labelbuffer += thisnode+' [label="'+ node.operation +'"];\n'
        self.edgebuffer +=  "n"+str(self.refcount) +" -> "+ thisnode +"\n"
        self.refcount = self.nodecount
        storeref = self.refcount
        self.nodecount += 1

        self.visit(node.lhs_child)
        self.refcount = storeref
        self.nodecount += 1

        self.visit(node.rhs_child)


    def visitUnaryExprNode(self, node):
        pass

    def visitCallExprNode(self, node):
        pass

    def visitDeclRefExprNode(self, node):
        thisnode = "n"+str((self.nodecount))
        self.labelbuffer += thisnode+' [label="'+ str(node.id) +'"];\n'
        self.edgebuffer +=  "n"+str(self.refcount) +" -> "+ thisnode +"\n"

    def visitImplicitCastExprNode(self, node):
        pass

    def visitInitListExprNode(self, node):
        pass

    def visitIntegerLiteralNode(self, node):
        thisnode = "n"+str((self.nodecount))
        self.labelbuffer += thisnode+' [label="'+ str(node.value) +'"];\n'
        self.edgebuffer +=  "n"+str(self.refcount) +" -> "+ thisnode +"\n"

    def visitFloatingLiteralNode(self, node):
        pass

    def visitCharacterLiteralNode(self, node):
        pass

    def visitStringLiteralNode(self, node):
        pass
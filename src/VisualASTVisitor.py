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
        
        nodelabel = ""
        if node.const:
            nodelabel += "const " + node.type
        else:
            nodelabel += node.type

        if node.array:
            self.labelbuffer += "n"+str(self.nodecount)+' [label="'+ nodelabel +"["+ str(node.len) +"]"+'"];\n'
            self.edgebuffer += thisnode +" -> "+"n"+str((self.nodecount))+"\n"
            self.nodecount += 1
        else:
            self.labelbuffer += "n"+str(self.nodecount)+' [label="'+ nodelabel +'"];\n'
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

        if not (node.child is None):
            self.visit(node.child)

    def visitBreakStmtNode(self, node):
        thisnode = "n"+str((self.nodecount))
        self.edgebuffer +=  "n"+str(self.refcount) +" -> "+ thisnode +"\n"
        self.nodecount += 1
        self.labelbuffer += thisnode+' [label="'+ str("BreakStmt") +'"];\n'

    def visitContinueStmtNode(self, node):
        thisnode = "n"+str((self.nodecount))
        self.edgebuffer +=  "n"+str(self.refcount) +" -> "+ thisnode +"\n"
        self.nodecount += 1
        self.labelbuffer += thisnode+' [label="'+ str("ContinueStmt") +'"];\n'


    def visitBinExprNode(self, node):
        thisnode = "n"+str((self.nodecount))
        self.labelbuffer += thisnode+' [label="BinExpr\n'+ "'" + node.operation + "'" +'"];\n'
        self.edgebuffer +=  "n"+str(self.refcount) +" -> "+ thisnode +"\n"
        self.refcount = self.nodecount
        storeref = self.refcount
        self.nodecount += 1

        self.visit(node.lhs_child)
        self.refcount = storeref
        self.nodecount += 1

        self.visit(node.rhs_child)


    def visitUnaryExprNode(self, node):
        thisnode = "n"+str((self.nodecount))
        if node.lvalue:
            label = "UnaryOperator\nlvalue "
        else:
            label = "UnaryOperator\nrvalue "
        if node.prefix:
            label += "prefix '"
        else:
            label += "postfix '"
        label += node.operation + "'"
        self.labelbuffer += thisnode+' [label="'+ label +'"];\n'
        self.edgebuffer +=  "n"+str(self.refcount) +" -> "+ thisnode +"\n"
        self.refcount = self.nodecount
        self.nodecount += 1

        self.visit(node.child)

    def visitCallExprNode(self, node):
        thisnode = "n"+str((self.nodecount))
        self.labelbuffer += thisnode+' [label="'+ str("CallExpr\n"+node.children[0].ref["ast_node"].type+" " + node.children[0].ref["ast_node"].id) +'()"];\n'
        self.edgebuffer +=  "n"+str(self.refcount) +" -> "+ thisnode +"\n"
        self.refcount = self.nodecount
        storeref = self.refcount
        self.nodecount += 1

        for Child in node.children[1:]:
            self.refcount = storeref
            self.nodecount += 1
            self.visit(Child)

    def visitDeclRefExprNode(self, node):
        thisnode = "n"+str((self.nodecount))
        self.labelbuffer += thisnode+' [label="'+ "DeclRefExpr\n"+str(node.ref["object"] + " '"+ node.id)+"'" +'"];\n'
        self.edgebuffer +=  "n"+str(self.refcount) +" -> "+ thisnode +"\n"

    def visitArraySubscriptExprNode(self, node):
        thisnode = "n"+str((self.nodecount))
        self.labelbuffer += thisnode+' [label="'+ "ArraySubscriptExpr\n'"+node.type+ "' lvalue" +'"];\n'
        self.edgebuffer +=  "n"+str(self.refcount) +" -> "+ thisnode +"\n"
        self.refcount = self.nodecount
        storeref = self.refcount
        self.nodecount += 1

        self.visit(node.array_child)
        self.refcount = storeref
        self.nodecount += 1

        self.visit(node.index_child)

    def visitImplicitCastExprNode(self, node):
        thisnode = "n"+str((self.nodecount))
        self.edgebuffer +=  "n"+str(self.refcount) +" -> "+ thisnode +"\n"
        self.refcount = self.nodecount
        storeref = self.refcount
        self.nodecount += 1
        self.labelbuffer += thisnode+' [label="'+ str("ImplicitCastExpr\n" + node.cast) +'"];\n'
        self.visit(node.child)

    def visitInitListExprNode(self, node):
        thisnode = "n"+str((self.nodecount))
        self.edgebuffer +=  "n"+str(self.refcount) +" -> "+ thisnode +"\n"
        self.refcount = self.nodecount
        storeref = self.refcount
        self.nodecount += 1
        self.labelbuffer += thisnode+' [label="'+ str("InitListExpr") +'"];\n'

        for child in node.children:
            self.refcount = storeref
            self.nodecount += 1
            self.visit(child)

    def visitIntegerLiteralNode(self, node):
        thisnode = "n"+str((self.nodecount))
        label = "IntegerLiteral\nrvalue "
        label += "'" + str(node.value) + "'"
        self.labelbuffer += thisnode+' [label="'+ label +'"];\n'
        self.edgebuffer +=  "n"+str(self.refcount) +" -> "+ thisnode +"\n"

    def visitFloatingLiteralNode(self, node):
        thisnode = "n"+str((self.nodecount))
        label = "FloatingLiteral\nrvalue "
        label += "'" + str(node.value) + "'"
        self.labelbuffer += thisnode+' [label="'+ label +'"];\n'
        self.edgebuffer +=  "n"+str(self.refcount) +" -> "+ thisnode +"\n"

    def visitCharacterLiteralNode(self, node):
        thisnode = "n"+str((self.nodecount))
        label = "CharacterLiteral\nrvalue "
        label += "'" + chr(node.value) + "'"
        self.labelbuffer += thisnode+' [label="'+ label +'"];\n'
        self.edgebuffer +=  "n"+str(self.refcount) +" -> "+ thisnode +"\n"

    def visitStringLiteralNode(self, node):
        pass
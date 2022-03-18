from ASTVisitor import ASTVisitor


class VisualASTVisitor(ASTVisitor):

    def __init__(self):
        self.labelbuffer = ""
        self.edgebuffer = ""
        self.nodecount = 0

    def visitProgNode(self, node):
        self.labelbuffer += "n"+str(self.nodecount)+' [label="File"];\n'
        self.nodecount += 1
        thisnode = "n"+str((self.nodecount-1))
        for StatementNode in node.StatementNodes:
            self.labelbuffer += "n"+str(self.nodecount)+' [label="Statement"];\n'
            self.nodecount += 1
            self.edgebuffer += thisnode +" -> "+"n"+str((self.nodecount-1))+"\n"
            print(type(StatementNode))
            self.visit(StatementNode)
        return 0

    def visitAssignNode(self, node):
        pass

    def visitIdNode(self, node):
        thisnode = "n"+str((self.nodecount))
        self.edgebuffer +=  "n"+str((self.nodecount-1)) +" -> "+ thisnode +"\n"
        self.nodecount += 1
        self.labelbuffer += thisnode+' [label="'+ str("=") +'"];\n'
        self.labelbuffer += "n"+str(self.nodecount)+' [label="'+ str(type(node.PrimitiveNode)) +'"];\n'
        self.edgebuffer += thisnode +" -> "+"n"+str((self.nodecount))+"\n"
        self.nodecount += 1
        self.labelbuffer += "n"+str(self.nodecount)+' [label="'+ str(node.ID) +'"];\n'
        self.edgebuffer += thisnode +" -> "+"n"+str((self.nodecount))+"\n"
        self.nodecount += 1
        self.labelbuffer += "n"+str(self.nodecount)+' [label="'+ str(node.LiteralNode.value) +'"];\n'
        self.edgebuffer += thisnode +" -> "+"n"+str((self.nodecount))+"\n"
        self.nodecount += 1

    def visitBinaryExpressionNode(self, node):
        thisnode = "n"+str((self.nodecount))
        self.edgebuffer +=  "n"+str((self.nodecount-1)) +" -> "+ thisnode +"\n"
        self.nodecount += 1
        self.labelbuffer += thisnode+' [label="'+ str(type(node.op)) +'"];\n'
        self.labelbuffer += "n"+str(self.nodecount)+' [label="'+ str(node.lhs.value) +'"];\n'
        self.edgebuffer += thisnode +" -> "+"n"+str((self.nodecount))+"\n"
        self.nodecount += 1
        self.labelbuffer += "n"+str(self.nodecount)+' [label="'+ str(node.rhs.value) +'"];\n'
        self.edgebuffer += thisnode +" -> "+"n"+str((self.nodecount))+"\n"

    def visitNegateNode(self, node):
        pass

    def visitLiteralNode(self, node):
        pass

    def visitPrimitiveNode(self, node):
        pass
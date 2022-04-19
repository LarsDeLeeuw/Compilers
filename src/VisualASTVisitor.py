from ASTVisitor import ASTVisitor
from Nodes import *

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
        for StatementNode in node.StatementNodes:
            self.labelbuffer += "n"+str(self.nodecount)+' [label="Statement"];\n'
            self.refcount = self.nodecount
            storeref = self.refcount
            self.nodecount += 1
            self.edgebuffer += thisnode +" -> "+"n"+str((self.nodecount-1))+"\n"
            self.visit(StatementNode)
            self.refcount = storeref
        return 0

    def visitStatementNode(self, node):
        return self.visit(node.InnerNode)

    def visitAssignNode(self, node):
        pass

    def visitIdNode(self, node):
        thisnode = "n"+str((self.nodecount))
        self.edgebuffer +=  "n"+str((self.nodecount-1)) +" -> "+ thisnode +"\n"
        self.refcount = self.nodecount
        storeref = self.refcount
        self.nodecount += 1
        self.labelbuffer += thisnode+' [label="'+ str("=") +'"];\n'
        
        self.visit(node.ExpressionNode)
   
        self.refcount = storeref

        self.labelbuffer += "n"+str(self.nodecount)+' [label="'+ self.visitPrimitiveNode(node.PrimitiveNode) +'"];\n'
        self.edgebuffer += thisnode +" -> "+"n"+str((self.nodecount))+"\n"
        self.nodecount += 1
        self.labelbuffer += "n"+str(self.nodecount)+' [label="'+ str(node.ID) +'"];\n'
        self.edgebuffer += thisnode +" -> "+"n"+str((self.nodecount))+"\n"
        self.nodecount += 1

        # self.labelbuffer += "n"+str(self.nodecount)+' [label="'+ str(node.ExpressionNode.value) +'"];\n'
        # self.edgebuffer += thisnode +" -> "+"n"+str((self.nodecount))+"\n"
        # self.nodecount += 1

    def visitBinaryExpressionNode(self, node):

        switcher = {
            type(AdditionNode()) : "+",
            type(SubstractionNode()) : "-",
            type(MultiplicationNode()) : "*",
            type(DivisionNode()) : "/",
            type(LessThanNode()) : "<",
            type(GreaterThanNode()) : ">",
            type(IsEqualNode()) : "==",
            type(IsNotEqualNode()) : "!=",
            type(LessOrEqualNode()) : "<=",
            type(GreaterOrEqualNode()) : ">=",
            type(AndNode()) : "&&",
            type(OrNode()) : "||",
            type(ModulusNode()) : '%'
        }

        # Declare this_node to reference to later in block, connect parent_node and this_node.
        this_node = "n"+str((self.nodecount))
        self.edgebuffer +=  "n"+str((self.refcount)) +" -> "+ this_node +"\n"
        self.labelbuffer += this_node+' [label="'+ switcher.get(type(node.op), "???") +'"];\n'
        self.refcount = self.nodecount
        storeref = self.refcount
        self.nodecount += 1

        self.visit(node.lhs)
        # self.labelbuffer += "n"+str(self.nodecount)+' [label="'+ str(node.lhs.value) +'"];\n'
        # self.edgebuffer += this_node +" -> "+"n"+str((self.nodecount))+"\n"
        # self.nodecount += 1

        self.refcount = storeref
        self.visit(node.rhs)
        # self.labelbuffer += "n"+str(self.nodecount)+' [label="'+ str(node.rhs.value) +'"];\n'
        # self.edgebuffer += this_node +" -> "+"n"+str((self.nodecount))+"\n"
        # self.nodecount += 1
    
    def visitNegateNode(self, node):
        # Declare this_node to reference to later in block, connect parent_node and this_node.
        this_node = "n"+str((self.nodecount))
        if node.boolean:
            label = "!"
        else:
            label = "-"
        self.edgebuffer +=  "n"+str((self.refcount)) +" -> "+ this_node +"\n"
        self.labelbuffer += this_node+' [label="'+ label +'"];\n'
        self.refcount = self.nodecount
        storeref = self.refcount
        self.nodecount += 1
        self.visit(node.InnerNode)
        self.refcount = storeref

    def visitLiteralNode(self, node):
        # Declare this_node to reference to later in block, connect parent_node and this_node.
        this_node = "n"+str((self.nodecount))
        self.edgebuffer +=  "n"+str((self.refcount)) +" -> "+ this_node +"\n"
        self.labelbuffer += this_node+' [label="'+ str(node.value) +'"];\n'
        self.nodecount += 1
    

    def visitPrimitiveNode(self, node):
        switcher = {
            type(PrimitiveCharNode()) : "char",
            type(PrimitiveFloatNode()) : "float",
            type(PrimitiveIntNode()) : "int"
        }

        return switcher.get(type(node), "?!?")
from Nodes import *

class ASTVisitor:

    def visitProgNode(self, node):
        pass

    def visitAssignNode(self, node):
        pass

    def visitBinaryExpressionNode(self, node):
        pass

    def visitNegateNode(self, node):
        pass

    def visitIdNode(self, node):
        pass

    def visitLiteralNode(self, node):
        pass

    def visitPrimitiveNode(self, node):
        pass

    def visitIdNode(self, node):
        pass

    def visit(self, node):

        node_type = type(node)

        if node_type is ProgNode:
            return self.visitProgNode(node)
        elif node_type is AssignNode:
            return self.visitAssignNode(node)
        elif node_type is IdNode:
            return self.visitIdNode(node) 
        elif node_type is BinaryExpressionNode:
            return self.visitBinaryExpressionNode(node)
        elif node_type is NegateNode:
            return self.visitNegateNode(node)
        elif node_type is IdNode:
            return self.visitIdNode(node)
        elif node_type is LiteralNode:
            return self.visitLiteralNode(node)
        elif node_type is PrimitiveNode:
            return self.visitPrimitiveNode(node)
        else:
            print("Tried visiting undefined node")
            print(type(node))
            return -1
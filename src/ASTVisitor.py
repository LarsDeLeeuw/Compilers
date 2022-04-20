from Nodes import *

class ASTVisitor:

    def visitProgNode(self, node):
        pass

    def visitStatementNode(self, node):
        pass

    def visitScopeNode(self, node):
        pass

    def visitAssignNode(self, node):
        pass

    def visitInitNode(self, node):
        pass

    def visitFunctionNode(self, node):
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
        elif node_type is ScopeNode:
            return self.visitScopeNode(node)
        elif node_type is StatementNode:
            return self.visitStatementNode(node)
        elif node_type is AssignNode:
            return self.visitAssignNode(node)
        elif node_type is InitNode:
            return self.visitInitNode(node)
        elif node_type is IdNode:
            return self.visitIdNode(node) 
        elif node_type is BinaryExpressionNode:
            return self.visitBinaryExpressionNode(node)
        elif node_type is FunctionNode:
            return self.visitFunctionNode(node)
        elif node_type is NegateNode:
            return self.visitNegateNode(node)
        elif node_type is IdNode:
            return self.visitIdNode(node)
        elif node_type is LiteralNode:
            return self.visitLiteralNode(node)
        elif node_type is IntegerNode:
            return self.visitLiteralNode(node)
        elif node_type is CharNode:
            return self.visitLiteralNode(node)   
        elif node_type is FloatNode:
            return self.visitLiteralNode(node)
        elif node_type is PrimitiveNode:
            return self.visitPrimitiveNode(node)
        else:
            print("Tried visiting undefined node")
            print(type(node))
            return -1
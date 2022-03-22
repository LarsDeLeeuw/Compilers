from ASTVisitor import ASTVisitor
from Nodes import *

class ConstFoldingASTVisitor(ASTVisitor):

    def visitProgNode(self, node):
        for StatementNode in node.StatementNodes:
            self.visit(StatementNode)
            print(type(StatementNode))
        return 0

    def visitAssignNode(self, node):
        pass

    def visitBinaryExpressionNode(self, node):

        lhs_checked = node.lhs
        rhs_checked = node.rhs

        if type(lhs_checked) is BinaryExpressionNode:
            lhs_checked = self.visit(node.lhs) 

        if type(rhs_checked) is BinaryExpressionNode:
            rhs_checked = self.visit(node.rhs)

        if type(lhs_checked) is IntegerNode and type(rhs_checked) is IntegerNode:

            folded_node = IntegerNode()

            switcher = {
                AdditionNode        : int(lhs_checked.value) + int(rhs_checked.value),
                SubstractionNode    : int(lhs_checked.value) - int(rhs_checked.value),
                MultiplicationNode  : int(lhs_checked.value) * int(rhs_checked.value),
                DivisionNode        : int(lhs_checked.value) / int(rhs_checked.value)
            }

            folded_node.value = switcher.get(type(node.op), "?")
            folded_node.Parent = node.Parent
            
            if node.Parent is ProgNode:
                index = node.Parent.StatementNodes.index(node)
                node.Parent.StatementNodes.insert(index, folded_node)
                node.Parent.StatementNodes.remove(node)
            elif type(node.Parent) is IdNode:
                node.Parent.ExpressionNode = folded_node
            elif type(node.Parent) is BinaryExpressionNode:
                print("hehehehj")
                if node.Parent.lhs == node:
                    node.Parent.lhs = folded_node
                else:
                    node.Parent.rhs = folded_node
                self.visit(node.Parent)
        
    def visitNegateNode(self, node):
        pass

    def visitLiteralNode(self, node):
        pass

    def visitPrimitiveNode(self, node):
        pass

    def visitIdNode(self, node):
        self.visit(node.ExpressionNode)

    
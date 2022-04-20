from ASTVisitor import ASTVisitor
from Nodes import *

class ConstFoldingASTVisitor(ASTVisitor):

    def visitProgNode(self, node):
        for StatementNode in node.StatementNodes:
            self.visit(StatementNode)
        return 0

    def visitAssignNode(self, node):
        return self.visit(node.NewExpressionNode)

    def visitInitNode(self, node):
        return self.visit(node.InnerNode)

    def visitStatementNode(self, node):
        return self.visit(node.InnerNode)

    def visitBinaryExpressionNode(self, node):

        lhs_checked = node.lhs
        rhs_checked = node.rhs

        if type(lhs_checked) is IdNode:
            lhs_checked = self.visit(lhs_checked)

        if type(rhs_checked) is IdNode:
            rhs_checked = self.visit(rhs_checked)

        if (issubclass(type(lhs_checked), LiteralNode) and issubclass(type(rhs_checked), LiteralNode)) and (type(lhs_checked) == type(rhs_checked)):

            if type(lhs_checked) is IntegerNode:
                
                folded_node = IntegerNode()

                if type(node.op) is AdditionNode:
                    folded_node.value = int(lhs_checked.value) + int(rhs_checked.value)
                elif type(node.op) is SubstractionNode:
                    folded_node.value = int(lhs_checked.value) - int(rhs_checked.value)
                elif type(node.op) is MultiplicationNode:
                    folded_node.value = int(lhs_checked.value) * int(rhs_checked.value)
                elif type(node.op) is DivisionNode:
                    folded_node.value = int(int(lhs_checked.value) / int(rhs_checked.value))
                elif type(node.op) is GreaterThanNode:
                    folded_node.value = int (1) if int(lhs_checked.value) > int(rhs_checked.value) else 0
                elif type(node.op) is LessThanNode:
                    folded_node.value = int (1) if int(lhs_checked.value) < int(rhs_checked.value) else 0
                elif type(node.op) is IsEqualNode:
                    folded_node.value = int (1) if int(lhs_checked.value) == int(rhs_checked.value) else 0
                else:
                    folded_node.value = "?"
            elif type(lhs_checked) is FloatNode:
                folded_node = FloatNode()

                if type(node.op) is AdditionNode:
                    folded_node.value = float(lhs_checked.value) + float(rhs_checked.value)
                elif type(node.op) is SubstractionNode:
                    folded_node.value = float(lhs_checked.value) - float(rhs_checked.value)
                elif type(node.op) is MultiplicationNode:
                    folded_node.value = float(lhs_checked.value) * float(rhs_checked.value)
                elif type(node.op) is DivisionNode:
                    folded_node.value = float(int(lhs_checked.value) / float(rhs_checked.value))
                elif type(node.op) is GreaterThanNode:
                    folded_node.value = float (1) if int(lhs_checked.value) > float(rhs_checked.value) else 0
                elif type(node.op) is LessThanNode:
                    folded_node.value = int (1) if float(lhs_checked.value) < float(rhs_checked.value) else 0
                elif type(node.op) is IsEqualNode:
                    folded_node.value = int (1) if float(lhs_checked.value) == float(rhs_checked.value) else 0
                else:
                    folded_node.value = "?"
            else:
                print("ERRORINFOLDINGCAUSE")

            folded_node.Parent = node.Parent
            folded_node.serial = node.serial
            
            if node.Parent is ProgNode:
                index = node.Parent.StatementNodes.index(node)
                node.Parent.StatementNodes.insert(index, folded_node)
                node.Parent.StatementNodes.remove(node)
            elif type(node.Parent) is IdNode:
                node.Parent.ExpressionNode = folded_node
            elif type(node.Parent) is BinaryExpressionNode:
                if node.Parent.lhs == node:
                    node.Parent.lhs = folded_node
                else:
                    node.Parent.rhs = folded_node
                self.visit(node.Parent)
            elif type(node.Parent) is StatementNode:
               node.Parent.InnerNode = folded_node
            
            return 0

        if type(lhs_checked) is BinaryExpressionNode or type(lhs_checked) is NegateNode:
            lhs_checked = self.visit(node.lhs) 

        if type(rhs_checked) is BinaryExpressionNode or type(rhs_checked) is NegateNode:
            rhs_checked = self.visit(node.rhs)

        if issubclass(type(lhs_checked), LiteralNode) and issubclass(type(rhs_checked), LiteralNode):

            folded_node = IntegerNode()

            switcher = {
                AdditionNode        : int(lhs_checked.value) + int(rhs_checked.value),
                SubstractionNode    : int(lhs_checked.value) - int(rhs_checked.value),
                MultiplicationNode  : int(lhs_checked.value) * int(rhs_checked.value),
                DivisionNode        : int(int(lhs_checked.value) / int(rhs_checked.value)),
                GreaterThanNode     : int (1) if int(lhs_checked.value) > int(rhs_checked.value) else 0,
                LessThanNode        : int (1) if int(lhs_checked.value) < int(rhs_checked.value) else 0,
                IsEqualNode         : int (1) if int(lhs_checked.value) == int(rhs_checked.value) else 0,
            }

            folded_node.value = switcher.get(type(node.op), "?")
            folded_node.Parent = node.Parent
            folded_node.serial = node.serial
            
            if node.Parent is ProgNode:
                index = node.Parent.StatementNodes.index(node)
                node.Parent.StatementNodes.insert(index, folded_node)
                node.Parent.StatementNodes.remove(node)
            elif type(node.Parent) is IdNode:
                node.Parent.ExpressionNode = folded_node
            elif type(node.Parent) is BinaryExpressionNode:
                if node.Parent.lhs == node:
                    node.Parent.lhs = folded_node
                else:
                    node.Parent.rhs = folded_node
                self.visit(node.Parent)
            elif type(node.Parent) is StatementNode:
               node.Parent.InnerNode = folded_node

            return 0
        
    def visitNegateNode(self, node):

        innernode_checked = node.InnerNode

        # If the InnerNode is a BinExp, try visiting it to check if it folds to IntNode
        if type(innernode_checked) is BinaryExpressionNode:
            innernode_checked = self.visit(node.InnerNode)
        
        #If the InnerNode is a NegNode, 'cut' node and node.InnerNode from AST
        if type(innernode_checked) is NegateNode:
            if type(node.Parent) is IdNode:
                node.Parent.ExpressionNode = node.InnerNode.InnerNode
            elif type(node.Parent) is BinaryExpressionNode:
                if node.Parent.lhs == node:
                    node.Parent.lhs = node.InnerNode.InnerNode
                else:
                    node.Parent.rhs = node.InnerNode.InnerNode
                self.visit(node.Parent)
            elif type(node.Parent) is StatementNode:
               node.Parent.InnerNode = node.InnerNode.InnerNode

            node.InnerNode.InnerNode.Parent = node.Parent
            self.visit(node.InnerNode.InnerNode)

        if type(innernode_checked) is IntegerNode:
            innernode_checked.value = -int(innernode_checked.value)

            if type(node.Parent) is IdNode:
                node.Parent.ExpressionNode = innernode_checked
            elif type(node.Parent) is BinaryExpressionNode:
                if node.Parent.lhs == node:
                    node.Parent.lhs = innernode_checked
                else:
                    node.Parent.rhs = innernode_checked
                self.visit(node.Parent)
            elif type(node.Parent) is StatementNode:
               node.Parent.InnerNode = innernode_checked

    def visitLiteralNode(self, node):
        pass

    def visitPrimitiveNode(self, node):
        pass

    def visitIdNode(self, node):
        # Check if ID refers to a literal or can be folded to a literal
        # If not then return node, else return the folded or literal node
        if issubclass(type(node.ExpressionNode), LiteralNode):
            return node.ExpressionNode
        else:
            self.visit(node.ExpressionNode)

        if issubclass(type(node.ExpressionNode), LiteralNode):
            return node.ExpressionNode
        else:
            return node


    
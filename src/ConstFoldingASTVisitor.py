from ASTVisitor import ASTVisitor
from ASTNodes import *

class ConstFoldingASTVisitor(ASTVisitor):

    def visitProgNode(self, node):
        for DeclNode in node.children:
            self.visit(DeclNode)
        return 0

    def visitVarDeclNode(self, node):
        if node.init:
            if issubclass(type(node.getInitExpr()), LiteralNode):
                return 0
            else:
                self.visit(node.init_expr)
        return 0
    
    def visitFunctionDeclNode(self, node):
        if node.init:
            # Visit the function's scope node, located at end of children
            self.visit(node.children[-1])

    def visitScopeStmtNode(self, node):
        for StmtNode in node.children:
            self.visit(StmtNode)
    
    def visitExprStmtNode(self, node):
        self.visit(node.child)

    def visitDeclStmtNode(self, node):
        self.visit(node.child)

    def visitCallExprNode(self, node):
        if len(node.children) > 1:
            for Arg in node.children[1:]:
                self.visit(Arg)

    def visitStatementNode(self, node):
        return self.visit(node.InnerNode)

    def visitBinExprNode(self, node):
        lhs_checked = node.lhs_child
        rhs_checked = node.rhs_child

        # Try and get literal
        if not (issubclass(type(lhs_checked), LiteralNode)):
            self.visit(lhs_checked)
        if not (issubclass(type(rhs_checked), LiteralNode)):
            self.visit(rhs_checked)
        lhs_checked = node.lhs_child
        rhs_checked = node.rhs_child

        if (issubclass(type(lhs_checked), LiteralNode) and issubclass(type(rhs_checked), LiteralNode)) and (type(lhs_checked) == type(rhs_checked)):
        # Only fold if lhs and rhs are same type
            if node.type == "int":
                folded_node = IntergerLiteralNode()
                if node.operation == "+":
                    folded_node.value = int(lhs_checked.value) + int(rhs_checked.value)
                elif node.operation == "-":
                    folded_node.value = int(lhs_checked.value) - int(rhs_checked.value)
                elif node.operation == "*":
                    folded_node.value = int(lhs_checked.value) * int(rhs_checked.value)
                elif node.operation == "/":
                    folded_node.value = int(int(lhs_checked.value) / int(rhs_checked.value))
                elif node.operation == ">":
                    folded_node.value = int (1) if int(lhs_checked.value) > int(rhs_checked.value) else 0
                elif node.operation == "<":
                    folded_node.value = int (1) if int(lhs_checked.value) < int(rhs_checked.value) else 0
                elif node.operation == "==":
                    folded_node.value = int (1) if int(lhs_checked.value) == int(rhs_checked.value) else 0
                else:
                    folded_node.value = "?"
            elif node.type == "float":
                folded_node = FloatingLiteralNode()
                if node.operation == "+":
                    folded_node.value = float(lhs_checked.value) + float(rhs_checked.value)
                elif node.operation == "-":
                    folded_node.value = float(lhs_checked.value) - float(rhs_checked.value)
                elif node.operation == "*":
                    folded_node.value = float(lhs_checked.value) * float(rhs_checked.value)
                elif node.operation == "/":
                    folded_node.value = float(int(lhs_checked.value) / float(rhs_checked.value))
                elif node.operation == ">":
                    folded_node.value = float (1) if int(lhs_checked.value) > float(rhs_checked.value) else 0
                elif node.operation == "<":
                    folded_node.value = int (1) if float(lhs_checked.value) < float(rhs_checked.value) else 0
                elif node.operation == "==":
                    folded_node.value = int (1) if float(lhs_checked.value) == float(rhs_checked.value) else 0
                else:
                    folded_node.value = "?"
            else:
                print("ERRORINFOLDINGCAUSE")

            folded_node.parent = node.parent
            folded_node.type = node.type

            if type(node.parent) is VarDeclNode:
                node.parent.init_expr = folded_node
            elif type(node.parent) is DeclRefExprNode:
                node.parent.ref = folded_node
            elif type(node.parent) is BinExprNode:
                if node.parent.lhs_child == node:
                    node.parent.lhs_child = folded_node
                else:
                    node.parent.rhs_child = folded_node
                # self.visit(node.Parent)
            elif type(node.parent) is UnaryExprNode:
               node.parent.child = folded_node
            elif type(node.parent) is CallExprNode:
                node.parent.children.insert(node.parent.children.index(node), folded_node)
                node.parent.children.remove(node)
            return 0
        
    def visitUnaryExprNode(self, node):
        child_checked = node.child

        if type(child_checked) is UnaryExprNode:
            pass

        if not (issubclass(type(child_checked), LiteralNode)):
            child_checked = self.visit(child_checked)
        
        if issubclass(type(child_checked), LiteralNode):
            pass

    def visitDeclRefExprNode(self, node):
        pass
        
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


    
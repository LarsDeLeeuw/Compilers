
class AbstractNode:
    
    def __init__(self):
        self.Parent = None

    def setParent(self, node):
        self.Parent = node
    

class ProgNode(AbstractNode):

    def __init__(self):
        super().__init__()
        self.StatementNodes = []

class AssignNode(AbstractNode):

    def __init__(self):
        super().__init__()
        self.IdNode = None
        self.LiteralNode = None

class ExpressionNode (AbstractNode):
    pass

class BinaryExpressionNode (ExpressionNode):
    
    def __init(self):
        super().__init__()
        self.lhs = None
        self.rhs = None
        self.op = None

class AdditionNode (BinaryExpressionNode):
    pass

class SubstractionNode (BinaryExpressionNode):
    pass

class MultiplicationNode (BinaryExpressionNode):
    pass

class DivisionNode (BinaryExpressionNode):
    pass

class LessThanNode (BinaryExpressionNode):
    pass

class GreaterThanNode (BinaryExpressionNode):
    pass

class IsEqualNode (BinaryExpressionNode):
    pass

class IsNotEqualNode (BinaryExpressionNode):
    pass

class LessOrEqualNode (BinaryExpressionNode):
    pass

class GreaterOrEqualNode (BinaryExpressionNode):
    pass

class AndNode (BinaryExpressionNode):
    pass

class OrNode (BinaryExpressionNode):
    pass

class ModulusNode (BinaryExpressionNode):
    pass

class NegateNode (ExpressionNode):
    
    def __init__(self):
        super().__init__()
        self.boolean = None
        self.InnerNode = None


class LiteralNode (ExpressionNode):
    
    def __init__(self):
        super().__init__()
        self.value = None

class IntegerNode (LiteralNode):
    pass

class FloatNode (LiteralNode):
    pass

class CharNode (LiteralNode):
    pass


class PrimitiveNode(AbstractNode):
    pass

class PrimitiveCharNode(PrimitiveNode):
    pass

class PrimitiveFloatNode(PrimitiveNode):
    pass

class PrimitiveIntNode(PrimitiveNode):
    pass

class IdNode(ExpressionNode):

    def __init__(self):
        super().__init__()
        self.PrimitiveNode = None
        self.ID = None
        self.ExpressionNode = None





class AbstractNode:
    
    def __init__(self):
        self.Parent = None
        self.serial = None

    def setParent(self, node):
        self.Parent = node
    
    def save(self):
        return "AbstractNode save method used, something went wrong"
    

class ProgNode(AbstractNode):

    def __init__(self):
        super().__init__()
        self.StatementNodes = []

    def save(self):
        progsavebuffer = ''
        nodesavebuffer = ''
        for stat in self.StatementNodes:
            switcher = {
                type(IdNode()) : 'idnode',
                type(AssignNode()) : 'assignnode' 
            }
            nodetype = switcher.get(type(stat), str(type(stat)))
            progsavebuffer += '\t\t\t<'+nodetype+'>' + str(stat.serial) + '</'+nodetype+'>\n'
            nodesavebuffer += stat.save()

        return '\t<PROG>\n\t\t<STATS>\n' + progsavebuffer + '\t\t</STATS>\n\t</PROG>\n' + nodesavebuffer
        
class StatementNode(AbstractNode):
    pass

class AssignNode(StatementNode):

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

    def save(self):
        innersavebuffer = '\t<BINOPNODE>\n\t\t<serial>'+str(self.serial)+'</serial>\n\t</BINOPNODE>\n'
        return innersavebuffer
        
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
    
    def save(self):
        return '\t<PRIMCHARNODE>\n\t\t<serial>'+str(self.serial)+'</serial>\n\t</PRIMCHARNODE>\n'

class PrimitiveFloatNode(PrimitiveNode):

    def save(self):
        return '\t<PRIMFLOATNODE>\n\t\t<serial>'+str(self.serial)+'</serial>\n\t</PRIMFLOATNODE>\n'

class PrimitiveIntNode(PrimitiveNode):

    def save(self):
        return '\t<PRIMINTNODE>\n\t\t<serial>'+str(self.serial)+'</serial>\n\t</PRIMINTNODE>\n'

class IdNode(StatementNode):

    def __init__(self):
        super().__init__()
        self.PrimitiveNode = None
        self.ID = None
        self.ExpressionNode = None

    def save(self):
        innersavebuffer = '\t<IDNODE>\n\t\t<serial>'+str(self.serial)+'</serial>\n'
        innersavebuffer += '\t\t<primitive>'+str(self.PrimitiveNode.serial)+'</primitive>\n'
        innersavebuffer += '\t\t<id>'+str(self.ID)+'</id>\n'
        innersavebuffer += '\t\t<expression>'+str(self.ExpressionNode.serial)+'</expression>\n'+'\t</IDNODE>\n'

        innersavebuffer += self.PrimitiveNode.save()
        innersavebuffer += self.ExpressionNode.save()

        return innersavebuffer


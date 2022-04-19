
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
            nodetype = switcher.get(type(stat), 'expression')
            progsavebuffer += '\t\t\t<'+nodetype+'>' + str(stat.serial) + '</'+nodetype+'>\n'
            nodesavebuffer += stat.save()

        return '\t<PROG>\n\t\t<serial>'+str(self.serial)+'</serial>\n\t\t<STATS>\n' + progsavebuffer + '\t\t</STATS>\n\t</PROG>\n' + nodesavebuffer
        
class StatementNode(AbstractNode):

    def __init__(self):
        super().__init__()
        self.IdNode = None
        self.InnerNode = None

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
        innersavebuffer = '\t<BINOPNODE>\n\t\t<serial>'+str(self.serial)+'</serial>\n'
        innersavebuffer += '\t\t<lhs>'+str(self.lhs.serial)+'</lhs>\n'
        innersavebuffer += '\t\t<op>'+str(self.op.serial)+'</op>\n'
        innersavebuffer += '\t\t<rhs>'+str(self.rhs.serial)+'</rhs>\n\t</BINOPNODE>\n'

        innersavebuffer += self.lhs.save()
        innersavebuffer += self.op.save()
        innersavebuffer += self.rhs.save()
        return innersavebuffer
        
class AdditionNode (BinaryExpressionNode):

    def save(self):
        innerbuffer = '\t<ADDNODE>\n\t\t<serial>'+str(self.serial)+'</serial>\n'+'\t</ADDNODE>\n'
        return innerbuffer

class SubstractionNode (BinaryExpressionNode):
    
    def save(self):
        innerbuffer = '\t<SUBNODE>\n\t\t<serial>'+str(self.serial)+'</serial>\n'+'\t</SUBNODE>\n'
        return innerbuffer

class MultiplicationNode (BinaryExpressionNode):
    
    def save(self):
        innerbuffer = '\t<MULNODE>\n\t\t<serial>'+str(self.serial)+'</serial>\n'+'\t</MULNODE>\n'
        return innerbuffer

class DivisionNode (BinaryExpressionNode):
    
    def save(self):
        innerbuffer = '\t<DIVNODE>\n\t\t<serial>'+str(self.serial)+'</serial>\n'+'\t</DIVNODE>\n'
        return innerbuffer

class LessThanNode (BinaryExpressionNode):
    
    def save(self):
        innerbuffer = '\t<LSTNODE>\n\t\t<serial>'+str(self.serial)+'</serial>\n'+'\t</LSTNODE>\n'
        return innerbuffer

class GreaterThanNode (BinaryExpressionNode):
    
    def save(self):
        innerbuffer = '\t<GRTNODE>\n\t\t<serial>'+str(self.serial)+'</serial>\n'+'\t</GRTNODE>\n'
        return innerbuffer

class IsEqualNode (BinaryExpressionNode):
    
    def save(self):
        innerbuffer = '\t<EQNODE>\n\t\t<serial>'+str(self.serial)+'</serial>\n'+'\t</EQNODE>\n'
        return innerbuffer

class IsNotEqualNode (BinaryExpressionNode):
    
    def save(self):
        innerbuffer = '\t<NEQNODE>\n\t\t<serial>'+str(self.serial)+'</serial>\n'+'\t</NEQNODE>\n'
        return innerbuffer

class LessOrEqualNode (BinaryExpressionNode):
    
    def save(self):
        innerbuffer = '\t<LEQNODE>\n\t\t<serial>'+str(self.serial)+'</serial>\n'+'\t</LEQNODE>\n'
        return innerbuffer

class GreaterOrEqualNode (BinaryExpressionNode):
    
    def save(self):
        innerbuffer = '\t<GEQNODE>\n\t\t<serial>'+str(self.serial)+'</serial>\n'+'\t</GEQNODE>\n'
        return innerbuffer

class AndNode (BinaryExpressionNode):
    
    def save(self):
        innerbuffer = '\t<ANDNODE>\n\t\t<serial>'+str(self.serial)+'</serial>\n'+'\t</ANDNODE>\n'
        return innerbuffer

class OrNode (BinaryExpressionNode):
    
    def save(self):
        innerbuffer = '\t<ORNODE>\n\t\t<serial>'+str(self.serial)+'</serial>\n'+'\t</ORNODE>\n'
        return innerbuffer

class ModulusNode (BinaryExpressionNode):
    
    def save(self):
        innerbuffer = '\t<MODNODE>\n\t\t<serial>'+str(self.serial)+'</serial>\n'+'\t</MODNODE>\n'
        return innerbuffer

class NegateNode (ExpressionNode):
    
    def __init__(self):
        super().__init__()
        self.boolean = None
        self.InnerNode = None

    def save(self):
        innerbuffer = '\t<NEGATENODE>\n\t\t<serial>'+str(self.serial)+'</serial>\n'
        innerbuffer += '\t\t<innernode>'+str(self.InnerNode.serial)+'</innernode>\n\t</NEGATENODE>\n'
        innerbuffer += self.InnerNode.save()
        return innerbuffer


class LiteralNode (ExpressionNode):
    
    def __init__(self):
        super().__init__()
        self.value = None

class IntegerNode (LiteralNode):
    
    def save(self):
        innerbuffer = '\t<INTNODE>\n\t\t<serial>'+str(self.serial)+'</serial>\n'
        innerbuffer += '\t\t<value>'+str(self.value)+'</value>\n\t</INTNODE>\n'
        return innerbuffer

class FloatNode (LiteralNode):
    
    def save(self):
        innerbuffer = '\t<FLOATNODE>\n\t\t<serial>'+str(self.serial)+'</serial>\n'
        innerbuffer += '\t\t<value>'+str(self.value)+'</value>\n\t</FLOATNODE>\n'
        return innerbuffer   

class CharNode (LiteralNode):

    def save(self):
        innerbuffer = '\t<CHARNODE>\n\t\t<serial>'+str(self.serial)+'</serial>\n'
        innerbuffer += '\t\t<value>'+str(self.value)+'</value>\n\t</CHARNODE>\n'
        return innerbuffer


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


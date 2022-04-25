
class AbstractNode:
    
    def __init__(self):
        self.parent = None
        self.serial = None

    def setParent(self, node):
        self.parent = node
    
    

class ProgNode(AbstractNode):
    '''
    This is the file node, placed at the root of the AST.
    It has DeclNode children.
    '''
    def __init__(self):
        self.children = []
        self.includes = {}
        
class DeclNode(AbstractNode):
    """Superclass for DeclNodes"""
    pass

class VarDeclNode(DeclNode):
    
    def __init__(self):
        self.line = None        # tuple(int row, int column)
        self.used = False
        self.id = None          # string
        self.type = None        # string
        self.array = False
        self.len = None
        self.init = False       
        self.init_expr = None   # InitListExprNode or LiteralNode

    def getInitExpr(self):
        if(self.init):
            return self.init_expr
        else:
            raise Exception("Trying to access init_expr of uninitialised VarDeclNode")

    def getLen(self):
        if(self.array):
            return self.len
        else:
            raise Exception("Trying to access len of non-array VarDeclNode")

class FunctionDeclNode(DeclNode):
    
    def __init__(self):
        self.line = None
        self.init = False
        self.used = False
        self.id = None
        self.included = False
        self.symboltable = None
        self.return_type = None # string, if no return_type -> 'void'
        self.arg_types = []     # [string, ...)
        self.children = []      # first signature.len are ParmVar, last is ScopeStmt

    def getSignature(self):
        output = self.return_type + " ("
        index = 0
        lensign = len(self.arg_types)
        for sign in self.arg_types:
            if(index == lensign - 1):
               output += sign
            else:
                output += sign + ", "
            index += 1
        output += ")"
        return output

class ParmVarDeclNode(DeclNode):
    
    def __init__(self):
        self.id = None
        self.type = None
        self.array = False
        self.len = None
        self.init = False

    def getLen(self):
        if(self.array):
            return self.len
        else:
            raise Exception("Trying to access len of non-array VarDeclNode")


class StmtNode(AbstractNode):
    '''Superclass for StmtNodes'''
    
    def __init__(self):
        self.line = None

class ScopeStmtNode(StmtNode):
    '''Node containing statements in same scope'''
    
    def __init__(self):
        self.symboltable = None
        self.children = []

class DeclStmtNode(StmtNode):
    
    def __init__(self):
        self.child = None

class ExprStmtNode(StmtNode):
    
    def __init__(self):
        self.child = None

class IfStmtNode(StmtNode):
    
    def __init__(self):
        self.has_else = False
        self.children = []      # first child is cond, next is ifblock, optional else block

class WhileStmtNode(StmtNode):
    
    def __init__(self):
        self.children = []

class ReturnStmtNode(StmtNode):
    
    def __init__(self):
        self.child = None


class ExprNode(AbstractNode):
    '''Superclass for ExprNodes'''
    
    def __init__(self):
        self.line = None

class BinExprNode(ExprNode):
    
    def __init__(self):
        self.type = None
        self.operation = None
        self.lhs_child = None
        self.rhs_child = None

class UnaryExprNode(ExprNode):
    
    def __init__(self):
        self.type = None
        self.operation = None
        self.prefix = True
        self.child = None

class CallExprNode(ExprNode):
    
    def __init__(self):
        self.type = None
        self.children = []  # first function, then args

class DeclRefExprNode(ExprNode):
    
    def __init__(self):
        self.type = None
        self.signature = None
        self.function = False
        self.ref = None
        self.id = None

class ImplicitCastExprNode(ExprNode):
    
    def __init__(self):
        self.type = None
        self.cast = None
        self.signature = None

class InitListExprNode(ExprNode):
    
    def __init__(self):
        self.type = None
        self.array = True
        self.len = None
        self.children = []


class LiteralNode(ExprNode):
    '''Superclass for LiteralNodes'''
    
    def __init__(self):
        self.type = None
        self.value = None

    def setValue(self, value):
        pass

class IntergerLiteralNode(LiteralNode):
    
    def setValue(self, value):
        try:
            self.value = int(value)
            self.type = "int"
        except:
            raise Exception("Failed setting value for IntegerLiteralNode")
    

class FloatingLiteralNode(LiteralNode):

    def setValue(self, value):
        try:
            self.value = float(value)
            self.type = "float"
        except:
            raise Exception("Failed setting value for FloatingLiteralNode")

class CharacterLiteralNode(LiteralNode):

     def setValue(self, value):
        try:
            self.value = chr(value)
            self.type = "char"
        except:
            raise Exception("Failed setting value for CharacterLiteralNode")

class StringLiteralNode(LiteralNode):
    # Not sure about this one atm
     def setValue(self, value):
        try:
            self.value = str(value[1:-1])
            self.type = "string"
        except:
            raise Exception("Failed setting value for StringLiteralNode")



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
    
    def __init__(self):
        self.line = None    # int
        self.column = None  # int

class VarDeclNode(DeclNode):
    
    def __init__(self):
        self.used = False
        self.id = None          # string
        self.type = None        # string
        self.array = False
        self.len = None
        self.const = False
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
        self.init = False
        self.used = False
        self.id = None
        self.included = False   # true if included from outer lib
        self.return_type = None # string, if no return_type -> 'void'
        self.arg_types = []     # [string, ...)
        self.children = []      # first signature.len are ParmVar, last is ScopeStmt

    def getSignature(self):
        if self.return_type is None:
            output = "void ("
        else:
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
        self.column = None

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
        self.children = []      # first child is cond, next scope

class ReturnStmtNode(StmtNode):
    
    def __init__(self):
        self.child = None

class BreakStmtNode(StmtNode):

    def __init__(self):
        pass

class ContinueStmtNode(StmtNode):

    def __init__(self):
        pass

class ExprNode(AbstractNode):
    '''Superclass for ExprNodes'''
    
    def __init__(self):
        self.line = None
        self.column = None

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

class ArraySubscriptExprNode(ExprNode):

    def __init__(self):
        self.type = None
        self.lvalue = True
        self.array_child = None
        self.index_child = None

class ImplicitCastExprNode(ExprNode):
    
    def __init__(self):
        self.type = None
        self.cast = None
        self.child = None
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
        self.line = None
        self.column = None
        self.type = None
        self.value = None
        self.offset = 0

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
            self.value = ord(value)
            self.type = "char"
        except:
            raise Exception("Failed setting value for CharacterLiteralNode")

class StringLiteralNode(LiteralNode):
    # Not sure about this one atm
     def setValue(self, value):
        try:
            ''' When setting the value, first parse the string because escapechars are not behaving
                Using offset because len('\n') = 1 but len('\0A') = 3 so this info needs to be kept.
            '''
            buffer = ""
            escape_flag = False
            for character in str(value[1:-1]):
                if escape_flag:
                    if character == "n":
                        buffer += "\\0A"
                        self.offset -= 2
                    else:
                        buffer += "\\" + character
                    escape_flag = False
                    continue
                if character == '\\':
                    escape_flag = True
                else:
                    buffer += character
            self.value = buffer
            self.type = "string"
        except:
            raise Exception("Failed setting value for StringLiteralNode")



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

    def parseType(self):
        if self.type is None:
            return None
        temp = self.type.split(" ")
        prim = None
        ptr = None
        array = None
        if len(temp) == 2:
            isPtr = True
        else:
            isPtr = False
        if isPtr:
            prim = temp[0]
            temp = temp[1].split("[")
            if len(temp) == 1:
                isArray = False
                ptr = temp[0]
            else:
                isArray = True
                ptr = temp[0]
                for i, j in enumerate(temp):
                    temp[i] = j.strip("]")
                array = temp[1:]
        else:
            temp = temp[0].split("[")
            if len(temp) == 1:
                isArray = False
                prim = temp[0]
            else:
                isArray = True
                prim = temp[0]
                for i, j in enumerate(temp):
                    temp[i] = j.strip("]")
                array = temp[1:]
                    
        return [isPtr, isArray, prim, ptr, array]

class VarDeclNode(DeclNode):
    
    def __init__(self):
        super().__init__()
        self.used = False
        self.id = None          # string
        self.type = None        # string
        self.array = False
        self.array_size_expr = None
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
        super().__init__()
        self.init = False
        self.used = False
        self.id = None
        self.included = False   # true if included from outer lib
        self.type = None        # string, if no return_type -> 'void'
        self.arg_types = []     # [string, ...)
        self.children = []      # first arg_types.len are ParmVar, last is ScopeStmt

    def getSignature(self):
        if self.type is None:
            output = "void ("
        else:
            output = self.type + " ("
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
        super().__init__()
        self.id = None
        self.type = None
        self.array = False
        self.len = None
        self.init = False
        self.used = False

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
        super().__init__()
        self.symboltable = None
        self.children = []

class DeclStmtNode(StmtNode):
    
    def __init__(self):
        super().__init__()
        self.child = None

class ExprStmtNode(StmtNode):
    
    def __init__(self):
        super().__init__()
        self.child = None

class IfStmtNode(StmtNode):
    
    def __init__(self):
        super().__init__()
        self.has_else = False
        self.children = []      # first child is cond, next is ifblock, optional else block

class WhileStmtNode(StmtNode):
    
    def __init__(self):
        super().__init__()
        self.children = []      # first child is cond, next scope

class ReturnStmtNode(StmtNode):
    
    def __init__(self):
        super().__init__()
        self.child = None

class BreakStmtNode(StmtNode):

    def __init__(self):
        super().__init__()

class ContinueStmtNode(StmtNode):

    def __init__(self):
        super().__init__()

class ExprNode(AbstractNode):
    '''Superclass for ExprNodes'''
    
    def __init__(self):
        self.line = None
        self.column = None
    
    def parseType(self):
        if self.type is None:
            return None
        temp = self.type.split(" ")
        prim = None
        ptr = None
        array = None
        if len(temp) == 2:
            isPtr = True
        else:
            isPtr = False
        if isPtr:
            prim = temp[0]
            temp = temp[1].split("[")
            if len(temp) == 1:
                isArray = False
                ptr = temp[0]
            else:
                isArray = True
                ptr = temp[0]
                for i, j in enumerate(temp):
                    temp[i] = j.strip("]")
                array = temp[1:]
        else:
            temp = temp[0].split("[")
            if len(temp) == 1:
                isArray = False
                prim = temp[0]
            else:
                isArray = True
                prim = temp[0]
                for i, j in enumerate(temp):
                    temp[i] = j.strip("]")
                array = temp[1:]
                    
        return [isPtr, isArray, prim, ptr, array]

class BinExprNode(ExprNode):
    
    def __init__(self):
        super().__init__()
        self.type = None
        self.operation = None
        self.lhs_child = None
        self.rhs_child = None

class UnaryExprNode(ExprNode):
    
    def __init__(self):
        super().__init__()
        self.type = None
        self.operation = None
        self.prefix = True
        self.child = None

class CallExprNode(ExprNode):
    
    def __init__(self):
        super().__init__()
        self.type = None
        self.children = []  # first function, then args

class DeclRefExprNode(ExprNode):
    
    def __init__(self):
        super().__init__()
        self.type = None
        self.signature = None
        self.function = False
        self.ref = None
        self.id = None

class ArraySubscriptExprNode(ExprNode):

    def __init__(self):
        super().__init__()
        self.type = None
        self.array_child = None
        self.index_child = None

class ImplicitCastExprNode(ExprNode):
    
    def __init__(self):
        super().__init__()
        self.type = None
        self.cast = None
        self.child = None
        self.signature = None

class InitListExprNode(ExprNode):
    
    def __init__(self):
        super().__init__()
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
        self.buffer = None
        self.rawbuffer = None

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

    def setValue(self, value):
        try:
            ''' When setting the value, first parse the string because escapechars are not behaving
                Using offset because len('\n') = 1 but len('\0A') = 3 so this info needs to be kept.
            '''
            buffer = []
            escape_flag = False
            self.rawbuffer = []
            for character in str(value[1:-1]):
                self.rawbuffer.append(str(character))
                if escape_flag:
                    if character == "n":
                        buffer.append("\\0A")
                        self.offset -= 2
                    elif character == "t":
                        buffer.append("\\09")
                    else:
                        buffer.append("\\" + str(character))
                    escape_flag = False
                    continue
                if character == '\\':
                    escape_flag = True
                else:
                    buffer.append(str(character))
            
            self.rawvalue = ""
            for char in self.rawbuffer:
                self.rawvalue += char
            self.buffer = buffer
            self.value = ""
            for char in buffer:
                self.value += char
            self.type = "char[" + str(len(buffer)) + "]"
        except:
            raise Exception("Failed setting value for StringLiteralNode")


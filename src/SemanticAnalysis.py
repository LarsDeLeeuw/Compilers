from ASTVisitor import ASTVisitor
from ASTNodes import *
import copy

class bcolors:
    OK = '\033[1;92m' # BOLD GREEN
    WARNING = '\033[1;93m' # BOLD YELLOW
    FAIL = '\033[1;91m' # BOLD RED
    NOTE = '\033[1;96m'
    BOLD = '\033[1;97m' # BOLD WHITE
    RESET = '\033[0m' #RESET COLOR


class SemanticAnalysis(ASTVisitor):

    def __init__(self, inputfilepath):
        self.inputfilepath = inputfilepath
        self.buffer = {}
        self.buffer["warnings"] = []
        self.buffer["errors"] = []
        with open(inputfilepath) as f:
            self.lines = f.readlines()
        self.register = -1
       
    def loadSTT(self, STT):
        self.STT = copy.deepcopy(STT)

    def getRegister(self):
        self.register += 1
        return self.register

    def visitProgNode(self, node):
        for symbol_id in self.STT.current_symboltablenode.hashtable.keys():
            self.STT.set_attribute(symbol_id, "declared", "false")

        for DeclChild in node.children:
            self.visit(DeclChild)
        
        # self.buffer["main"] += "\t\tret i32 0\n}\n"
        
        return 0

    def visitFunctionDeclNode(self, node):
        if node.init:
            self.STT.child_scope()
            self.visit(node.children[-1])
            self.STT.prev_scope()
        else:
            result = self.STT.lookup(node.id)
            if result["ast_node"].getSignature() == node.getSignature():
                pass
            else:
                print( bcolors.BOLD + "{}:{}:{}: ".format(self.inputfilepath, node.line, node.column) + bcolors.FAIL + "error: " + bcolors.RESET 
                + "conflicting types for '\033[1;97m{}\033[0m'; have '\033[1;97m{}\033[0m'".format(node.id, node.getSignature()))
                print(" "*(5-len(str(node.line))) + str(node.line) + " | " + self.lines[node.line-1][:node.column] + bcolors.FAIL + self.lines[node.line-1][node.column] + bcolors.RESET + self.lines[node.line-1][node.column+1:-1])
                print(" "*(5) + " | " + " "*(node.column) + bcolors.FAIL + "^" + bcolors.RESET)
                print( bcolors.BOLD + "{}:{}:{}: ".format(self.inputfilepath, result["ast_node"].line, result["ast_node"].column) + bcolors.NOTE + "note: " + bcolors.RESET 
                + "previous declaration of '\033[1;97m{}\033[0m'; with type '\033[1;97m{}\033[0m'".format(result["ast_node"].id, result["ast_node"].getSignature()))
                print(" "*(5-len(str(result["ast_node"].line))) + str(result["ast_node"].line) + " | " + self.lines[result["ast_node"].line-1][:result["ast_node"].column] + bcolors.NOTE + self.lines[result["ast_node"].line-1][result["ast_node"].column] + bcolors.RESET + self.lines[result["ast_node"].line-1][result["ast_node"].column+1:-1])
                print(" "*(5) + " | " + " "*(result["ast_node"].column) + bcolors.NOTE + "^" + bcolors.RESET)

                self.buffer["errors"].append(bcolors.BOLD + "{}:{}:{}: ".format(self.inputfilepath, node.line, node.column) + bcolors.FAIL + "error: " + bcolors.RESET 
                + "conflicting types for '\033[1;97m{}\033[0m'; have '\033[1;97m{}\033[0m'".format(node.id, node.getSignature())
                + " "*(5-len(str(node.line))) + str(node.line) + " | " + self.lines[node.line-1][:node.column] + bcolors.FAIL + self.lines[node.line-1][node.column] + bcolors.RESET + self.lines[node.line-1][node.column+1:-1] 
                + " "*(5) + " | " + " "*(node.column) + bcolors.FAIL + "^" + bcolors.RESET
                 + bcolors.BOLD + "{}:{}:{}: ".format(self.inputfilepath, result["ast_node"].line, result["ast_node"].column) + bcolors.NOTE + "note: " + bcolors.RESET 
                + "previous declaration of '\033[1;97m{}\033[0m'; with type '\033[1;97m{}\033[0m'".format(result["ast_node"].id, result["ast_node"].getSignature())
                + " "*(5-len(str(result["ast_node"].line))) + str(result["ast_node"].line) + " | " + self.lines[result["ast_node"].line-1][:result["ast_node"].column] + bcolors.NOTE + self.lines[result["ast_node"].line-1][result["ast_node"].column] + bcolors.RESET + self.lines[result["ast_node"].line-1][result["ast_node"].column+1:-1] 
                + " "*(5) + " | " + " "*(result["ast_node"].column) + bcolors.NOTE + "^" + bcolors.RESET)

    def visitScopeStmtNode(self, node):
        for symbol_id in self.STT.current_symboltablenode.hashtable.keys():
            self.STT.set_attribute(symbol_id, "declared", "false")

        for StmtNode in node.children:
            self.visit(StmtNode)
    
    def visitDeclStmtNode(self, node):
        # if self.STT.lookup(node.child.id)["declared"] == "false":
        #     self.STT.set_attribute(node.child.id, "declared", "true")
        # else:
        #     print("got ya")
        self.visit(node.child)
    
    def visitExprStmtNode(self, node):
        self.visit(node.child)

    def visitArraySubscriptExprNode(self, node):
        if not node.array_child.parseType()[1]:
            print( bcolors.BOLD + "{}:{}:{}: ".format(self.inputfilepath, node.line, node.column) + bcolors.FAIL + "error: " + bcolors.RESET 
            + "subscripted value is not an array")
            print(" "*(5-len(str(node.line))) + str(node.line) + " | " + self.lines[node.line-1][:node.column] + bcolors.FAIL + self.lines[node.line-1][node.column] + bcolors.RESET + self.lines[node.line-1][node.column+1:-1])
            print(" "*(5) + " | " + " "*(node.column) + bcolors.FAIL + "^" + bcolors.RESET)
            
            self.buffer["errors"].append(bcolors.BOLD + "{}:{}:{}: ".format(self.inputfilepath, node.line, node.column) + bcolors.FAIL + "error: " + bcolors.RESET 
            + "subscripted value is not an array"
            + " "*(5-len(str(node.line))) + str(node.line) + " | " + self.lines[node.line-1][:node.column] + bcolors.FAIL + self.lines[node.line-1][node.column] + bcolors.RESET + self.lines[node.line-1][node.column+1:-1] 
            + " "*(5) + " | " + " "*(node.column) + bcolors.FAIL + "^" + bcolors.RESET)

        if node.index_child.type != "int":
            print( bcolors.BOLD + "{}:{}:{}: ".format(self.inputfilepath, node.line, node.column) + bcolors.FAIL + "error: " + bcolors.RESET 
            + "array subscript is not an integer")
            print(" "*(5-len(str(node.line))) + str(node.line) + " | " + self.lines[node.line-1][:node.column] + bcolors.FAIL + self.lines[node.line-1][node.column] + bcolors.RESET + self.lines[node.line-1][node.column+1:-1])
            print(" "*(5) + " | " + " "*(node.column) + bcolors.FAIL + "^" + bcolors.RESET)
            
            self.buffer["errors"].append(bcolors.BOLD + "{}:{}:{}: ".format(self.inputfilepath, node.line, node.column) + bcolors.FAIL + "error: " + bcolors.RESET 
            + "array subscript is not an integer"
            + " "*(5-len(str(node.line))) + str(node.line) + " | " + self.lines[node.line-1][:node.column] + bcolors.FAIL + self.lines[node.line-1][node.column] + bcolors.RESET + self.lines[node.line-1][node.column+1:-1] 
            + " "*(5) + " | " + " "*(node.column) + bcolors.FAIL + "^" + bcolors.RESET)

    def visitVarDeclNode(self, node):
        result = self.STT.lookup(node.id)
        if result["declared"] == "false":
            self.STT.set_attribute(node.id, "declared", "true")
            if node.array:
                if node.array_size_expr.type == "int":
                    pass
                else:
                    print( bcolors.BOLD + "{}:{}:{}: ".format(self.inputfilepath, node.line, node.column) + bcolors.FAIL + "error: " + bcolors.RESET 
                    + "size of array '\033[1;97m{}\033[0m' has non-integer type".format(node.id))
                    print(" "*(5-len(str(node.line))) + str(node.line) + " | " + self.lines[node.line-1][:node.column] + bcolors.FAIL + self.lines[node.line-1][node.column] + bcolors.RESET + self.lines[node.line-1][node.column+1:-1])
                    print(" "*(5) + " | " + " "*(node.column) + bcolors.FAIL + "^" + bcolors.RESET)
                    
                    self.buffer["errors"].append(bcolors.BOLD + "{}:{}:{}: ".format(self.inputfilepath, node.line, node.column) + bcolors.FAIL + "error: " + bcolors.RESET 
                    + "size of array '\033[1;97m{}\033[0m' has non-integer type".format(node.id)
                    + " "*(5-len(str(node.line))) + str(node.line) + " | " + self.lines[node.line-1][:node.column] + bcolors.FAIL + self.lines[node.line-1][node.column] + bcolors.RESET + self.lines[node.line-1][node.column+1:-1] 
                    + " "*(5) + " | " + " "*(node.column) + bcolors.FAIL + "^" + bcolors.RESET)
        else:
            if result["ast_node"].type != node.type:
                print( bcolors.BOLD + "{}:{}:{}: ".format(self.inputfilepath, node.line, node.column) + bcolors.FAIL + "error: " + bcolors.RESET 
                + "conflicting types for '\033[1;97m{}\033[0m'; have '\033[1;97m{}\033[0m'".format(node.id, node.type))
                print(" "*(5-len(str(node.line))) + str(node.line) + " | " + self.lines[node.line-1][:node.column] + bcolors.FAIL + self.lines[node.line-1][node.column] + bcolors.RESET + self.lines[node.line-1][node.column+1:-1])
                print(" "*(5) + " | " + " "*(node.column) + bcolors.FAIL + "^" + bcolors.RESET)
                print( bcolors.BOLD + "{}:{}:{}: ".format(self.inputfilepath, result["ast_node"].line, result["ast_node"].column) + bcolors.NOTE + "note: " + bcolors.RESET 
                + "previous declaration of '\033[1;97m{}\033[0m'; with type '\033[1;97m{}\033[0m'".format(result["ast_node"].id, result["ast_node"].type))
                print(" "*(5-len(str(result["ast_node"].line))) + str(result["ast_node"].line) + " | " + self.lines[result["ast_node"].line-1][:result["ast_node"].column] + bcolors.NOTE + self.lines[result["ast_node"].line-1][result["ast_node"].column] + bcolors.RESET + self.lines[result["ast_node"].line-1][result["ast_node"].column+1:-1])
                print(" "*(5) + " | " + " "*(result["ast_node"].column) + bcolors.NOTE + "^" + bcolors.RESET)

                self.buffer["errors"].append(bcolors.BOLD + "{}:{}:{}: ".format(self.inputfilepath, node.line, node.column) + bcolors.FAIL + "error: " + bcolors.RESET 
                + "conflicting types for '\033[1;97m{}\033[0m'; have '\033[1;97m{}\033[0m'".format(node.id, node.type)
                + " "*(5-len(str(node.line))) + str(node.line) + " | " + self.lines[node.line-1][:node.column] + bcolors.FAIL + self.lines[node.line-1][node.column] + bcolors.RESET + self.lines[node.line-1][node.column+1:-1] 
                + " "*(5) + " | " + " "*(node.column) + bcolors.FAIL + "^" + bcolors.RESET
                 + bcolors.BOLD + "{}:{}:{}: ".format(self.inputfilepath, result["ast_node"].line, result["ast_node"].column) + bcolors.NOTE + "note: " + bcolors.RESET 
                + "previous declaration of '\033[1;97m{}\033[0m'; with type '\033[1;97m{}\033[0m'".format(result["ast_node"].id, result["ast_node"].type)
                + " "*(5-len(str(result["ast_node"].line))) + str(result["ast_node"].line) + " | " + self.lines[result["ast_node"].line-1][:result["ast_node"].column] + bcolors.NOTE + self.lines[result["ast_node"].line-1][result["ast_node"].column] + bcolors.RESET + self.lines[result["ast_node"].line-1][result["ast_node"].column+1:-1] 
                + " "*(5) + " | " + " "*(result["ast_node"].column) + bcolors.NOTE + "^" + bcolors.RESET)
            elif result["global"]:
                print("got ya")
            else:
                print( bcolors.BOLD + "{}:{}:{}: ".format(self.inputfilepath, node.line, node.column) + bcolors.FAIL + "error: " + bcolors.RESET 
                + "redeclaration of '\033[1;97m{}\033[0m'".format(node.id))
                print(" "*(5-len(str(node.line))) + str(node.line) + " | " + self.lines[node.line-1][:node.column] + bcolors.FAIL + self.lines[node.line-1][node.column] + bcolors.RESET + self.lines[node.line-1][node.column+1:-1])
                print(" "*(5) + " | " + " "*(node.column) + bcolors.FAIL + "^" + bcolors.RESET)
                print( bcolors.BOLD + "{}:{}:{}: ".format(self.inputfilepath, result["ast_node"].line, result["ast_node"].column) + bcolors.NOTE + "note: " + bcolors.RESET 
                + "previous declaration of '\033[1;97m{}\033[0m' with type '\033[1;97m{}\033[0m'".format(result["ast_node"].id, result["ast_node"].type))
                print(" "*(5-len(str(result["ast_node"].line))) + str(result["ast_node"].line) + " | " + self.lines[result["ast_node"].line-1][:result["ast_node"].column] + bcolors.NOTE + self.lines[result["ast_node"].line-1][result["ast_node"].column] + bcolors.RESET + self.lines[result["ast_node"].line-1][result["ast_node"].column+1:-1])
                print(" "*(5) + " | " + " "*(result["ast_node"].column) + bcolors.NOTE + "^" + bcolors.RESET)

                self.buffer["errors"].append(bcolors.BOLD + "{}:{}:{}: ".format(self.inputfilepath, node.line, node.column) + bcolors.FAIL + "error: " + bcolors.RESET 
                + "redeclaration of '\033[1;97m{}\033[0m'".format(node.id)
                + " "*(5-len(str(node.line))) + str(node.line) + " | " + self.lines[node.line-1][:node.column] + bcolors.FAIL + self.lines[node.line-1][node.column] + bcolors.RESET + self.lines[node.line-1][node.column+1:-1] 
                + " "*(5) + " | " + " "*(node.column) + bcolors.FAIL + "^" + bcolors.RESET
                 + bcolors.BOLD + "{}:{}:{}: ".format(self.inputfilepath, result["ast_node"].line, result["ast_node"].column) + bcolors.NOTE + "note: " + bcolors.RESET 
                + "previous declaration of '\033[1;97m{}\033[0m' with type '\033[1;97m{}\033[0m'".format(result["ast_node"].id, result["ast_node"].type)
                + " "*(5-len(str(result["ast_node"].line))) + str(result["ast_node"].line) + " | " + self.lines[result["ast_node"].line-1][:result["ast_node"].column] + bcolors.NOTE + self.lines[result["ast_node"].line-1][result["ast_node"].column] + bcolors.RESET + self.lines[result["ast_node"].line-1][result["ast_node"].column+1:-1] 
                + " "*(5) + " | " + " "*(result["ast_node"].column) + bcolors.NOTE + "^" + bcolors.RESET)

        if not node.init_expr is None:
            self.visit(node.init_expr)
    
    def visitImplicitCastExprNode(self, node):
        if node.cast == "<FloatingToIntegral>":
            print("{}:{}:{}: ".format(self.inputfilepath, node.line, node.column) + bcolors.WARNING + "warning: " + bcolors.RESET 
            + "implicit conversion from '{}' to '{}' may change value".format(node.child.type, node.type))
            self.buffer["warnings"].append("{}:{}:{}: ".format(self.inputfilepath, node.line, node.column) + bcolors.WARNING + "warning: " + bcolors.RESET 
            + "implicit conversion from '{}' to '{}' may change value".format(node.child.type, node.type))

    def visitBinExprNode(self, node):
        if node.operation in ["==", "!=", ">", "<", ">=", "<="]:
            if node.lhs_child.parseType()[1] and node.rhs_child.parseType()[1]:
                print( bcolors.BOLD + "{}:{}:{}: ".format(self.inputfilepath, node.line, node.column) + bcolors.FAIL + "error: " + bcolors.RESET 
                + "comparison between two arrays not supported")
                print(" "*(5-len(str(node.line))) + str(node.line) + " | " + self.lines[node.line-1][:node.column] + bcolors.FAIL + self.lines[node.line-1][node.column] + bcolors.RESET + self.lines[node.line-1][node.column+1:-1])
                print(" "*(5) + " | " + " "*(node.column) + bcolors.FAIL + "^" + bcolors.RESET)
                
                self.buffer["errors"].append(bcolors.BOLD + "{}:{}:{}: ".format(self.inputfilepath, node.line, node.column) + bcolors.FAIL + "error: " + bcolors.RESET 
                + "comparison between two arrays not supported"
                + " "*(5-len(str(node.line))) + str(node.line) + " | " + self.lines[node.line-1][:node.column] + bcolors.FAIL + self.lines[node.line-1][node.column] + bcolors.RESET + self.lines[node.line-1][node.column+1:-1] 
                + " "*(5) + " | " + " "*(node.column) + bcolors.FAIL + "^" + bcolors.RESET)
from ASTVisitor import ASTVisitor
from ASTNodes import *
import copy

class MIPSGenerator(ASTVisitor):

    def __init__(self):
        self.buffer = {}
        self.buffer["data"] = ".data\n"
        self.buffer["str"] = ""
        self.buffer["float"] = ""
        self.buffer["text"] = ".text\nmain:\n"
        self.buffer["exit"] = "\tli $v0, 10\n\tsyscall\n"
        self.register = -1
        self.str_constants = {}
        self.float_constants = {}
        self.call_count = 0
        self.conv_count = 0
        self.register_count = 0
        self.lor_count = 0
        self.land_count = 0
        self.inc_count = 0
        self.dec_count = 0
        self.if_count = 0
        self.while_count = 0
        self.current_label = None
        self.STT = None
        self.idshadowing = {}
        self.idcount = {}
        self.arrayidx_count = 0
        self.loop_stack = []
        self.absolute_br = []

    def loadSTT(self, STT):
        self.STT = copy.deepcopy(STT)

    def generateFile(self, filename="main"):
        output = open(str(filename+".asm"), 'w')
        output.write(self.buffer["data"] + self.buffer["str"] + self.buffer["float"] + "\n\n" + self.buffer["text"] + self.buffer["exit"])
        output.close()
        
    def visitProgNode(self, node):
        for DeclChild in node.children:
            self.visit(DeclChild)
        
        # self.buffer["main"] += "\t\tret i32 0\n}\n"
        return 0

    def visitFunctionDeclNode(self, node):
        if node.init:    
            self.STT.child_scope()
            self.visit(node.children[-1])
            self.STT.prev_scope()

    def visitScopeStmtNode(self, node):
        for StmtNode in node.children:
            self.visit(StmtNode)
    
    def visitDeclStmtNode(self, node):
        self.visit(node.child)
    
    def visitExprStmtNode(self, node):
        self.visit(node.child)
    
    def visitCallExprNode(self, node):
        # Save contents of $a0-$a3 into memory if caller needs them later.
        # Same for $t0-$t9 and $v0,$v1. Restore them after call.
        if node.children[0].id == "printf":
            # First edition of this codeblock, probably very inefficient.
            format_flag = False
            processed_string = []
            actual_text = []
            temp = ""
            for char in node.children[1].child.buffer:
                if char == '%':
                    format_flag = True
                    continue
                if format_flag:
                    if char == 'c':
                        if not temp == "":
                            actual_text.append(temp)
                        actual_text.append(11)
                        temp = ""
                    elif char == 'd':
                        if not temp == "":
                            actual_text.append(temp)
                        actual_text.append(1)
                        temp = ""
                    elif char == 'f':
                        if not temp == "":
                            actual_text.append(temp)
                        actual_text.append(2)
                        temp = ""
                    elif char == 's':
                        if not temp == "":
                            actual_text.append(temp)
                        actual_text.append(4)
                        temp = ""
                    else:
                        raise Exception("Unknown formatting.")
                    format_flag = False
                else:
                    temp += char
            if not temp == "":
                actual_text.append(temp)

            for part in actual_text:
                if type(part) is int:
                    processed_string.append(part)
                    continue
                if part in self.str_constants:
                    processed_string.append(self.str_constants[part])
                else:
                    self.str_constants[part] = "str." + str(len(self.str_constants))
                    self.buffer["str"] += self.str_constants[part] + ': .asciiz "'
                    self.buffer["str"] += part + '"\n'
                    processed_string.append(self.str_constants[part])
            
            format_arg = 2
            for part in processed_string:
                if type(part) is int:
                    self.buffer["text"] += "\tli $v0, {}\n".format(part)
                    self.visit(node.children[format_arg])
                    format_arg += 1
                    if part == 2:
                        # load format_value to $f12
                        self.buffer["text"] += "\tmtc1 $t0, $f0\n" 
                        self.buffer["text"] += "\tmov.s $f12, $f0\n\tsyscall\n" 
                    else:
                        # load format_value to $a0
                        self.buffer["text"] += "\tmove $a0, $t0\n\tsyscall\n" 
                else:
                    self.buffer["text"] += "\tli $v0, 4\n\tla $a0, " + part + "\n\tsyscall\n"



    def visitBinExprNode(self, node):
        # Save registers $s0, $s1
        self.buffer["text"] += "\t# Entering BinExprNode.\n"
        self.buffer["text"] += "\tsubi $sp, $sp, 8\n"
        self.buffer["text"] += "\tsw $s0, 4($sp)\n"
        self.buffer["text"] += "\tsw $s1, 0($sp)\n"

        self.visit(node.lhs_child)
        self.buffer["text"] += "\tmove $s0, $t0\n"
        self.visit(node.rhs_child)
        self.buffer["text"] += "\tmove $s1, $t0\n"
        if node.lhs_child.type == "float" or node.rhs_child.type == "float":
            # Need float instructions
            if node.lhs_child.type == "float":
                self.buffer["text"] += "\tmtc1 $s0, $f0\n" 
            elif node.lhs_child.type == "int":
                self.buffer["text"] += "\tmtc1 $s0, $f0\n\tcvt.s.w $f0, $f0\n"
            elif node.lhs_child.type == "char":
                pass
            else:
                pass

            if node.rhs_child.type == "float":
                self.buffer["text"] += "\tmtc1 $s1, $f1\n"
            elif node.rhs_child.type == "int":
                self.buffer["text"] += "\tmtc1 $s1, $f1\n\tcvt.s.w $f1, $f1\n"
            elif node.rhs_child.type == "char":
                pass
            else:
                pass

            if node.operation == "+":
                self.buffer["text"] += "\tadd.s $f0, $f0, $f1\n"
            elif node.operation == "-":
                self.buffer["text"] += "\tsub.s $f0, $f0, $f1\n"
            elif node.operation == "*":
                self.buffer["text"] += "\tmul.s $f0, $f0, $f1\n"
            elif node.operation == "/":
                self.buffer["text"] += "\tdiv.s $f0, $f0, $f1\n"

            self.buffer["text"] += "\tmfc1 $t0, $f0\n"
        else:
            # Need int instructions
            if node.operation == "+":
                self.buffer["text"] += "\tadd $t0, $s0, $s1\n"
            elif node.operation == "-":
                self.buffer["text"] += "\tsub $t0, $s0, $s1\n"
            elif node.operation == "*":
                self.buffer["text"] += "\tmul $t0, $s0, $s1\n"
            elif node.operation == "/":
                self.buffer["text"] += "\tdiv $t0, $s0, $s1\n"
        
        # Restore registers $s0, $s1
        self.buffer["text"] += "\tlw $s0, 4($sp)\n"
        self.buffer["text"] += "\tlw $s1, 0($sp)\n"
        self.buffer["text"] += "\taddi $sp, $sp, 8\n"
        self.buffer["text"] += "\t# Exiting BinExprNode.\n"

    def visitImplicitCastExprNode(self, node):
        pass

    def visitIntegerLiteralNode(self, node):
        self.buffer["text"] += "\tli $t0, {}\n".format(node.value)
    
    def visitFloatingLiteralNode(self, node):
        if node.value in self.float_constants:
            self.buffer["text"] += "\tl.s $f0, {}\n".format(self.float_constants[node.value])
            self.buffer["text"] += "\tmfc1 $t0, $f0\n" 
        else:
            self.float_constants[node.value] = "float." + str(len(self.float_constants))
            self.buffer["float"] += str(self.float_constants[node.value]) + ': .float '
            self.buffer["float"] += str(node.value) + '\n'
            self.buffer["text"] += "\tl.s $f0, {}\n".format(self.float_constants[node.value])
            self.buffer["text"] += "\tmfc1 $t0, $f0\n" 


            
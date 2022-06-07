from ASTVisitor import ASTVisitor
from ASTNodes import *
import copy
from collections import deque

class MIPSGeneratorRegisters():

    def __init__(self):
        self.active_registers = deque([])   # Queue
        self.standby_registers = deque(["$s7", "$s6", "$s5", "$s4", "$s3", "$s2", "$s1", "$s0", "$t9", "$t8", "$t7", "$t6", "$t5", "$t4", "$t3"])  # Stack
        self.state = {}                     # symbol.serial -> register
        self.reverse_state = {}             # register -> symbol.serial

    def lookup(self, serial):
        if serial in self.state.keys():
            self.active_registers.remove(self.state[serial])
            self.active_registers.append(self.state[serial])
            return self.state[serial]
        else:
            return None

    def deprecate(self, register=None, serial=None):
        if register is None and serial is None:
            raise Exception("Misuse of deprecate method")
        if register is None:
            if serial in self.state.keys():
                self.reverse_state.remove(self.state[serial])
                self.active_registers.remove(self.state[serial])
                self.standby_registers.append(self.state[serial])
                self.state.remove(serial)
                return None
            else:
                return None
        else:
            pass
    
    def insert(self, serial):
        # Check if any standby_registers
        if len(self.standby_registers) > 0:
            register = self.standby_registers.pop()
            self.active_registers.append(register)
            self.state[serial] = register
            self.reverse_state[register] = serial
            return register
        else:
            # No standby, get least recently used active_register
            register = self.active_registers.popleft()
            self.state.remove(self.reverse_state[register])
            self.state[serial] = register
            self.reverse_state[register] = serial
            return register

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
        self.registers = MIPSGeneratorRegisters()
        self.call_count = 0
        self.conv_count = 0
        self.register_count = 0
        self.lor_count = 0
        self.land_count = 0
        self.lnot_count = 0
        self.fcmp_count = 0
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

    def storeVar(self, result, register):
        # Check if variable somewhere in registers
        if self.registers.lookup(result["serial"]) is None:
            # Not in registers
            self.buffer["text"] += "\tsw {}, {}($fp)\n".format(register, result["mem_offset"])
        else:
            # Data in register will be outdated thus remove association
            self.registers.deprecate(serial=result["serial"])
            self.buffer["text"] += "\tsw {}, {}($fp)\n".format(register, result["mem_offset"])

    def loadVar(self, result):
        # First check if present in registers
        register = self.registers.lookup(result["serial"])
        if register is None:
            # If not present, choose register to load it into
            register = self.registers.insert(result["serial"])
            # Load into chosen register
            self.buffer["text"] += "\tlw {}, {}($fp)\n".format(register, result["mem_offset"])
            return register
        else:
            # Found in register.
            return register
        
    def visitProgNode(self, node):
        for DeclChild in node.children:
            self.visit(DeclChild)
        
        return 0

    def visitVarDeclNode(self, node):
        pass

    def visitFunctionDeclNode(self, node):
        if node.init:    
            self.STT.child_scope()
            self.visit(node.children[-1])
            self.STT.prev_scope()

    def visitScopeStmtNode(self, node):
        memory_offset = -44 
        for symbol_id in self.STT.current_symboltablenode.hashtable.keys():
            # Allocate memory for every variable, store offset from frame pointer as attribute of symbol.
            # Accumulate the total memory required, to move stack pointer.
            result = self.STT.lookup(symbol_id)
            type_temp = result["ast_node"].parseType()
            if type_temp[1]:
                memory_size = result["ast_node"].getLen() * 4
                self.STT.set_attribute(symbol_id, "mem_offset", memory_offset)
                memory_offset -= memory_size
            else:
                self.STT.set_attribute(symbol_id, "mem_offset", memory_offset)
                memory_offset -= 4
            print("{} {}($fp)".format(symbol_id, result["mem_offset"]))
        
        # Store previous frame pointer
        self.buffer["text"] += "\tsw $fp, 0($sp)\t\t# Push old $fp ( control-link )\n"
        self.buffer["text"] += "\tsw $fp, -4($sp)\t\t# Push activation link ( static-link )\n"
        # Set framepointer for current frame
        self.buffer["text"] += "\tmove $fp, $sp\t\t# Set $fp of new frame\n"
        # Move stackpointer
        self.buffer["text"] += "\taddi $sp, $sp, {}\t# Allocate {} bytes on the stack\n".format(memory_offset, memory_offset)
        # Store $s0-s7 and $ra
        self.buffer["text"] += "\tsw $ra, -8($fp)\t\t# Store value of return address\n"
        self.buffer["text"] += "\tsw $s0, -12($fp)\t# Save incase it gets used locally\n"
        self.buffer["text"] += "\tsw $s1, -16($fp)\t# Save incase it gets used locally\n"
        self.buffer["text"] += "\tsw $s2, -20($fp)\t# Save incase it gets used locally\n"
        self.buffer["text"] += "\tsw $s3, -24($fp)\t# Save incase it gets used locally\n"
        self.buffer["text"] += "\tsw $s4, -28($fp)\t# Save incase it gets used locally\n"
        self.buffer["text"] += "\tsw $s5, -32($fp)\t# Save incase it gets used locally\n"
        self.buffer["text"] += "\tsw $s6, -36($fp)\t# Save incase it gets used locally\n"
        self.buffer["text"] += "\tsw $s7, -40($fp)\t# Save incase it gets used locally\n"

        for StmtNode in node.children:
            self.visit(StmtNode)

        print("Active registers: ", self.registers.active_registers)

        self.buffer["text"] += "\tlw $ra, -8($fp)\t\t# Restore saved return address\n"
        self.buffer["text"] += "\tlw $s0, -12($fp)\t# Restore saved register\n"
        self.buffer["text"] += "\tlw $s1, -16($fp)\t# Restore saved register\n"
        self.buffer["text"] += "\tlw $s2, -20($fp)\t# Restore saved register\n"
        self.buffer["text"] += "\tlw $s3, -24($fp)\t# Restore saved register\n"
        self.buffer["text"] += "\tlw $s4, -28($fp)\t# Restore saved register\n"
        self.buffer["text"] += "\tlw $s5, -32($fp)\t# Restore saved register\n"
        self.buffer["text"] += "\tlw $s6, -36($fp)\t# Restore saved register\n"
        self.buffer["text"] += "\tlw $s7, -40($fp)\t# Restore saved register\n"
        self.buffer["text"] += "\tmove $sp, $fp\t\t# Deallocate {} bytes from the stack\n".format(memory_offset)
        self.buffer["text"] += "\tlw $fp, 0($sp)\t\t# Restore old framepointer\n"
    
    def visitDeclStmtNode(self, node):
        var = node.child
        result = self.STT.lookup(var.id)
        type_temp = var.parseType()
        if var.init:
            if type_temp[1]:
                pass
            else:
                if issubclass(type(var.init_expr), LiteralNode):
                    if type_temp[2] == "float":
                        if var.init_expr.value in self.float_constants:
                            self.buffer["text"] += "\tl.s $f0, {}\n".format(self.float_constants[var.init_expr.value])
                            self.buffer["text"] += "\tmfc1 $t0, $f0\n" 
                            self.buffer["text"] += "\tsw $t0, {}($fp)\n".format(result["mem_offset"]) 
                        else:
                            self.float_constants[var.init_expr.value] = "float." + str(len(self.float_constants))
                            self.buffer["float"] += str(self.float_constants[var.init_expr.value]) + ': .float '
                            self.buffer["float"] += str(var.init_expr.value) + '\n'
                            self.buffer["text"] += "\tl.s $f0, {}\n".format(self.float_constants[var.init_expr.value])
                            self.buffer["text"] += "\tmfc1 $t0, $f0\n" 
                            self.buffer["text"] += "\tsw $t0, {}($fp)\n".format(result["mem_offset"]) 
                    else:
                        self.buffer["text"] += "\tli $t0, {}\n".format(var.init_expr.value)
                        self.buffer["text"] += "\tsw $t0, {}($fp)\n".format(result["mem_offset"])
                        # self.buffer["text"] += "\t" + "store "+ llvm_type +" " + str(var.init_expr.value)
                        # self.buffer["text"] += ", "+ llvm_type +"* %" + str(self.idshadowing[serial]) + ", align "+ llvm_align +"\n"
                else:
                    register = self.visit(var.init_expr)
                    self.buffer["text"] += "\tsw {}, {}($fp)\n".format(register, result["mem_offset"]) 
                    # self.buffer["text"] += "\t" + "store "+ llvm_type +" %" + str(self.register_count-1)
                    # self.buffer["text"] += ", "+ llvm_type +"* %" + str(self.idshadowing[serial]) + ", align "+ llvm_align +"\n"
        else:
            if type_temp[2] == "char":
                pass
            elif type_temp[2] == "int":
                pass
            elif type_temp[2] == "float":
                pass
            else:
                raise Exception("¸„٭⊹✡•~⍣°”ˆ˜¨ 乇尺尺の尺 ¨˜ˆ”°⍣~•✡⊹٭„¸")
        self.visit(node.child)
    
    def visitExprStmtNode(self, node):
        self.visit(node.child)

    def visitIfStmtNode(self, node):
        pass
    
    def visitCallExprNode(self, node):
        # Save contents of $a0-$a3 into memory if caller needs them later.
        # Same for $t0-$t9 and $v0,$v1. Restore them after call.
        if node.children[0].id == "printf":
            # First edition of this codeblock, probably very inefficient.
            format_flag = False
            processed_string = []
            actual_text = []
            temp = ""
            for char in node.children[1].child.rawbuffer:
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
                    register = self.visit(node.children[format_arg])
                    format_arg += 1
                    if part == 2:
                        # load format_value to $f12
                        self.buffer["text"] += "\tmtc1 {}, $f0\n".format(register) 
                        self.buffer["text"] += "\tmov.s $f12, $f0\n\tsyscall\n" 
                    else:
                        # load format_value to $a0
                        self.buffer["text"] += "\tmove $a0, {}\n\tsyscall\n".format(register) 
                else:
                    self.buffer["text"] += "\tli $v0, 4\n\tla $a0, " + part + "\n\tsyscall\n"

    def visitUnaryExprNode(self, node):
        # Save register $s0
        self.buffer["text"] += "\t# Entering UnaryExprNode.\n"
        # self.buffer["text"] += "\tsubi $sp, $sp, 4\n"
        # self.buffer["text"] += "\tsw $s0, 0($sp)\n"

        self.visit(node.child)

        if node.prefix:
            if node.child.type == "float":
                self.buffer["text"] += "\tmtc1 $t0, $f0\n"

                if node.operation == "!":
                    self.buffer["text"] += "\tmfc1 $zero, $f2\n\tcvt.s.w $f2, $f2\n"
                    # Compare if child == 0, this sets flag in coprocessor if true.
                    # Branch to lnot.x.true if set.
                    self.buffer["text"] += "\tc.eq.s $f0, $f2\n"
                    self.buffer["text"] += "\tbc1t lnot.{}.true\n".format(self.lnot_count)
                     # lnot.x.false block
                    self.buffer["text"] += "lnot.{}.false:\n".format(self.lnot_count)
                    self.buffer["text"] += "\tli $t0, 0\n"
                    self.buffer["text"] += "\tb lnot.{}.end\n".format(self.lnot_count)
                    # lnot.x.true block
                    self.buffer["text"] += "lnot.{}.true:\n".format(self.lnot_count)
                    self.buffer["text"] += "\tli $t0, 1\n"
                    # lnot.x.end block
                    self.buffer["text"] += "lnot.{}.end:\n".format(self.lnot_count)
                    self.lnot_count += 1
                elif node.operation == "-":
                    pass
            else:
                if node.operation == "!":
                    # Branch to lnot.x.true if $t0 == 0.
                    self.buffer["text"] += "\tbeq $t0, $zero, lnot.{}.true\n".format(self.lnot_count)
                    # lnot.x.false block
                    self.buffer["text"] += "lnot.{}.false:\n".format(self.lnot_count)
                    self.buffer["text"] += "\tli $t0, 0\n"
                    self.buffer["text"] += "\tb lnot.{}.end\n".format(self.lnot_count)
                    # lnot.x.true block
                    self.buffer["text"] += "lnot.{}.true:\n".format(self.lnot_count)
                    self.buffer["text"] += "\tli $t0, 1\n"
                    # lnot.x.end block
                    self.buffer["text"] += "lnot.{}.end:\n".format(self.lnot_count)
                    self.lnot_count += 1
                elif node.operation == "-":
                    pass
        else:
            pass

        # Restore register $s0
        # self.buffer["text"] += "\tlw $s0, 0($sp)\n"
        # self.buffer["text"] += "\taddi $sp, $sp, 4\n"
        self.buffer["text"] += "\t# Exiting UnaryExprNode.\n"
        return "$t0"

    def visitBinExprNode(self, node):

        if node.operation == "=":
            # Deal with lhs
            if type(node.lhs_child) is DeclRefExprNode:
                result = self.STT.lookup(node.lhs_child.ref["ast_node"].id)
                register = self.visit(node.rhs_child)
                self.storeVar(result, register)
                return None
            else:
                raise Exception("Not yet")


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

            if node.operation in ["+", "-", "*", "/"]:
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
                if node.operation == "&&":
                    self.buffer["text"] += "\tmfc1 $zero, $f2\n\tcvt.s.w $f2, $f2\n"
                    # Compare if lhs == 0, this sets flag in coprocessor if true.
                    # Branch to land.x.false if set.
                    self.buffer["text"] += "\tc.eq.s $f0, $f2\n"
                    self.buffer["text"] += "\tbc1t land.{}.false\n".format(self.land_count)
                    # Compare if rhs == 0, this sets flag in coprocessor if true.
                    # Branch to land.x.true if not set.
                    self.buffer["text"] += "\tc.eq.s $f1, $f2\n"
                    self.buffer["text"] += "\tbc1f land.{}.true\n".format(self.land_count)
                    # land.x.false block
                    self.buffer["text"] += "land.{}.false:\n".format(self.land_count)
                    self.buffer["text"] += "\tli $t0, 0\n"
                    self.buffer["text"] += "\tb land.{}.end\n".format(self.land_count)
                    # land.x.true block
                    self.buffer["text"] += "land.{}.true:\n".format(self.land_count)
                    self.buffer["text"] += "\tli $t0, 1\n"
                    # land.x.end block
                    self.buffer["text"] += "land.{}.end:\n".format(self.land_count)
                    self.land_count += 1
                elif node.operation == "||":
                    self.buffer["text"] += "\tmfc1 $zero, $f2\n\tcvt.s.w $f2, $f2\n"
                    # Compare if lhs == 0, this sets flag in coprocessor if true.
                    # Branch to lor.x.true if not set.
                    self.buffer["text"] += "\tc.eq.s $f0, $f2\n"
                    self.buffer["text"] += "\tbc1f lor.{}.true\n".format(self.lor_count)
                    # Compare if rhs == 0, this sets flag in coprocessor if true.
                    # Branch to lor.x.true if not set.
                    self.buffer["text"] += "\tc.eq.s $f1, $f2\n"
                    self.buffer["text"] += "\tbc1f lor.{}.true\n".format(self.lor_count)
                    # lor.x.false block
                    self.buffer["text"] += "lor.{}.false:\n".format(self.lor_count)
                    self.buffer["text"] += "\tli $t0, 0\n"
                    self.buffer["text"] += "\tb lor.{}.end\n".format(self.lor_count)
                    # lor.x.true block
                    self.buffer["text"] += "lor.{}.true:\n".format(self.lor_count)
                    self.buffer["text"] += "\tli $t0, 1\n"
                    # lor.x.end block
                    self.buffer["text"] += "lor.{}.end:\n".format(self.lor_count)
                    self.lor_count += 1
                elif node.operation == ">":
                    self.buffer["text"] += "\tc.lt.s $f1, $f0\n"
                    self.buffer["text"] += "\tbc1t fcmp.{}.true\n".format(self.fcmp_count)
                    # fcmp.x.false block
                    self.buffer["text"] += "fcmp.{}.false:\n".format(self.fcmp_count)
                    self.buffer["text"] += "\tli $t0, 0\n"
                    self.buffer["text"] += "\tb fcmp.{}.end\n".format(self.fcmp_count)
                    # fcmp.x.true block
                    self.buffer["text"] += "fcmp.{}.true:\n".format(self.fcmp_count)
                    self.buffer["text"] += "\tli $t0, 1\n"
                    # fcmp.x.end block
                    self.buffer["text"] += "fcmp.{}.end:\n".format(self.fcmp_count)
                    self.fcmp_count += 1
                elif node.operation == "<":
                    self.buffer["text"] += "\tc.lt.s $f0, $f1\n"
                    self.buffer["text"] += "\tbc1t fcmp.{}.true\n".format(self.fcmp_count)
                    # fcmp.x.false block
                    self.buffer["text"] += "fcmp.{}.false:\n".format(self.fcmp_count)
                    self.buffer["text"] += "\tli $t0, 0\n"
                    self.buffer["text"] += "\tb fcmp.{}.end\n".format(self.fcmp_count)
                    # fcmp.x.true block
                    self.buffer["text"] += "fcmp.{}.true:\n".format(self.fcmp_count)
                    self.buffer["text"] += "\tli $t0, 1\n"
                    # fcmp.x.end block
                    self.buffer["text"] += "fcmp.{}.end:\n".format(self.fcmp_count)
                    self.fcmp_count += 1
                elif node.operation == ">=":
                    self.buffer["text"] += "\tc.le.s $f1, $f0\n"
                    self.buffer["text"] += "\tbc1t fcmp.{}.true\n".format(self.fcmp_count)
                    # fcmp.x.false block
                    self.buffer["text"] += "fcmp.{}.false:\n".format(self.fcmp_count)
                    self.buffer["text"] += "\tli $t0, 0\n"
                    self.buffer["text"] += "\tb fcmp.{}.end\n".format(self.fcmp_count)
                    # fcmp.x.true block
                    self.buffer["text"] += "fcmp.{}.true:\n".format(self.fcmp_count)
                    self.buffer["text"] += "\tli $t0, 1\n"
                    # fcmp.x.end block
                    self.buffer["text"] += "fcmp.{}.end:\n".format(self.fcmp_count)
                    self.fcmp_count += 1
                elif node.operation == "<=":
                    self.buffer["text"] += "\tc.le.s $f0, $f1\n"
                    self.buffer["text"] += "\tbc1t fcmp.{}.true\n".format(self.fcmp_count)
                    # fcmp.x.false block
                    self.buffer["text"] += "fcmp.{}.false:\n".format(self.fcmp_count)
                    self.buffer["text"] += "\tli $t0, 0\n"
                    self.buffer["text"] += "\tb fcmp.{}.end\n".format(self.fcmp_count)
                    # fcmp.x.true block
                    self.buffer["text"] += "fcmp.{}.true:\n".format(self.fcmp_count)
                    self.buffer["text"] += "\tli $t0, 1\n"
                    # fcmp.x.end block
                    self.buffer["text"] += "fcmp.{}.end:\n".format(self.fcmp_count)
                    self.fcmp_count += 1
                elif node.operation == "!=":
                    self.buffer["text"] += "\tc.eq.s $f0, $f1\n"
                    self.buffer["text"] += "\tbc1f fcmp.{}.true\n".format(self.fcmp_count)
                    # fcmp.x.false block
                    self.buffer["text"] += "fcmp.{}.false:\n".format(self.fcmp_count)
                    self.buffer["text"] += "\tli $t0, 0\n"
                    self.buffer["text"] += "\tb fcmp.{}.end\n".format(self.fcmp_count)
                    # fcmp.x.true block
                    self.buffer["text"] += "fcmp.{}.true:\n".format(self.fcmp_count)
                    self.buffer["text"] += "\tli $t0, 1\n"
                    # fcmp.x.end block
                    self.buffer["text"] += "fcmp.{}.end:\n".format(self.fcmp_count)
                    self.fcmp_count += 1
        else:
            # Need int instructions
            if node.operation in ["+", "-", "*", "/"]:
                if node.operation == "+":
                    self.buffer["text"] += "\tadd $t0, $s0, $s1\n"
                elif node.operation == "-":
                    self.buffer["text"] += "\tsub $t0, $s0, $s1\n"
                elif node.operation == "*":
                    self.buffer["text"] += "\tmul $t0, $s0, $s1\n"
                elif node.operation == "/":
                    self.buffer["text"] += "\tdiv $t0, $s0, $s1\n"
            else:
                if node.operation == "&&":
                    # Branch to land.x.false if == 0.
                    self.buffer["text"] += "\tbeq $s0, $zero land.{}.false\n".format(self.land_count)
                    # Branch to land.x.true if != 0.
                    self.buffer["text"] += "\tbne $s1, $zero land.{}.true\n".format(self.land_count)
                    # land.x.false block
                    self.buffer["text"] += "land.{}.false:\n".format(self.land_count)
                    self.buffer["text"] += "\tli $t0, 0\n"
                    self.buffer["text"] += "\tb land.{}.end\n".format(self.land_count)
                    # land.x.true block
                    self.buffer["text"] += "land.{}.true:\n".format(self.land_count)
                    self.buffer["text"] += "\tli $t0, 1\n"
                    # land.x.end block
                    self.buffer["text"] += "land.{}.end:\n".format(self.land_count)
                    self.land_count += 1
                elif node.operation == "||":
                    # Branch to lor.x.true if $s0 != 0
                    self.buffer["text"] += "\tbne $s0, $zero lor.{}.true\n".format(self.lor_count)
                    # Branch to lor.x.true if $s1 != 0
                    self.buffer["text"] += "\tbne $s1, $zero lor.{}.true\n".format(self.lor_count)
                    # lor.x.false block
                    self.buffer["text"] += "lor.{}.false:\n".format(self.lor_count)
                    self.buffer["text"] += "\tli $t0, 0\n"
                    self.buffer["text"] += "\tb lor.{}.end\n".format(self.lor_count)
                    # lor.x.true block
                    self.buffer["text"] += "lor.{}.true:\n".format(self.lor_count)
                    self.buffer["text"] += "\tli $t0, 1\n"
                    # lor.x.end block
                    self.buffer["text"] += "lor.{}.end:\n".format(self.lor_count)
                    self.lor_count += 1
                elif node.operation == ">":
                    self.buffer["text"] += "\tslt $t0, $s1, $s0\n"
                elif node.operation == "<":
                    self.buffer["text"] += "\tslt $t0, $s0, $s1\n"
                elif node.operation == ">=":
                    self.buffer["text"] += "\tsle $t0, $s1, $s0\n"
                elif node.operation == "<=":
                    self.buffer["text"] += "\tsle $t0, $s0, $s1\n"
                elif node.operation == "!=":
                    self.buffer["text"] += "\tsne $t0, $s0, $s1\n"

        # Restore registers $s0, $s1
        self.buffer["text"] += "\tlw $s0, 4($sp)\n"
        self.buffer["text"] += "\tlw $s1, 0($sp)\n"
        self.buffer["text"] += "\taddi $sp, $sp, 8\n"
        self.buffer["text"] += "\t# Exiting BinExprNode.\n"
        return "$t0"

    def visitDeclRefExprNode(self, node):
        result = self.STT.lookup(node.ref["ast_node"].id)
        if result is None:
            print("gotta fix this")
        else:
            self.buffer["text"] += "\taddi $t0, $fp, {}\n".format(result["mem_offset"])


    def visitImplicitCastExprNode(self, node):
        if node.cast == "<LValueToRValue>":
            if type(node.child) is DeclRefExprNode:
                result = self.STT.lookup(node.child.ref["ast_node"].id)
                if result is None:
                    print("gotta fix this")
                else:
                    return self.loadVar(result) # Should return the register where loaded ex "$t0"
            print("Not fully defined behavior yet")
            self.visit(node.child)
            self.buffer["text"] += "\tlw $t0, 0($t0)\n"
        elif node.cast == "<ArrayToPointerDecay>":
            if type(node.child) is StringLiteralNode:
                return self.visit(node.child)
                


    def visitCharacterLiteralNode(self, node):
        self.buffer["text"] += "\tli $t0, {}\n".format(node.value)
        return "$t0"

    def visitIntegerLiteralNode(self, node):
        self.buffer["text"] += "\tli $t0, {}\n".format(node.value)
        return "$t0"

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
        return "$t0"

    def visitStringLiteralNode(self, node):
        if node.rawvalue in self.str_constants:
            pass
        else:
            self.str_constants[node.rawvalue] = "str." + str(len(self.str_constants))
            self.buffer["str"] += self.str_constants[node.rawvalue] + ': .asciiz "'
            self.buffer["str"] += node.rawvalue +'"\n'
        
        self.buffer["text"] += "\tla $t0, " + self.str_constants[node.rawvalue] + "\n"
        return "$t0"
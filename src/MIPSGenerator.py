from ASTVisitor import ASTVisitor
from ASTNodes import *
import copy
from collections import deque

class MIPSGeneratorRegisters():

    def __init__(self):
        self.active_registers = deque([])   # Queue
        self.standby_registers = deque(["$s7", "$s6", "$s5", "$s4", "$s3", "$s2", "$t9", "$t8", "$t7", "$t6", "$t5", "$t4", "$t3"])  # Stack
        self.state = {}                     # symbol.serial -> register
        self.reverse_state = {}             # register -> symbol.serial

    def lookup(self, serial):
        if serial in self.state.keys():
            self.active_registers.remove(self.state[serial])
            self.active_registers.append(self.state[serial])
            return self.state[serial]
        else:
            return None

    def reset(self):
        self.active_registers = deque([])   # Queue
        self.standby_registers = deque(["$s7", "$s6", "$s5", "$s4", "$s3", "$s2", "$t9", "$t8", "$t7", "$t6", "$t5", "$t4", "$t3"])  # Stack
        self.state = {}                     # symbol.serial -> register
        self.reverse_state = {}             # register -> symbol.serial

    def deprecate(self, register=None, serial=None):
        if register is None and serial is None:
            raise Exception("Misuse of deprecate method")
        if register is None:
            if serial in self.state.keys():
                del self.reverse_state[self.state[serial]]
                self.active_registers.remove(self.state[serial])
                self.standby_registers.append(self.state[serial])
                del self.state[serial]
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
            del self.state[self.reverse_state[register]]
            self.state[serial] = register
            self.reverse_state[register] = serial
            return register

class MIPSGenerator(ASTVisitor):

    def __init__(self):
        self.readbufferpresent = False
        self.buffer = {}
        self.buffer["data"] = ".data\n"
        self.buffer["str"] = ""
        self.buffer["float"] = ""
        self.buffer["global"] = ""
        self.buffer["text"] = ".text\n\tjal main.entry\n\tli $v0, 10\n\tsyscall\n"
        self.buffer["exit"] = ""
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
        self.current_function = None

    def loadSTT(self, STT):
        self.STT = copy.deepcopy(STT)

    def generateFile(self, filename="main"):
        output = open(str(filename+".asm"), 'w')
        output.write(self.buffer["data"] + self.buffer["str"] + ".align 2\n" + self.buffer["float"] + self.buffer["global"] + "\n\n" + self.buffer["text"] + self.buffer["exit"])
        output.close()

    def getResult(self, node):
        if not type(node) is DeclRefExprNode:
            raise Exception("Misuse of method!")
        else:
            temp_symboltable = self.STT.current_symboltablenode
            static_depth = 0
            while not (temp_symboltable is None):
                temp_result = temp_symboltable.lookup(node.ref["ast_node"].id)
                if temp_result is None:
                    temp_symboltable = temp_symboltable.parent
                else:
                    if node.ref["serial"] != temp_result["serial"]:
                        temp_symboltable = temp_symboltable.parent
                    else:
                        return (temp_result, static_depth)
                static_depth += 1

    def storeVar(self, result, register):

        (result, static_depth) = result
        # Check if variable somewhere in registers
        if self.registers.lookup(result["serial"]) is None:
            # Not in registers
            pass
        else:
            # Data in register will be outdated thus remove association
            self.registers.deprecate(serial=result["serial"])

        if result["global"]:
            self.buffer["text"] += "\tsw {}, _{}\n".format(register, result["ast_node"].id)
        else:
            if static_depth == 0:
                self.buffer["text"] += "\tsw {}, {}($fp)\n".format(register, result["mem_offset"])
            else:
                self.buffer["text"] += "\tsw {}, {}($fp)\n".format(register, result["mem_offset"])
                # self.buffer["text"] += "\tlw $t2, -4($fp)\n"
                # static_depth -= 1
                # while static_depth > 0:
                #     self.buffer["text"] += "\tlw $t2, -4($t2)\n"
                #     static_depth -= 1
                # self.buffer["text"] += "\tsw {}, {}($t2)\n".format(register, result["mem_offset"])

    def loadVar(self, result):
        # First check if present in registers
        (result, static_depth) = result
        register = self.registers.lookup(result["serial"])
        if register is None:
            if type(result["ast_node"]) is ParmVarDeclNode:
                register = self.registers.insert(-1)
            # If not present, choose register to load it into
            else:
                register = self.registers.insert(-1)
            # Load into chosen register
            if result["global"]:
                self.buffer["text"] += "\tlw {}, _{}\n".format(register, result["ast_node"].id)
            else:
                if static_depth == 0:
                    self.buffer["text"] += "\tlw {}, {}($fp)\n".format(register, result["mem_offset"])
                else:
                    self.buffer["text"] += "\tlw {}, {}($fp)\n".format(register, result["mem_offset"])
                    # self.buffer["text"] += "\tlw $t2, -4($fp)\n"
                    # static_depth -= 1
                    # while static_depth > 0:
                    #     self.buffer["text"] += "\tlw $t2, -4($t2)\n"
                    # self.buffer["text"] += "\tlw {}, {}($t2)\n".format(register, result["mem_offset"])
            return register
        else:
            # Found in register.
            return register

    def loadAddrVar(self, result):
        (result, static_depth) = result
        register = "$t0"
        if result["global"]:
            self.buffer["text"] += "\tla {}, _{}\n".format(register, result["ast_node"].id)
        else:
            if static_depth == 0:
                self.buffer["text"] += "\taddi {}, $fp, {}\n".format(register, result["mem_offset"])
            else:
                self.buffer["text"] += "\taddi {}, $fp, {}\n".format(register, result["mem_offset"])
                # self.buffer["text"] += "\tlw $t2, -4($fp)\n"
                # static_depth -= 1
                # while static_depth > 0:
                #     self.buffer["text"] += "\tlw $t2, -4($t2)\n"
                # self.buffer["text"] += "\taddi {}, $t2, {}\n".format(register, result["mem_offset"])
        return register
        
    def visitProgNode(self, node):
        for DeclChild in node.children:
            self.visit(DeclChild)
        
        return 0

    def visitVarDeclNode(self, node):
        # Even though all VarDecl use this node, this node is only visited directly for global var
        type_temp = node.parseType()
        if node.type == "char":
            if node.init:
                if type(node.init_expr) is CharacterLiteralNode:
                    self.buffer["global"] += "_{}: .byte {} .align 2\n".format(node.id, node.init_expr.value)
                else:
                    raise Exception("Can only initialise global variables with compiletime constants. Try compiling with optimizations enabled if you turned these off.")
            else:
                self.buffer["global"] += "_{}: .space 1 .align 2\n".format(node.id)
        elif node.type == "float":
            if node.init:
                if type(node.init_expr) is FloatingLiteralNode:
                    self.buffer["global"] += "_{}: .float {}\n".format(node.id, node.init_expr.value)
                else:
                    raise Exception("Can only initialise global variables with compiletime constants. Try compiling with optimizations enabled if you turned these off.")
            else:
                self.buffer["global"] += "_{}: .space 4\n".format(node.id)
        elif node.type == "int":
            if node.init:
                if type(node.init_expr) is IntergerLiteralNode:
                    self.buffer["global"] += "_{}: .word {}\n".format(node.id, node.init_expr.value)
                else:
                    raise Exception("Can only initialise global variables with compiletime constants. Try compiling with optimizations enabled if you turned these off.")
            else:
                self.buffer["global"] += "_{}: .space 4\n".format(node.id)
        else:
            if type_temp[1]:
                self.buffer["global"] += "_{}: .space {}\n".format(node.id, node.getLen()*4)
            else:
                self.buffer["global"] += "_{}: .space 4\n".format(node.id)

    def visitFunctionDeclNode(self, node):
        if node.init:
            self.current_function = node.id
            self.buffer["text"] += "{}.entry:\n".format(node.id)
            self.STT.child_scope()
            memory_offset = self.STT.current_symboltablenode.get_total_size() 
            
            # Store previous frame pointer
            self.buffer["text"] += "\tsw $fp, 0($sp)\t\t# Push old $fp ( control-link )\n"
            self.buffer["text"] += "\tsw $fp, -4($sp)\t\t# Push activation link ( static-link )\n"
            # Set framepointer for current frame
            self.buffer["text"] += "\tmove $fp, $sp\t\t# Set $fp of new frame\n"
            # Move stackpointer
            self.buffer["text"] += "\taddi $sp, $sp, {}\t# Allocate {} bytes on the stack\n".format(memory_offset, memory_offset)
            # Store $s0-s7 and $ra
            self.buffer["text"] += "\tsw $ra, -8($fp)\t\t# Store value of return address\n"
            # self.buffer["text"] += "\tsw $s0, -12($fp)\t# Save incase it gets used locally\n"
            # self.buffer["text"] += "\tsw $s1, -16($fp)\t# Save incase it gets used locally\n"
            # self.buffer["text"] += "\tsw $s2, -20($fp)\t# Save incase it gets used locally\n"
            # self.buffer["text"] += "\tsw $s3, -24($fp)\t# Save incase it gets used locally\n"
            # self.buffer["text"] += "\tsw $s4, -28($fp)\t# Save incase it gets used locally\n"
            # self.buffer["text"] += "\tsw $s5, -32($fp)\t# Save incase it gets used locally\n"
            # self.buffer["text"] += "\tsw $s6, -36($fp)\t# Save incase it gets used locally\n"
            # self.buffer["text"] += "\tsw $s7, -40($fp)\t# Save incase it gets used locally\n"
            param_count = 0
            for Param in node.children[:-1]:
                if param_count > 3:
                    raise Exception("My compiler only supports functions with max 4 arguments")
                result = self.STT.lookup(Param.id)
                self.storeVar((result, 0), "$a{}".format(param_count))
                param_count += 1
            self.visit(node.children[-1])            
            
            self.buffer["text"] += "{}.exit:\n".format(node.id)
            self.buffer["text"] += "\tlw $ra, -8($fp)\t\t# Restore saved return address\n"
            # self.buffer["text"] += "\tlw $s0, -12($fp)\t# Restore saved register\n"
            # self.buffer["text"] += "\tlw $s1, -16($fp)\t# Restore saved register\n"
            # self.buffer["text"] += "\tlw $s2, -20($fp)\t# Restore saved register\n"
            # self.buffer["text"] += "\tlw $s3, -24($fp)\t# Restore saved register\n"
            # self.buffer["text"] += "\tlw $s4, -28($fp)\t# Restore saved register\n"
            # self.buffer["text"] += "\tlw $s5, -32($fp)\t# Restore saved register\n"
            # self.buffer["text"] += "\tlw $s6, -36($fp)\t# Restore saved register\n"
            # self.buffer["text"] += "\tlw $s7, -40($fp)\t# Restore saved register\n"
            self.buffer["text"] += "\tmove $sp, $fp\t\t# Deallocate {} bytes from the stack\n".format(memory_offset)
            self.buffer["text"] += "\tlw $fp, 0($sp)\t\t# Restore old framepointer\n"
            self.buffer["text"] += "\tjr $ra\n"
            self.STT.prev_scope()

    def visitScopeStmtNode(self, node):
        
        control = None

        for StmtNode in node.children:
            # if type(StmtNode) is BreakStmtNode or type(StmtNode) is ContinueStmtNode:
            #     control = StmtNode
            #     break
            self.visit(StmtNode)
        
        # if control is None:
        #     pass
        # else:
        #     self.visit(control)
    
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
    
    def visitExprStmtNode(self, node):
        self.visit(node.child)

    def visitWhileStmtNode(self, node):
        label_cond = "while.{}.cond".format(self.while_count)
        label_body = "while.{}.body".format(self.while_count)
        label_end = "while.{}.end".format(self.while_count)
        self.while_count += 1
        self.loop_stack.append((label_cond, label_end))
        if len(node.children) == 2:

            self.current_label = label_cond
            self.buffer["text"] += label_cond + ":\n"
            condition_node = node.children[0]
            register = self.visit(condition_node)

            # If register > 0 its true
            self.buffer["text"] += "\tsgt $t0, {}, $zero\n".format(register)

            self.buffer["text"] += "\tbeq  $t0, $zero, " + label_end + "\n"

            self.buffer["text"] += label_body + ":\n"
            self.current_label = label_body
            self.STT.child_scope()
            self.visit(node.children[1])
            self.STT.prev_scope()
            self.buffer["text"] += "\tb " + label_cond + "\n"
            if len(self.loop_stack) != 0:
                if self.loop_stack[-1] == (label_cond, label_end):
                    self.loop_stack.pop()
                else:
                    raise Exception("Weird loop behavior")
            
            self.buffer["text"] += label_end + ":\n"
            self.current_label = label_end
        else:
            self.STT.child_scope()
            self.visit(node.children[2])
            self.current_label = label_cond
            self.buffer["text"] += label_cond + ":\n"
            condition_node = node.children[0]
            register = self.visit(condition_node)

            # If register > 0 its true
            self.buffer["text"] += "\tsgt $t0, {}, $zero\n".format(register)

            self.buffer["text"] += "\tbeq  $t0, $zero, " + label_end + "\n"

            self.buffer["text"] += label_body + ":\n"
            self.current_label = label_body
            self.visit(node.children[1])
            self.STT.prev_scope()
            self.buffer["text"] += "\tb " + label_cond + "\n"
            if len(self.loop_stack) != 0:
                if self.loop_stack[-1] == (label_cond, label_end):
                    self.loop_stack.pop()
                else:
                    raise Exception("Weird loop behavior")
            
            self.buffer["text"] += label_end + ":\n"
            self.current_label = label_end

    def visitBreakStmtNode(self, node):
        self.buffer["text"] += "\tb " + self.loop_stack[-1][1] + "\n"

    def visitContinueStmtNode(self, node):
        self.buffer["text"] += "\tb " + self.loop_stack[-1][0] + "\n"


    def visitIfStmtNode(self, node):

        # Evaluate condition
        condition_node = node.children[0]
        register = self.visit(condition_node)

        # If register > 0 its true
        self.buffer["text"] += "\tsgt $t0, {}, $zero\n".format(register)


        label_true = "if.{}.then".format(self.if_count)
        label_end = "if.{}.end".format(self.if_count)
        label_false = "if.{}.else".format(self.if_count) if node.has_else else label_end
        self.if_count += 1

        self.buffer["text"] += "\tbeq  $t0, $zero, " + label_false + "\n"

        # if-block
        self.buffer["text"] += label_true + ":\n"
        # self.current_label = label_true
        # self.absolute_br.append(label_end)
        self.STT.child_scope()
        self.visit(node.children[1])
        self.STT.prev_scope()
        
        self.buffer["text"] += "\tb " + label_end + "\n"


        if node.has_else:
            self.buffer["text"] += label_false + ":\n"
            self.STT.child_scope()
            self.visit(node.children[2])
            self.STT.prev_scope()

        self.buffer["text"] += label_end + ":\n"
    
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
                    
                    register = self.visit(node.children[format_arg])
                    format_arg += 1
                    if part == 2:
                        # load format_value to $f12
                        self.buffer["text"] += "\tmtc1 {}, $f0\n".format(register) 
                        self.buffer["text"] += "\tmov.s $f12, $f0\n" 
                    else:
                        # load format_value to $a0
                        self.buffer["text"] += "\tmove $a0, {}\n".format(register)
                    self.buffer["text"] += "\tli $v0, {}\n\tsyscall\n".format(part)
                else:
                    self.buffer["text"] += "\tli $v0, 4\n\tla $a0, " + part + "\n\tsyscall\n"
        elif node.children[0].id == "scanf":
            # First edition of this codeblock, probably very inefficient.
            format_flag = False
            processed_string = []
            actual_text = []
            temp = ""
            stringsize = []
            stringsizeflag = False
            for char in node.children[1].child.rawbuffer:
                if char == '%':
                    format_flag = True
                    continue
                if format_flag:
                    if char == 'c':
                        if not temp == "":
                            actual_text.append(temp)
                        actual_text.append(12)
                        temp = ""
                    elif char == 'd':
                        if not temp == "":
                            actual_text.append(temp)
                        actual_text.append(5)
                        temp = ""
                    elif char == 'f':
                        if not temp == "":
                            actual_text.append(temp)
                        actual_text.append(6)
                        temp = ""
                    elif char == 's':
                        if not self.readbufferpresent:
                            self.buffer["str"] += "buffer: .space 1024\n"
                            self.readbufferpresent = True
                        if stringsizeflag:
                            pass
                        else:
                            stringsize.append(2)
                        if not temp == "":
                            actual_text.append(temp)
                        actual_text.append(8)
                        temp = ""
                        stringsizeflag = False
                    elif char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                        stringsize.append(int(char)+1)
                        stringsizeflag = True
                        continue
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
            
            string_format_counter = 0
            format_arg = 2
            for part in processed_string:
                self.buffer["text"] += "\tli $v0, {}\n".format(part)
                if part == 8:
                    # load format_value to $f12
                    self.buffer["text"] += "\tla $a0, buffer\n"
                    self.buffer["text"] += "\tli $a1, {}\n\tsyscall\n".format(stringsize[string_format_counter])
                    register = self.visit(node.children[format_arg])
                    for i in range(stringsize[string_format_counter]-1):
                        j = stringsize[string_format_counter]-2 - i
                        self.buffer["text"] += "\tlb $v0, {}($a0)\n".format((i), register)
                        self.buffer["text"] += "\tsb $v0, {}({})\n".format(-(j), register)
                    self.registers.reset()

                    string_format_counter += 1
                else:
                    # load format_value to $a0
                    self.buffer["text"] += "\tsyscall\n"
                    register = self.visit(node.children[format_arg])
                    self.buffer["text"] += "\tsw $v0, 0({})\n".format(register)
                    self.registers.reset()
                    
                format_arg += 1
        else:
            arg_count = 0
            for arg in node.children[1:(len(node.children))]:
                register = self.visit(arg)
                self.buffer["text"] += "\tmove $a{}, {}\n".format(arg_count, register)
            self.buffer["text"] += "\tjal {}.entry\n".format(node.children[0].id)
            return "$v0"

    def visitReturnStmtNode(self, node):
        if node.child is None:
            self.buffer["text"] += "\tj {}.exit\n".format(self.current_function)
            # raise Exception("Empty return not supported for mips?")
        else:
            register = self.visit(node.child)
            self.buffer["text"] += "\tmove $v0, {}\n".format(register)
            self.buffer["text"] += "\tj {}.exit\n".format(self.current_function)

    def visitUnaryExprNode(self, node):
        # Save register $s0
        self.buffer["text"] += "\t# Entering UnaryExprNode.\n"
        # self.buffer["text"] += "\tsubi $sp, $sp, 4\n"
        # self.buffer["text"] += "\tsw $s0, 0($sp)\n"

        if node.operation == "*":
            register = self.visit(node.child)
            self.buffer["text"] += "\tlw {}, 0({})\n".format(register, register)
            return register
        elif node.operation == "&":
            register = self.visit(node.child)
            return register
        else:
            pass

        if node.child.type == "float":
            register = self.visit(node.child)
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
                register = self.visit(node.child)
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
            elif node.operation == "++":
                if type(node.child) is DeclRefExprNode:
                    result = self.getResult(node.child)
                    register = self.loadVar(result)
                    self.buffer["text"] += "\taddi $t0, {}, 1\n".format(register)
                    self.storeVar(result, "$t0")
                    if node.prefix:
                        return "$t0"
                    else:
                        return register
                else:
                    # Unregulated address assignment clear all Register Associations
                    self.registers.reset()
                    register = "$t0"
                    lvalue = self.visit(node.child)
                    self.buffer["text"] += "\tmove $t2, {}\n".format(lvalue)
                    self.buffer["text"] += "\tlw $t1, 0({})\n".format(lvalue)
                    self.buffer["text"] += "\taddi {}, {}, 1\n".format(register, "$t1")
                    self.buffer["text"] += "\tsw {}, 0({})\n".format(register, "$t2")                    
                    if node.prefix:
                        return register
                    else:
                        return "$t1"
            elif node.operation == "--":
                if type(node.child) is DeclRefExprNode:
                    result = self.getResult(node.child)
                    register = self.loadVar(result)
                    self.buffer["text"] += "\tsubi $t0, {}, 1\n".format(register)
                    self.storeVar(result, "$t0")
                    if node.prefix:
                        return "$t0"
                    else:
                        return register
                else:
                    # Unregulated address assignment clear all Register Associations
                    self.registers.reset()
                    register = "$t0"
                    lvalue = self.visit(node.child)
                    self.buffer["text"] += "\tmove $t2, {}\n".format(lvalue)
                    self.buffer["text"] += "\tlw $t1, 0({})\n".format(lvalue)
                    self.buffer["text"] += "\tsubi {}, {}, 1\n".format(register, "$t1")
                    self.buffer["text"] += "\tsw {}, 0({})\n".format(register, "$t2")                    
                    if node.prefix:
                        return register
                    else:
                        return "$t1"
        # Restore register $s0
        # self.buffer["text"] += "\tlw $s0, 0($sp)\n"
        # self.buffer["text"] += "\taddi $sp, $sp, 4\n"
        self.buffer["text"] += "\t# Exiting UnaryExprNode.\n"
        return "$t0"

    def visitBinExprNode(self, node):

        # Save registers $s0, $s1
        self.buffer["text"] += "\t# Entering BinExprNode.\n"
        self.buffer["text"] += "\tsubi $sp, $sp, 8\n"
        self.buffer["text"] += "\tsw $s0, 4($sp)\n"
        self.buffer["text"] += "\tsw $s1, 0($sp)\n"

        if node.operation == "=":
            # Deal with lhs
            if type(node.lhs_child) is DeclRefExprNode:
                result = self.getResult(node.lhs_child)
                register = self.visit(node.rhs_child)
                self.storeVar(result, register)
            else:
                # Unregulated address assignment clear all Register Associations
                self.registers.reset()
                lvalue = self.visit(node.lhs_child)
                self.buffer["text"] += "\tmove $s0, {}\n".format(lvalue)
                register = self.visit(node.rhs_child)
                self.buffer["text"] += "\tsw {}, 0($s0)\n".format(register, lvalue)
        else:
            lhs_register = self.visit(node.lhs_child)
            self.buffer["text"] += "\tmove $s0, {}\n".format(lhs_register)
            rhs_register = self.visit(node.rhs_child)
            self.buffer["text"] += "\tmove $s1, {}\n".format(rhs_register)
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
                    elif node.operation == "==":
                        self.buffer["text"] += "\tc.eq.s $f0, $f1\n"
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
            else:
                # Need int instructions
                if node.operation in ["+", "-", "*", "/", "%"]:
                    if node.operation == "+":
                        self.buffer["text"] += "\tadd $t0, $s0, $s1\n"
                    elif node.operation == "-":
                        self.buffer["text"] += "\tsub $t0, $s0, $s1\n"
                    elif node.operation == "*":
                        self.buffer["text"] += "\tmul $t0, $s0, $s1\n"
                    elif node.operation == "/":
                        self.buffer["text"] += "\tdiv $t0, $s0, $s1\n"
                    else:
                        self.buffer["text"] += "\trem $t0, $s0, $s1\n"
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
                    elif node.operation == "==":
                        self.buffer["text"] += "\tseq $t0, $s0, $s1\n"

        # Restore registers $s0, $s1
        self.buffer["text"] += "\tlw $s0, 4($sp)\n"
        self.buffer["text"] += "\tlw $s1, 0($sp)\n"
        self.buffer["text"] += "\taddi $sp, $sp, 8\n"
        self.buffer["text"] += "\t# Exiting BinExprNode.\n"
        return "$t0"

    def visitDeclRefExprNode(self, node):
        result = self.getResult(node)
        return self.loadAddrVar(result)

    def visitArraySubscriptExprNode(self, node):
        self.buffer["text"] += "\tsubi $sp, $sp, 4\n"
        self.buffer["text"] += "\tsw $s0, 0($sp)\n"
        register = self.visit(node.index_child)
        self.buffer["text"] += "\tsll $s0, {}, 2\n".format(register)

        register = self.visit(node.array_child)

        self.buffer["text"] += "\taddu $t0, {}, $s0\n".format(register)
        # Restore register $s0
        self.buffer["text"] += "\tlw $s0, 0($sp)\n"
        self.buffer["text"] += "\taddi $sp, $sp, 4\n"
        return "$t0"



    def visitImplicitCastExprNode(self, node):
        if node.cast == "<LValueToRValue>":
            if type(node.child) is DeclRefExprNode:
                result = self.getResult(node.child)
                if result is None:
                    print("gotta fix this")
                else:
                    return self.loadVar(result) # Should return the register where loaded ex "$t0"
            register = self.visit(node.child)
            self.buffer["text"] += "\tlw $t0, 0({})\n".format(register)
            return "$t0"
        elif node.cast == "<ArrayToPointerDecay>":
            if type(node.child) is StringLiteralNode:
                return self.visit(node.child)
            
            return self.visit(node.child)
        elif node.cast == "<FloatingToIntegral>":
            register = self.visit(node.child)
            self.buffer["text"] += "\tmtc1 {}, $f2\n\tcvt.w.s $f2, $f2\n\tmfc1 $t0, $f2\n".format(register)
            return "$t0"
        elif node.cast == "<IntegralToFloating>":
            register = self.visit(node.child)
            self.buffer["text"] += "\tmtc1 {}, $f2\n\tcvt.s.w $f2, $f2\n\tmfc1 $t0, $f2\n".format(register)
            return "$t0"
                

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
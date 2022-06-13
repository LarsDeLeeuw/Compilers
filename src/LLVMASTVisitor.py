from ASTVisitor import ASTVisitor
from ASTNodes import *
import copy

class LLVMASTVisitor(ASTVisitor):

    def __init__(self):
        self.buffer = {}
        self.register = -1
        self.str_constants = {}
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

    def getRegister(self):
        self.register += 1
        return self.register

    def visitProgNode(self, node):
        self.buffer["pre"] = ''
        self.buffer["functs"] = ''
        self.buffer["str"] = ''
        for Include in node.includes:
            for LibFuncts in node.includes[Include]:
                self.buffer["pre"] += LibFuncts

        for DeclChild in node.children:
            self.visit(DeclChild)
        
        # self.buffer["main"] += "\t\tret i32 0\n}\n"
        output = open("main.ll", 'w')
        output.write(self.buffer["str"]+"\n\n"+self.buffer["pre"]+"\n\n"+self.buffer["functs"])
        output.close()
        return 0

    def visitVarDeclNode(self, node):
        ''' This needs a refactor jezus '''
        self.buffer["pre"] += "@" + node.id + " = dso_local global "
        parsed_type = node.parseType()
        if parsed_type[2] == 'int':
            if node.array:
                if node.init:
                    self.buffer["pre"] += "[" + str(node.getLen()) + " x i32] ["
                    for i, Child in enumerate(node.init_expr.children):
                        if i == 0:
                            self.buffer["pre"] += "i32 " + str(Child.value)
                        else:
                            self.buffer["pre"] += ", i32 " + str(Child.value)
                    self.buffer["pre"] += "], align 4\n"
                else:
                    self.buffer["pre"] += "[" + str(node.getLen()) + " x i32] zeroinitializer, align 4\n"
            else:
                if node.init:
                    self.buffer["pre"] += "i32 " + str(node.init_expr.value) + ", align 4\n"
                else:
                    self.buffer["pre"] += "i32 " + str(0) + ", align 4\n"
        elif parsed_type[2] == 'float':
            if node.array:
                if node.init:
                    self.buffer["pre"] += "[" + str(node.getLen()) + " x float] ["
                    for i, Child in enumerate(node.init_expr.children):
                        if i == 0:
                            self.buffer["pre"] += "float " + str(Child.value)
                        else:
                            self.buffer["pre"] += ", float " + str(Child.value)
                    self.buffer["pre"] += "], align 4\n"
                else:
                    self.buffer["pre"] += "[" + str(node.getLen()) + " x float] zeroinitializer, align 4\n"
            else:
                if node.init:
                    self.buffer["pre"] += "float " + str(node.init_expr.value) + ", align 4\n"
                else:
                    self.buffer["pre"] += "float " + str(0) + ", align 4\n"
        elif parsed_type[2] == 'char':
            if node.array:
                if node.init:
                    self.buffer["pre"] += "[" + str(node.getLen()) + " x i8] ["
                    for i, Child in enumerate(node.init_expr.children):
                        if i == 0:
                            self.buffer["pre"] += "i8 " + str(Child.value)
                        else:
                            self.buffer["pre"] += ", i8 " + str(Child.value)
                    self.buffer["pre"] += "], align 4\n"
                else:
                    self.buffer["pre"] += "[" + str(node.getLen()) + " x i8] zeroinitializer, align 4\n"
            else:
                if node.init:
                    self.buffer["pre"] += "i8 " + str(node.init_expr.value) + ", align 4\n"
                else:
                    self.buffer["pre"] += "i8 " + str(0) + ", align 4\n"
        else:
            raise Exception("Tried generating LLVM for VarDecl of unknown type")

    def visitFunctionDeclNode(self, node):
        if node.init:
            self.buffer["functs"] += "define dso_local "
            # Return_type
            if node.type == "void":
                self.buffer["functs"] += "void"
            else:
                return_type = node.parseType()
                llvm_type = None
                if return_type[2] == "char":
                    llvm_type = "i8"
                    llvm_align = "1"
                elif return_type[2] == "int":
                    llvm_type = "i32"
                elif return_type[2] == "float":
                    llvm_type = "float"
                else:
                    print("What is this?")

                if return_type[0]:
                    llvm_type += return_type[3]
                self.buffer["functs"] += llvm_type
                
            self.buffer["functs"] += " @" + node.id + "("
            for i in range(len(node.arg_types)):
                # Parm Type
                arg_type = node.children[i].parseType()
                llvm_type = None
                if arg_type[2] == "char":
                    llvm_type = "i8"
                    llvm_align = "1"
                elif arg_type[2] == "int":
                    llvm_type = "i32"
                elif arg_type[2] == "float":
                    llvm_type = "float"
                else:
                    print("What is this?")

                if arg_type[0]:
                    llvm_type += arg_type[3]
                
                if node.children[i].array:
                    # Build the array type currently no multidim support
                    pass
                    # llvm_array = "[" + str(arg.getLen()) + " x " + llvm_type + "]"
                    # llvm_type = llvm_array

                self.buffer["functs"] += llvm_type+ " noundef %" + node.children[i].id

                if i != len(node.arg_types) - 1:
                    self.buffer["functs"] += ", "
            self.buffer["functs"] += ") {\nentry:\n"
            self.current_label = "entry"

            # Move to symboltable 
            self.STT.child_scope()

            if node.type == "int":
                self.buffer["functs"] += "\t" + "%retval = alloca i32, align 4\n"


            self.visit(node.children[-1]) # ScopeStmtNode is last in children of initialised FuncDecl
            
            self.buffer["functs"] += "}\n\n"

            self.STT.prev_scope()
        else:
            pass

        self.call_count = 0
        self.conv_count = 0
        self.register_count = 0
        self.lor_count = 0
        self.land_count = 0
        self.inc_count = 0
        self.dec_count = 0
        self.if_count = 0
        self.while_count = 0
        self.idshadowing = {}
        self.idcount = {}
        self.arrayidx_count = 0
        self.loop_stack = []
        self.absolute_br = []


    def visitScopeStmtNode(self, node):
        # Declare and initialise where needed
        for symbol_id in self.STT.current_symboltablenode.hashtable.keys():
            result = self.STT.lookup(symbol_id)
            serial = result["serial"]
            if type(result["ast_node"]) is ParmVarDeclNode:
                var = result["ast_node"]

                if var.id in self.idcount.keys():
                    self.idcount[var.id] += 1
                else:
                    self.idcount[var.id] = 0
                if self.idcount[var.id] == 0:
                    self.idshadowing[serial] = var.id
                else:
                    self.idshadowing[serial] = var.id + str(self.idcount[var.id])

                var_type = var.parseType()
                llvm_type = None
                llvm_align = "4"
                if var_type[2] == "char":
                    llvm_type = "i8"
                    llvm_align = "1"
                elif var_type[2] == "int":
                    llvm_type = "i32"
                elif var_type[2] == "float":
                    llvm_type = "float"
                else:
                    print("What is this?")

                if var_type[0]:
                    if not var.array:
                        llvm_align = "8"
                    else:
                        llvm_align = "16"
                    llvm_type += var_type[3]
                
                if var.array:
                    # Build the array type currently no multidim support
                    llvm_array = "[" + str(var.getLen()) + " x " + llvm_type + "]"
                    llvm_type = llvm_array

              # Allocate
                self.buffer["functs"] += "\t" + "%" + str(self.idshadowing[serial])
                self.buffer["functs"] += ".addr = alloca "+llvm_type+", align "+llvm_align+"\n"
                # Init
                self.buffer["functs"] += "\t" + "store "+llvm_type+" %" + self.idshadowing[serial]
                self.buffer["functs"] += ", "+llvm_type+"* %" + self.idshadowing[serial] + ".addr, align "+llvm_align+"\n"
            

        returnFlag = False

        if type(node.parent) is IfStmtNode:
            store_br = self.absolute_br[-1]

        for StmtNode in node.children:
            if StmtNode.reachable:
            # DeclStmts already done above with symboltable
                if type(StmtNode) is DeclNode:
                    self.visit(StmtNode)
                else:
                    if type(StmtNode) is ReturnStmtNode:
                        returnFlag = True
                        self.visit(StmtNode)
                        self.buffer["functs"] += "\n"
                        break
                    self.visit(StmtNode)
        
        if type(node.parent) is IfStmtNode:
            if not returnFlag:
                check_br = self.absolute_br.pop()
                if check_br != store_br:
                    self.absolute_br.remove(store_br)
                    store_br = check_br
                self.buffer["functs"] += "\tbr label %" + store_br + "\n\n"

        
        if not returnFlag and type(node.parent) is FunctionDeclNode:
            # Check return type of function
            if node.parent.type == "void":
                self.buffer["functs"] += "\tret void\n"
            elif node.parent.type == "int":
                self.buffer["functs"] += "\tstore i32 0, i32* %retval, align 4\n"
                self.buffer["functs"] += "\t%"+str(self.register_count)+" = load i32, i32* %retval, align 4\n"
                self.buffer["functs"] += "\tret i32 %"+str(self.register_count)+"\n"
                self.register_count += 1
            elif node.parent.type == "float":
                self.buffer["functs"] += "\tstore float 0.0, float* %retval, align 4\n"
                self.buffer["functs"] += "\t%"+str(self.register_count)+" = load float, float* %retval, align 4\n"
                self.buffer["functs"] += "\tret float %"+str(self.register_count)+"\n"
                self.register_count += 1
            elif node.parent.type == "char":
                self.buffer["functs"] += "\tstore i8 0, i8* %retval, align 4\n"
                self.buffer["functs"] += "\t%"+str(self.register_count)+" = load i8, i8* %retval, align 4\n"
                self.buffer["functs"] += "\tret i8 %"+str(self.register_count)+"\n"
                self.register_count += 1
            else:
                raise Exception("Cannot generate default return for type: {}".format(node.parent.type))
        
    def visitReturnStmtNode(self, node):
        if node.child is None:
            self.buffer["functs"] += "\tret void\n"
        else:
            if issubclass(type(node.child), ExprNode):
                self.visit(node.child)
                self.buffer["functs"] += "\tstore i32 %"+str(self.register_count-1)+", i32* %retval, align 4\n"
                self.buffer["functs"] += "\t%"+str(self.register_count)+" = load i32, i32* %retval, align 4\n"
                self.buffer["functs"] += "\tret i32 %"+str(self.register_count)+"\n"
                self.register_count += 1
            else:
                self.buffer["functs"] += "\tstore i32 "+str(node.child.value)+", i32* %retval, align 4\n"
                self.buffer["functs"] += "\t%"+str(self.register_count)+" = load i32, i32* %retval, align 4\n"
                self.buffer["functs"] += "\tret i32 %"+str(self.register_count)+"\n"
                self.register_count += 1

    def visitBreakStmtNode(self, node):
        self.absolute_br.append(self.loop_stack[-1][1])
        # self.buffer["functs"] += "\tbr label %" + self.loop_stack[-1][1] + "\n\n"

    def visitContinueStmtNode(self, node):
        self.absolute_br.append(self.loop_stack[-1][0])
        # self.buffer["functs"] += "\tbr label %" + self.loop_stack[-1][0] + "\n\n"

    def visitWhileStmtNode(self, node):
        label_cond = "while.cond" + str(self.while_count)
        label_body = "while.body" + str(self.while_count)
        label_end = "while.end" + str(self.while_count)
        self.while_count += 1
        self.loop_stack.append((label_cond, label_end))
        if len(node.children) == 2:
            self.buffer["functs"] += "\tbr label %" + label_cond + "\n\n"
            self.current_label = label_cond
            self.buffer["functs"] += label_cond + ":\n"
            condition_node = node.children[0]
            self.visit(condition_node)

            cond_type = condition_node.type.split(" ")
            llvm_type = None
            llvm_operation = "icmp ne"
            llvm_cmpto = "0"
            if cond_type[0] == "char":
                llvm_type = "i8"
            elif cond_type[0] == "int":
                llvm_type = "i32"
            elif cond_type[0] == "float":
                llvm_type = "float"
                llvm_operation = "fcmp ne"
                llvm_cmpto = "0.000000e+00"
            else:
                print("What is this?")

            if len(cond_type) == 2:
                pass
                llvm_type += cond_type[1]
            else:
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = "+llvm_operation+" "+llvm_type+" %" + str(self.register_count-1) + ", "+llvm_cmpto+"\n"
                self.register_count += 1
            self.buffer["functs"] += "\tbr i1 %" + str(self.register_count-1) + ", label %" + label_body + ", label %" + label_end + "\n\n"

            self.buffer["functs"] += label_body + ":\n"
            self.current_label = label_body
            self.STT.child_scope()
            self.visit(node.children[1])
            self.buffer["functs"] += "\tbr label %" + label_cond + "\n\n"
            self.STT.prev_scope()
            if len(self.loop_stack) != 0:
                if self.loop_stack[-1] == (label_cond, label_end):
                    self.loop_stack.pop()
            
            self.buffer["functs"] += label_end + ":\n"
            self.current_label = label_end
        else:
            self.STT.child_scope()
            self.visit(node.children[2])
            self.buffer["functs"] += "\tbr label %" + label_cond + "\n\n"
            self.current_label = label_cond
            self.buffer["functs"] += label_cond + ":\n"
            condition_node = node.children[0]
            self.visit(condition_node)

            cond_type = condition_node.type.split(" ")
            llvm_type = None
            llvm_operation = "icmp ne"
            llvm_cmpto = "0"
            if cond_type[0] == "char":
                llvm_type = "i8"
            elif cond_type[0] == "int":
                llvm_type = "i32"
            elif cond_type[0] == "float":
                llvm_type = "float"
                llvm_operation = "fcmp ne"
                llvm_cmpto = "0.000000e+00"
            else:
                print("What is this?")

            if len(cond_type) == 2:
                pass
                llvm_type += cond_type[1]
            else:
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = "+llvm_operation+" "+llvm_type+" %" + str(self.register_count-1) + ", "+llvm_cmpto+"\n"
                self.register_count += 1
            self.buffer["functs"] += "\tbr i1 %" + str(self.register_count-1) + ", label %" + label_body + ", label %" + label_end + "\n\n"

            self.buffer["functs"] += label_body + ":\n"
            self.current_label = label_body
            self.visit(node.children[1])
            self.buffer["functs"] += "\tbr label %" + label_cond + "\n\n"
            self.STT.prev_scope()
            if len(self.loop_stack) != 0:
                if self.loop_stack[-1] == (label_cond, label_end):
                    self.loop_stack.pop()
            
            self.buffer["functs"] += label_end + ":\n"
            self.current_label = label_end


    def visitIfStmtNode(self, node):
        # load and eval cond node.children[0]
        condition_node = node.children[0]
        self.visit(condition_node)
        cond_type = condition_node.type.split(" ")
        llvm_type = None
        llvm_operation = "icmp ne"
        llvm_cmpto = "0"
        if cond_type[0] == "char":
            llvm_type = "i8"
        elif cond_type[0] == "int":
            llvm_type = "i32"
        elif cond_type[0] == "float":
            llvm_type = "float"
            llvm_operation = "fcmp ne"
            llvm_cmpto = "0.000000e+00"
        else:
            print("What is this?")

        if len(cond_type) == 2:
            pass
            llvm_type += cond_type[1]
        else:
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = "+llvm_operation+" "+llvm_type+" %" + str(self.register_count-1) + ", "+llvm_cmpto+"\n"
            self.register_count += 1
        
        label_true = "if.then" + str(self.if_count)
        label_end = "if.end" + str(self.if_count)
        label_false = str("if.else" + str(self.if_count)) if node.has_else else label_end
        self.if_count += 1

        self.buffer["functs"] += "\tbr i1 %" + str(self.register_count-1) + ", label %" + label_true + ", label %" + label_false + "\n\n"

        self.buffer["functs"] += label_true + ":\n"
        self.current_label = label_true
        self.absolute_br.append(label_end)
        self.STT.child_scope()
        self.visit(node.children[1])
        self.STT.prev_scope()
        # br_to = self.absolute_br.pop()
        # if br_to != label_end:
        #     self.absolute_br.remove(label_end)
        # self.buffer["functs"] += "\tbr label %" + br_to + "\n\n"

        if node.has_else:
            self.buffer["functs"] += label_false + ":\n"
            self.current_label = label_false
            self.absolute_br.append(label_end)
            self.STT.child_scope()
            self.visit(node.children[2])
            self.STT.prev_scope()
            # br_to = self.absolute_br.pop()
            # if br_to != label_end:
            #     self.absolute_br.remove(label_end)
            # self.buffer["functs"] += "\tbr label %" + br_to + "\n\n"

        self.buffer["functs"] += label_end + ":\n"
        self.current_label = label_end

    def visitExprStmtNode(self, node):
        if type(node.child) is BinExprNode:
            if node.child.operation == "=":
                self.visit(node.child)
            else:
                self.visit(node.child)
        else:
            self.visit(node.child)
            

    def visitCallExprNode(self, node):
        funct_node = node.children[0].ref["ast_node"]
        result = self.STT.lookup(funct_node.id)
        if result is None:
            print("gotta fix this")
        else:
            if funct_node.included:
                if funct_node.id == "printf":
                    hold = {}

                    for form_data in node.children[1:(len(node.children))]:
                        self.visit(form_data)
                        parsed_type = form_data.parseType()
                        llvm_type = ""

                        if parsed_type[2] == 'char':
                            llvm_type += "i8"
                        elif parsed_type[2] == 'int':
                            llvm_type += "i32"
                        elif parsed_type[2] == 'float':
                            llvm_type += "double"
                        else:
                            print("oopsiee what is this {}".format(form_data.type))  

                        if parsed_type[0]:
                            llvm_type += parsed_type[3]
                          

                        if parsed_type[2] == 'int':
                            hold[str(self.register_count-1)] = llvm_type
                        elif parsed_type[2] == 'float':
                            self.buffer["functs"] += "\t%" + str("conv" + str(self.conv_count)) + " = fpext float %"+str(self.register_count-1)+" to double\n"
                            self.conv_count += 1
                            hold[str("conv" + str(self.conv_count-1))] = llvm_type
                        elif parsed_type[2] == 'char':
                            hold[str(self.register_count-1)] = llvm_type
                        else:
                            print("oopsiee {}".format(form_data.type))
                    
                    # debug
                    # print(hold)

                    format_type = "i32"
                    self.buffer["functs"] += "\t%" + str(self.register_count) + " = call i32 (i8*, ...) "
                    self.buffer["functs"] += "@printf("
                    for i, form_data in enumerate(hold):
                        if i == len(hold) - 1:
                            self.buffer["functs"] += hold[form_data]+" %" + form_data + ")\n"
                        else:
                            self.buffer["functs"] += hold[form_data]+" %" + form_data + ", "
                    self.call_count += 1
                    self.register_count += 1
                elif funct_node.id == "scanf":                    
                    hold = {}

                    for form_data in node.children[1:(len(node.children))]:
                        self.visit(form_data)
                        type_split = form_data.parseType()
                        llvm_type = None
                        if type_split[2] == "int":
                            llvm_type = "i32"
                        elif type_split[2] == "float":
                            llvm_type = "float"
                        elif type_split[2] == "char":
                            llvm_type = "i8"
                        else:
                            print("what")
                        if type_split[0]:
                            if type_split[1]:
                                llvm_array_type = "[" + type_split[4][0] + " x " + llvm_type + "]"
                                llvm_type = llvm_array_type
                            llvm_type += "*"
                            hold[str(self.register_count-1)] = llvm_type
                        else:
                            print("Euhm {}".format(form_data.type))
                    
                    
                    # debug
                    # print(hold)

                    format_type = "i32"
                    self.buffer["functs"] += "\t%" + str(self.register_count) + " = call i32 (i8*, ...) "
                    self.buffer["functs"] += "@__isoc99_scanf("
                    for i, form_data in enumerate(hold):
                        if i == len(hold) - 1:
                            self.buffer["functs"] += hold[form_data]+" %" + form_data + ")\n"
                        else:
                            self.buffer["functs"] += hold[form_data]+" %" + form_data + ", "
                    self.call_count += 1
                    self.register_count += 1
            else:
                hold = {}

                for form_data in node.children[1:(len(node.children))]:
                    self.visit(form_data)
                    type_split = form_data.parseType()
                    llvm_type = None
                    if type_split[2] == "int":
                        llvm_type = "i32"
                    elif type_split[2] == "float":
                        llvm_type = "float"
                    elif type_split[2] == "char":
                        llvm_type = "i8"
                    else:
                        print("what")
                    if type_split[0]:
                        # if type_split[1]:
                        #     llvm_array_type = "[" + type_split[4][0] + " x " + llvm_type + "]"
                        #     llvm_type = llvm_array_type
                        llvm_type += type_split[3]
                    hold[str(self.register_count-1)] = llvm_type

                if funct_node.type == "void":
                    self.buffer["functs"] += "\tcall void @" + funct_node.id + "("
                    if len(hold) == 0:
                        self.buffer["functs"] += ')\n'
                    else:
                        for i, form_data in enumerate(hold):
                            if i == len(hold) - 1:
                                self.buffer["functs"] += hold[form_data]+" %" + form_data + ")\n"
                            else:
                                self.buffer["functs"] += hold[form_data]+" %" + form_data + ", "
                elif funct_node.type == "int":
                    self.buffer["functs"] += "\t%" + str(self.register_count) + " = call i32 @" + funct_node.id + "("
                    self.call_count += 1
                    self.register_count += 1
                    if len(hold) == 0:
                        self.buffer["functs"] += ')\n'
                    else:
                        for i, form_data in enumerate(hold):
                            if i == len(hold) - 1:
                                self.buffer["functs"] += hold[form_data]+" %" + form_data + ")\n"
                            else:
                                self.buffer["functs"] += hold[form_data]+" %" + form_data + ", "
                else:
                    raise Exception("LLVM FuncCAll panic")
        

    def visitBinExprNode(self, node):
        '''Generate LLVM that executes the required BinExpr,
            stores result in latest register where applicable. '''

        # First eval the lhs_child, the value we need will get stored in the register %lhs_register_count
        lhs_register_count = self.register_count + 1
        if issubclass(type(node.lhs_child), LiteralNode):
            lhs_split_type = node.lhs_child.type.split(" ")
            llvm_lhs_type = None
            if lhs_split_type[0] == "char":
                llvm_lhs_type = "i8"
            elif lhs_split_type[0] == "int":
                llvm_lhs_type = "i32"
            elif lhs_split_type[0] == "float":
                llvm_lhs_type = "float"
            else:
                print("What is this")
            if len(lhs_split_type) == 2:
                raise Exception("LLVM Panic: LiteralNode with type {}".format(node.lhs_child.type))

            self.buffer["functs"] += "\t%" + str(lhs_register_count-1) + " = alloca "+llvm_lhs_type+", align 4\n"
            self.buffer["functs"] += "\tstore "+llvm_lhs_type+" " + str(node.lhs_child.value) + ", "+llvm_lhs_type+"* %"+ str(lhs_register_count-1) +", align 4\n"
            self.register_count += 1
            self.buffer["functs"] += "\t%" + str(lhs_register_count) + " = load "+llvm_lhs_type+", "+llvm_lhs_type+"* %"+str(lhs_register_count-1)+", align 4\n"
            self.register_count += 1
        else:
            self.visit(node.lhs_child)
            lhs_register_count = self.register_count - 1
        # Secondly eval the rhs_child, the value we need will get stored in register %rhs_register_count
        rhs_register_count = self.register_count + 1
        if issubclass(type(node.rhs_child), LiteralNode):
            rhs_split_type = node.rhs_child.type.split(" ")
            llvm_rhs_type = None
            if rhs_split_type[0] == "char":
                llvm_rhs_type = "i8"
            elif rhs_split_type[0] == "int":
                llvm_rhs_type = "i32"
            elif rhs_split_type[0] == "float":
                llvm_rhs_type = "float"
            else:
                print("What is this")
            if len(rhs_split_type) == 2:
                raise Exception("LLVM Panic: LiteralNode with type {}".format(node.rhs_child.type))

            self.buffer["functs"] += "\t%" + str(rhs_register_count-1) + " = alloca "+llvm_rhs_type+", align 4\n"
            self.buffer["functs"] += "\tstore "+llvm_rhs_type+" " + str(node.rhs_child.value) + ", "+llvm_rhs_type+"* %"+ str(rhs_register_count-1) +", align 4\n"
            self.register_count += 1
            self.buffer["functs"] += "\t%" + str(rhs_register_count) + " = load "+llvm_rhs_type+", "+llvm_rhs_type+"* %"+str(rhs_register_count-1)+", align 4\n"
            self.register_count += 1
        else:
            self.visit(node.rhs_child)
            rhs_register_count = self.register_count - 1
        # Generate the LLVM for the correct node.operation using %lhs_register and %rhs_register_count
        split_type = node.type.split(" ")
        if len(split_type) == 2:
            '''Special ptr operations'''
            llvm_type += split_type[1]
            pass
        else:
            if node.operation == "||" or node.operation == "&&":
                label_true = None
                label_false = None
                label_prev = self.current_label
                if node.operation == "||":
                    label_true = "lor.end" + str(self.lor_count)
                    label_false = "lor.rhs" + str(self.lor_count)
                    self.lor_count += 1
                else:
                    label_true = "land.rhs" + str(self.land_count)
                    label_false = "land.end" + str(self.land_count)
                    self.land_count += 1
                
                lhs_split_type = node.lhs_child.type.split(" ")
                llvm_lhs_cmpto = None
                llvm_lhs_type = None
                flhs_op = False
                if lhs_split_type[0] == "char":
                    llvm_lhs_type = "i8"
                elif lhs_split_type[0] == "int":
                    llvm_lhs_type = "i32"
                elif lhs_split_type[0] == "float":
                    llvm_lhs_type = "float"
                    flhs_op = True
                else:
                    print("What is this")
                if len(lhs_split_type) == 2:
                    '''Need to cmpr to nullptr'''
                    pass
                else:
                    llvm_lhs_operation = None
                    if flhs_op:
                        llvm_lhs_operation = "fcmp une"
                        llvm_lhs_cmpto = "0.000000e+00"
                    else:
                        llvm_lhs_operation = "icmp ne"
                        llvm_lhs_cmpto = "0"
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = "+llvm_lhs_operation+" "+llvm_lhs_type+" %" + str(lhs_register_count) + ", "+llvm_lhs_cmpto+"\n"
                self.register_count += 1
                self.buffer["functs"] += "\tbr i1 %" + str(self.register_count-1) + ", label %" + label_true + ", label %" + label_false + "\n\n"

                if node.operation == "||":
                    self.buffer["functs"] += label_false + ":\n"
                    self.current_label = label_false
                else:
                    self.buffer["functs"] += label_true + ":\n"
                    self.current_label = label_true

                rhs_split_type = node.rhs_child.type.split(" ")
                llvm_rhs_cmpto = None
                llvm_rhs_type = None
                frhs_op = False
                if rhs_split_type[0] == "char":
                    llvm_rhs_type = "i8"
                elif rhs_split_type[0] == "int":
                    llvm_rhs_type = "i32"
                elif rhs_split_type[0] == "float":
                    llvm_rhs_type = "float"
                    frhs_op = True
                else:
                    print("What is this")
                if len(rhs_split_type) == 2:
                    '''Need to cmpr to nullptr'''
                    pass
                else:
                    llvm_rhs_operation = None
                    if frhs_op:
                        llvm_rhs_operation = "fcmp une"
                        llvm_rhs_cmpto = "0.000000e+00"
                    else:
                        llvm_rhs_operation = "icmp ne"
                        llvm_rhs_cmpto = "0"
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = "+llvm_rhs_operation+" "+llvm_rhs_type+" %" + str(rhs_register_count) + ", "+llvm_rhs_cmpto+"\n"
                self.register_count += 1
                if node.operation == "||":
                    self.buffer["functs"] += "\tbr label %" + label_true + "\n\n"
                    self.buffer["functs"] += label_true + ":\n"
                    self.current_label = label_true
                else:
                    self.buffer["functs"] += "\tbr label %" + label_false + "\n\n"
                    self.buffer["functs"] += label_false + ":\n"
                    self.current_label = label_false
                if node.operation == "||":
                    self.buffer["functs"] += "\t%" + str(self.register_count) + " = phi i1 [ true, %" + label_prev + " ], [ %" + str(self.register_count-1) + ", %" + label_false + " ]\n"
                    self.register_count += 1
                else:
                    self.buffer["functs"] += "\t%" + str(self.register_count) + " = phi i1 [ false, %" + label_prev + " ], [ %" + str(self.register_count-1) + ", %" + label_true + " ]\n"
                    self.register_count += 1
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = zext i1 %" + str(self.register_count-1) + " to i32\n"
                self.register_count += 1
            elif node.operation == "=":
                lhs_split_type = node.lhs_child.type.split(" ")
                lhs_split_type = node.lhs_child.parseType()
                llvm_lhs_type = None
                llvm_lhs_align = "4"
                if lhs_split_type[2] == "char":
                    llvm_lhs_type = "i8"
                elif lhs_split_type[2] == "int":
                    llvm_lhs_type = "i32"
                elif lhs_split_type[2] == "float":
                    llvm_lhs_type = "float"
                else:
                    print("What is this")
                if lhs_split_type[0]:
                    llvm_lhs_type += lhs_split_type[3]
                    llvm_lhs_align = "8"
                self.visit(node.lhs_child)
                self.buffer["functs"] += "\t" + "store "+llvm_lhs_type+" " + "%"+str(rhs_register_count)
                self.buffer["functs"] += ", "+llvm_lhs_type+"* %" + str(self.register_count-1) + ", align "+llvm_lhs_align+"\n"
            else:
                llvm_operation = None
                llvm_extend = False
                flhs_op = False
                lhs_split_type = node.lhs_child.type.split(" ")
                llvm_lhs_type = None
                if lhs_split_type[0] == "char":
                    llvm_lhs_type = "i8"
                elif lhs_split_type[0] == "int":
                    llvm_lhs_type = "i32"
                elif lhs_split_type[0] == "float":
                    llvm_lhs_type = "float"
                    flhs_op = True
                else:
                    print("What is this")
                if len(lhs_split_type) == 2:
                    '''Need to cmpr to nullptr'''
                    pass
                if node.operation == "+":
                    if flhs_op:
                        llvm_operation = "fadd"
                    else:
                        llvm_operation = "add nsw"
                elif node.operation == "-":
                    if flhs_op:
                        llvm_operation = "fsub"
                    else:
                        llvm_operation = "sub nsw"
                elif node.operation == "*":
                    if flhs_op:
                        llvm_operation = "fmul"
                    else:
                        llvm_operation = "mul nsw"
                elif node.operation == "/":
                    if flhs_op:
                        llvm_operation = "fdiv"
                    else:
                        llvm_operation = "sdiv"
                elif node.operation == "%":
                    if flhs_op:
                        raise Exception("Modulo operator only supports int")
                    else:
                        llvm_operation = "srem"
                elif node.operation == ">":
                    llvm_extend = True
                    if flhs_op:
                        llvm_operation = "fcmp ogt"
                    else:
                        llvm_operation = "icmp sgt"
                elif node.operation == "<":
                    llvm_extend = True
                    if flhs_op:
                        llvm_operation = "fcmp olt"
                    else:
                        llvm_operation = "icmp slt"
                elif node.operation == ">=":
                    llvm_extend = True
                    if flhs_op:
                        llvm_operation = "fcmp oge"
                    else:
                        llvm_operation = "icmp sge"
                elif node.operation == "<=":
                    llvm_extend = True
                    if flhs_op:
                        llvm_operation = "fcmp ole"
                    else:
                        llvm_operation = "icmp sle"
                elif node.operation == "!=":
                    llvm_extend = True
                    if flhs_op:
                        llvm_operation = "fcmp une"
                    else:
                        llvm_operation = "icmp ne"
                elif node.operation == "==":
                    llvm_extend = True
                    if flhs_op:
                        llvm_operation = "fcmp oeq"
                    else:
                        llvm_operation = "icmp eq"
                else:
                    raise Exception("Binary Operator {} is not supported.".format(node.operation))
                
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = "+llvm_operation+" "+llvm_lhs_type+" %"+str(lhs_register_count)+", %"+str(rhs_register_count)+"\n"
                self.register_count += 1

                if llvm_extend:
                    self.buffer["functs"] += "\t%" + str(self.register_count) + " = zext i1 %" + str(self.register_count-1) + " to i32\n"
                    self.register_count += 1
            

    def visitUnaryExprNode(self, node):
        
        child_register_count = self.register_count + 1

        if issubclass(type(node.child), LiteralNode):
            if node.child.type == 'int':
                self.buffer["functs"] += "\t%" + str(child_register_count-1) + " = alloca i32, align 4\n"
                self.buffer["functs"] += "\tstore i32 " + str(node.child.value) + ", i32* %"+ str(child_register_count-1) +", align 4\n"
                self.register_count += 1
                self.buffer["functs"] += "\t%" + str(child_register_count) + " = load i32, i32* %"+str(child_register_count-1)+", align 4\n"
                self.register_count += 1
            elif node.child.type == 'float':
                self.buffer["functs"] += "\t%" + str(child_register_count-1) + " = alloca float, align 4\n"
                self.buffer["functs"] += "\tstore float " + str(node.child.value) + ", float* %"+ str(child_register_count-1) +", align 4\n"
                self.register_count += 1
                self.buffer["functs"] += "\t%" + str(child_register_count) + " = load float, float* %"+str(child_register_count-1)+", align 4\n"
                self.register_count += 1
            else:
                raise Exception("LLVM panic")
        else:
            self.visit(node.child)
            child_register_count = self.register_count - 1
        
        
        if node.operation == "!":
            child_type = node.child.type.split(" ")
            llvm_type = None
            llvm_operation = "icmp ne"
            llvm_cmpto = "0"
            if child_type[0] == "char":
                llvm_type = "i8"
            elif child_type[0] == "int":
                llvm_type = "i32"
            elif child_type[0] == "float":
                llvm_type = "float"
                llvm_operation = "fcmp ne"
                llvm_cmpto = "0.000000e+00"
            else:
                print("What is this?")

            if len(child_type) == 2:
                pass
                llvm_type += child_type[1]
            else:
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = "+llvm_operation+" "+llvm_type+" %" + str(child_register_count) + ", "+llvm_cmpto+"\n"
            self.register_count += 1

            self.buffer["functs"] += "\t%" + str(self.register_count) + " = xor i1 %" +str(self.register_count-1)+", true\n"
            self.register_count += 1
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = zext i1 %" + str(self.register_count-1) + " to i32\n"
            self.register_count += 1
        elif node.operation == "-":
            '''Stores numeric inverse in latest register'''
            child_type = node.child.type.split(" ")
            llvm_type = None
            if child_type[0] == "char":
                llvm_type = "i8"
            elif child_type[0] == "int":
                llvm_type = "i32"
            elif child_type[0] == "float":
                llvm_type = "float"
            else:
                print("what is this")
            llvm_align = "4"
            if len(child_type) == 2:
                llvm_type += child_type[1]
                llvm_align = "8"
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = sub nsw "+llvm_type+" 0,  %" +str(child_register_count)+"\n"
            self.register_count += 1
        elif node.operation == "&":
            type_split = node.parseType()
            llvm_type = None
            if type_split[2] == "int":
                llvm_type = "i32"
            elif type_split[2] == "float":
                llvm_type = "float"
            elif type_split[2] == "char":
                llvm_type = "i8"
            else:
                print("what")

            if type_split[0]:
                llvm_type += type_split[3]
        elif node.operation == "*":
            type_split = node.child.parseType()
            llvm_type = None
            if type_split[2] == "int":
                llvm_type = "i32"
            elif type_split[2] == "float":
                llvm_type = "float"
            elif type_split[2] == "char":
                llvm_type = "i8"
            else:
                print("what")
            if type_split[0]:
                llvm_type += len(type_split[3])*"*"
                        
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = load "+llvm_type+", "+llvm_type+"* %" +str(child_register_count)+", align 4\n"
            self.register_count += 1
        elif node.operation == "++":
            '''Stores rvalue before operation in latest register, excute operation, if prefix load updated value to latest register'''
            child_type = node.child.type.split(" ")
            llvm_type = None
            if child_type[0] == "char":
                llvm_type = "i8"
            elif child_type[0] == "int":
                llvm_type = "i32"
            elif child_type[0] == "float":
                llvm_type = "float"
            else:
                print("what is this")
            llvm_align = "4"
            if len(child_type) == 2:
                llvm_type += child_type[1]
                llvm_align = "8"
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = load "+llvm_type+", "+llvm_type+"* %"+str(self.register_count-1)+", align "+llvm_align+"\n"
            self.register_count += 1
            self.buffer["functs"] += "\t%" + "inc"+str(self.inc_count) + " = add nsw "+llvm_type+" %" +str(self.register_count-1)+", 1\n"
            self.inc_count += 1
            self.buffer["functs"] += "\tstore "+llvm_type+" %" + "inc"+str(self.inc_count-1) + ", "+llvm_type+"* %"+ str(child_register_count) + ", align "+llvm_align+"\n"
            if node.prefix:
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = load "+llvm_type+", "+llvm_type+"* %"+str(child_register_count)+", align "+llvm_align+"\n"
                self.register_count += 1
        elif node.operation == "--":
            '''Stores rvalue before operation in latest register, excute operation, if prefix load updated value to latest register'''
            child_type = node.child.parseType()
            llvm_type = None
            if child_type[2] == "char":
                llvm_type = "i8"
            elif child_type[2] == "int":
                llvm_type = "i32"
            elif child_type[2] == "float":
                llvm_type = "float"
            else:
                print("what is this: {}".format(child_type[2]))
            llvm_align = "4"
            if len(child_type) == 2:
                llvm_type += child_type[1]
                llvm_align = "8"
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = load "+llvm_type+", "+llvm_type+"* %"+str(self.register_count-1)+", align "+llvm_align+"\n"
            self.register_count += 1
            self.buffer["functs"] += "\t%" + "dec"+str(self.dec_count) + " = add nsw "+llvm_type+" %" +str(self.register_count-1)+", -1\n"
            self.dec_count += 1
            self.buffer["functs"] += "\tstore "+llvm_type+" %" + "dec"+str(self.dec_count-1) + ", "+llvm_type+"* %"+ str(child_register_count) + ", align "+llvm_align+"\n"
            if node.prefix:
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = load "+llvm_type+", "+llvm_type+"* %"+str(child_register_count)+", align "+llvm_align+"\n"
                self.register_count += 1
        else:
            raise Exception("LLVM Panic: {}".format(node.operation))

    def visitDeclStmtNode(self, node):
        result = self.STT.lookup(node.child.id)
        serial = result["serial"]
        var = result["ast_node"]

        if var.id in self.idcount.keys():
            self.idcount[var.id] += 1
        else:
            self.idcount[var.id] = 0
        if self.idcount[var.id] == 0:
            self.idshadowing[serial] = var.id
        else:
            self.idshadowing[serial] = var.id + str(self.idcount[var.id])

        var_type = var.type.split(" ")
        var_type = var.parseType()
        llvm_type = None
        llvm_align = "4"
        if var_type[2] == "char":
            llvm_type = "i8"
            llvm_align = "1"
        elif var_type[2] == "int":
            llvm_type = "i32"
        elif var_type[2] == "float":
            llvm_type = "float"
        else:
            print("What is this?")

        if var_type[0]:
            if not var.array:
                llvm_align = "8"
            else:
                llvm_align = "16"
            llvm_type += var_type[3]
        
        if var.array:
            # Build the array type currently no multidim support
            llvm_array = "[" + str(var.getLen()) + " x " + llvm_type + "]"
            llvm_type = llvm_array

        self.buffer["functs"] += "\t" + "%" + str(self.idshadowing[serial])
        self.buffer["functs"] += " = alloca "+llvm_type+", align "+llvm_align+"\n"
        
        if var.init:
            if var.array:
                raise Exception("LLVM NOT IMPLEMENTED YET")
            
            if issubclass(type(var.init_expr), LiteralNode):
                self.buffer["functs"] += "\t" + "store "+ llvm_type +" " + str(var.init_expr.value)
                self.buffer["functs"] += ", "+ llvm_type +"* %" + str(self.idshadowing[serial]) + ", align "+ llvm_align +"\n"
            else:
                self.visit(var.init_expr)
                self.buffer["functs"] += "\t" + "store "+ llvm_type +" %" + str(self.register_count-1)
                self.buffer["functs"] += ", "+ llvm_type +"* %" + str(self.idshadowing[serial]) + ", align "+ llvm_align +"\n"
    
    def visitImplicitCastExprNode(self, node):
        if node.cast == "<LValueToRValue>":
            # Store the LValue in latest register
            self.visit(node.child)
            # Convert to RValue
            child_type = node.child.type.split(" ")
            child_type = node.child.parseType()
            llvm_type = None
            if child_type[2] == "char":
                llvm_type = "i8"
            elif child_type[2] == "int":
                llvm_type = "i32"
            elif child_type[2] == "float":
                llvm_type = "float"
            else:
                print("what is this")
            llvm_align = "4"
            if child_type[0]:
                llvm_type += child_type[3]
                llvm_align = "8"
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = load "+llvm_type+", "+llvm_type+"* %"+str(self.register_count-1)+", align "+llvm_align+"\n"
            self.register_count += 1
        elif node.cast == "<ArrayToPointerDecay>":
            '''Currently not build for multidim yet'''
            if type(node.child) is StringLiteralNode:
                self.visit(node.child)
                return

            llvm_array_type = None

            child_type = node.child.ref["ast_node"].parseType()
            llvm_type = None
            if child_type[2] == "char":
                llvm_type = "i8"
            elif child_type[2] == "int":
                llvm_type = "i32"
            elif child_type[2] == "float":
                llvm_type = "float"
            else:
                print("what is this")

            # Build the LLVM array type
            llvm_array_type = "[" + str(node.child.ref["ast_node"].getLen()) + " x " + llvm_type + "]"

            serial = node.child.ref["serial"]
            llvm_pre = "%"
            
            if node.child.ref["global"]:
                llvm_pre = "@"
                llvm_id = node.child.ref["ast_node"].id
            else:
                llvm_id = str(self.idshadowing[serial])

            # .
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = getelementptr inbounds "+llvm_array_type+", "+llvm_array_type+"* "+llvm_pre+llvm_id+", i64 0, i64 0\n"
            self.register_count += 1
        elif node.cast == "<FloatingToIntegral>":
            self.visit(node.child)
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = fptosi float %" + str(self.register_count-1) + " to i32\n"
            self.register_count += 1
        elif node.cast == "<IntegralToFloating>":
            self.visit(node.child)
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = sitofp i32 %" + str(self.register_count-1) + " to float\n"
            self.register_count += 1
            

    def visitArraySubscriptExprNode(self, node):
        '''Writes LLVM that stores referenced lvalue in latest register'''
        self.visit(node.index_child)
        self.buffer["functs"] += "\t%" + str(self.register_count) + " = sext i32 %" + str(self.register_count-1) + " to i64\n"
        self.register_count += 1
        index_register = self.register_count-1
        self.visit(node.array_child)
        child_type = node.array_child.parseType()
        llvm_type = None
        if child_type[2] == "char":
            llvm_type = "i8"
        elif child_type[2] == "int":
            llvm_type = "i32"
        elif child_type[2] == "float":
            llvm_type = "float"
        else:
            print("what is this")

        self.buffer["functs"] += "\t%" + str(self.register_count) + " = getelementptr inbounds "+llvm_type+", "+llvm_type+"* "+"%"+str(self.register_count-1)+", i64 "+"%" + str(index_register) + "\n"
        self.register_count += 1


    def visitDeclRefExprNode(self, node):
        result = self.STT.lookup(node.ref["ast_node"].id)
        if result is None:
            print("gotta fix this")
        else:
            serial = node.ref["serial"]
            child_type = node.ref["ast_node"].parseType()
            llvm_type = None
            if child_type[2] == "char":
                llvm_type = "i8"
            elif child_type[2] == "int":
                llvm_type = "i32"
            elif child_type[2] == "float":
                llvm_type = "float"
            else:
                print("what is this")

            if child_type[0]:
                llvm_type += child_type[3]

            if node.ref["ast_node"].array:
                llvm_array_type = "[" + str(node.ref["ast_node"].getLen()) + " x " + llvm_type + "]"
                llvm_type = llvm_array_type

            llvm_pre = "%"

            if node.ref["global"]:
                llvm_pre = "@"
                llvm_id = node.ref["ast_node"].id
            else:
                if node.ref["object"] == "lvalue ParmVar":
                    llvm_id = str(self.idshadowing[serial] + ".addr")
                else:
                    llvm_id = str(self.idshadowing[serial])
            
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = getelementptr inbounds "+llvm_type+", "+llvm_type+"* "+llvm_pre+llvm_id+", i64 0\n"
            self.register_count += 1


    def visitInitListExprNode(self, node):
        pass

    def visitIntegerLiteralNode(self, node):
        self.buffer["functs"] += "\t%" + str(self.register_count) + " = alloca i32, align 4\n"
        self.buffer["functs"] += "\tstore i32 " + str(node.value) + ", i32* %"+ str(self.register_count) +", align 4\n"
        self.register_count += 1
        self.buffer["functs"] += "\t%" + str(self.register_count) + " = load i32, i32* %"+str(self.register_count-1)+", align 4\n"
        self.register_count += 1

    def visitFloatingLiteralNode(self, node):
        self.buffer["functs"] += "\t%" + str(self.register_count) + " = alloca float, align 4\n"
        self.buffer["functs"] += "\tstore float " + str(node.value) + ", float* %"+ str(self.register_count) +", align 4\n"
        self.register_count += 1
        self.buffer["functs"] += "\t%" + str(self.register_count) + " = load float, float* %"+str(self.register_count-1)+", align 4\n"
        self.register_count += 1

    def visitCharacterLiteralNode(self, node):
        self.buffer["functs"] += "\t%" + str(self.register_count) + " = alloca i8, align 4\n"
        self.buffer["functs"] += "\tstore i8 " + str(node.value) + ", i8* %"+ str(self.register_count) +", align 4\n"
        self.register_count += 1
        self.buffer["functs"] += "\t%" + str(self.register_count) + " = load i8, i8* %"+str(self.register_count-1)+", align 4\n"
        self.register_count += 1

    def visitStringLiteralNode(self, node):
        if node.value in self.str_constants:
            pass
        else:
            self.str_constants[node.value] = "@.str." + str(len(self.str_constants))
            self.buffer["str"] += self.str_constants[node.value] + " = private unnamed_addr constant ["
            self.buffer["str"] += str(len(node.buffer)+1) + ' x i8] c"' + node.value + "\\00" +'", align 1\n'

        self.buffer["functs"] += "\t%" + str(self.register_count) + " = getelementptr inbounds ["+ str(len(node.buffer)+1) +" x i8], ["+ str(len(node.buffer)+1)
        self.buffer["functs"] += " x i8]* "+ self.str_constants[node.value] +", i32 0, i32 0\n"
        self.register_count += 1
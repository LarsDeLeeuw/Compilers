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
        self.buffer["pre"] += "@" + node.id + " = dso_local global "
        if node.type == 'int':
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
        elif node.type == 'float':
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
        elif node.type == 'char':
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
            if node.return_type == "void":
                self.buffer["functs"] += "void"
            elif node.return_type == 'int':
                if node.init:
                    self.buffer["functs"] += "i32"
                else:
                    self.buffer["functs"] += "i32"
            self.buffer["functs"] += " @" + node.id + "("
            for i, arg in enumerate(node.arg_types):
                # Parm Type
                if arg == 'int':
                    self.buffer["functs"] += "i32 noundef %" + node.children[i].id
                elif arg == 'float':
                    self.buffer["functs"] += "float noundef %" + node.children[i].id

                if i != len(node.arg_types) - 1:
                    self.buffer["functs"] += ", "
            self.buffer["functs"] += ") {\nentry:\n"
            self.current_label = "entry"

            # Move to symboltable 
            self.STT.child_scope()

            if node.id == "main":
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
                arg = result["ast_node"]
                if arg.id in self.idcount.keys():
                    self.idcount[arg.id] += 1
                else:
                    self.idcount[arg.id] = 0
                if self.idcount[arg.id] == 0:
                    self.idshadowing[serial] = arg.id
                else:
                    self.idshadowing[serial] = arg.id + str(self.idcount[arg.id])
              # Allocate
                if arg.type == 'int':
                    self.buffer["functs"] += "\t" + "%" + self.idshadowing[serial]
                    self.buffer["functs"] += ".addr = alloca i32, align 4\n"
                elif arg.type == 'float':
                    self.buffer["functs"] += "\t" + "%" + self.idshadowing[serial]
                    self.buffer["functs"] += ".addr = alloca float, align 4\n"
                else:
                    raise Exception("LLVM Panic")
                # Init
                if arg.type == 'int':
                    self.buffer["functs"] += "\t" + "store i32 %" + self.idshadowing[serial]
                    self.buffer["functs"] += ", i32* %" + self.idshadowing[serial] + ".addr, align 4\n"
                elif arg.type == 'float':
                    self.buffer["functs"] += "\t" + "store float %" + self.idshadowing[serial]
                    self.buffer["functs"] += ", float* %" + self.idshadowing[serial] + ".addr, align 4\n"
                else:
                    raise Exception("LLVM Panic")
            else:
                var = result["ast_node"]
                if var.array:
                    if var.id in self.idcount.keys():
                        self.idcount[var.id] += 1
                    else:
                        self.idcount[var.id] = 0
                    self.idshadowing[serial] = var.id + str(self.idcount[var.id])
                    # Allocate
                    if var.type == 'int':
                        self.buffer["functs"] += "\t" + "%" + str(self.idshadowing[serial])
                        self.buffer["functs"] += " = alloca ["+str(var.len)+" x i32], align 4\n"
                    elif var.type == 'float':
                        self.buffer["functs"] += "\t" + "%" + str(self.idshadowing[serial])
                        self.buffer["functs"] += " = alloca ["+str(var.len)+" x float], align 4\n"
                    elif var.type == 'char':
                        self.buffer["functs"] += "\t" + "%" + str(self.idshadowing[serial])
                        self.buffer["functs"] += " = alloca ["+str(var.len)+" x i8], align 4\n"
                    else:
                        raise Exception("LLVM Panic")
                    if var.init:
                        raise Exception("LLVM NOT IMPLEMENTED YET")
                        if not var.init_expr is None and issubclass(type(var.init_expr), LiteralNode):
                            # Init
                            self.memory[serial] = var.init_expr.value
                            if var.type == 'int':
                                self.buffer["functs"] += "\t" + "store i32 " + str(var.init_expr.value)
                                self.buffer["functs"] += ", i32* %" + str(self.idshadowing[serial]) + ", align 4\n"
                            elif var.type == 'float':
                                self.buffer["functs"] += "\t" + "store float " + str(var.init_expr.value)
                                self.buffer["functs"] += ", float* %" + str(self.idshadowing[serial]) + ", align 4\n"
                            elif var.type == 'char':
                                self.buffer["functs"] += "\t" + "store i8 " + str(var.init_expr.value)
                                self.buffer["functs"] += ", i8* %" + str(self.idshadowing[serial]) + ", align 4\n"
                else:
                    if var.id in self.idcount.keys():
                        self.idcount[var.id] += 1
                    else:
                        self.idcount[var.id] = 0
                    self.idshadowing[serial] = var.id + str(self.idcount[var.id])
                    # Allocate
                    if var.type == 'int':
                        self.buffer["functs"] += "\t" + "%" + str(self.idshadowing[serial])
                        self.buffer["functs"] += " = alloca i32, align 4\n"
                    elif var.type == 'float':
                        self.buffer["functs"] += "\t" + "%" + str(self.idshadowing[serial])
                        self.buffer["functs"] += " = alloca float, align 4\n"
                    elif var.type == 'char':
                        self.buffer["functs"] += "\t" + "%" + str(self.idshadowing[serial])
                        self.buffer["functs"] += " = alloca i8, align 4\n"
                    if var.init:
                        if not var.init_expr is None:
                            if issubclass(type(var.init_expr), LiteralNode):
                                # Init
                                if var.type == 'int':
                                    self.buffer["functs"] += "\t" + "store i32 " + str(var.init_expr.value)
                                    self.buffer["functs"] += ", i32* %" + str(self.idshadowing[serial]) + ", align 4\n"
                                elif var.type == 'float':
                                    self.buffer["functs"] += "\t" + "store float " + str(var.init_expr.value)
                                    self.buffer["functs"] += ", float* %" + str(self.idshadowing[serial]) + ", align 4\n"
                                elif var.type == 'char':
                                    self.buffer["functs"] += "\t" + "store i8 " + str(var.init_expr.value)
                                    self.buffer["functs"] += ", i8* %" + str(self.idshadowing[serial]) + ", align 4\n"
                            elif type(var.init_expr) is ImplicitCastExprNode:
                                # Currently assuming lhs and rhs will be same type
                                if var.init_expr.cast == "<LValueToRValue>":
                                    self.visit(var.init_expr)
                                    # Init
                                    if var.type == 'int':
                                        self.buffer["functs"] += "\t" + "store i32 %" + str(self.register_count-1)
                                        self.buffer["functs"] += ", i32* %" + str(self.idshadowing[serial]) + ", align 4\n"
                                    elif var.type == 'float':
                                        self.buffer["functs"] += "\t" + "store float %" + str(self.register_count-1)
                                        self.buffer["functs"] += ", float* %" + str(self.idshadowing[serial]) + ", align 4\n"
                                    elif var.type == 'char':
                                        self.buffer["functs"] += "\t" + "store i8 %" + str(self.register_count-1)
                                        self.buffer["functs"] += ", i8* %" + str(self.idshadowing[serial]) + ", align 4\n"
                                else:
                                    print("Still needs work")
                            elif type(var.init_expr) is UnaryExprNode:
                                if var.init_expr.operation == "&":
                                    pass
                                else:
                                    raise Exception("VarDecl init with Unary not fully implemented yet")
                            elif type(var.init_expr) is CallExprNode:
                                raise Exception("VarDecl init with CallExpr not implemented yet")
                            else:
                                raise Exception("LLVM Panic {}".format(var.init_expr))
        returnFlag = False

        for StmtNode in node.children:
            # DeclStmts already done above with symboltable
            if type(StmtNode) is DeclNode:
                pass
            else:
                if type(StmtNode) is ReturnStmtNode:
                    returnFlag = True
                self.visit(StmtNode)
        
        if not returnFlag and type(node.parent) is FunctionDeclNode:
            # Check return type of function
            if node.parent.return_type == "void":
                self.buffer["functs"] += "\tret void\n"
            elif node.parent.return_type == "int":
                self.buffer["functs"] += "\tstore i32 0, i32* %retval, align 4\n"
                self.buffer["functs"] += "\t%"+str(self.register_count)+" = load i32, i32* %retval, align 4\n"
                self.buffer["functs"] += "\tret i32 %"+str(self.register_count)+"\n"
                self.register_count += 1
            elif node.parent.return_type == "float":
                self.buffer["functs"] += "\tstore float 0.0, float* %retval, align 4\n"
                self.buffer["functs"] += "\t%"+str(self.register_count)+" = load float, float* %retval, align 4\n"
                self.buffer["functs"] += "\tret float %"+str(self.register_count)+"\n"
                self.register_count += 1
            elif node.parent.return_type == "char":
                self.buffer["functs"] += "\tstore i8 0, i8* %retval, align 4\n"
                self.buffer["functs"] += "\t%"+str(self.register_count)+" = load i8, i8* %retval, align 4\n"
                self.buffer["functs"] += "\tret i8 %"+str(self.register_count)+"\n"
                self.register_count += 1
            else:
                raise Exception("Cannot generate default return for type: {}".format(node.parent.return_type))
        
    def visitReturnStmtNode(self, node):
        if node.child is None:
            self.buffer["functs"] += "\tret void\n"
        else:
            if issubclass(type(node.child), ExprNode):
                self.buffer["functs"] += "\tstore i32 "+str(node.child.value)+", i32* %retval, align 4\n"
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

        self.buffer["functs"] += "\tbr label %" + label_cond + "\n\n"
        self.current_label = label_cond
        self.buffer["functs"] += label_cond + ":\n"
        condition_node = node.children[0]
        self.visit(condition_node)

        if condition_node.type == 'bool':
            pass
        else:
            print("somying whilestmt type")
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


    def visitIfStmtNode(self, node):
        # load and eval cond node.children[0]
        condition_node = node.children[0]
        self.visit(condition_node)
        if condition_node.type == 'bool':
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
            br_to = self.absolute_br.pop()
            if br_to != label_end:
                self.absolute_br.remove(label_end)
            self.buffer["functs"] += "\tbr label %" + br_to + "\n\n"

            if node.has_else:
                self.buffer["functs"] += label_false + ":\n"
                self.current_label = label_false
                self.absolute_br.append(label_end)
                self.STT.child_scope()
                self.visit(node.children[2])
                self.STT.prev_scope()
                br_to = self.absolute_br.pop()
                if br_to != label_end:
                    self.absolute_br.remove(label_end)
                self.buffer["functs"] += "\tbr label %" + br_to + "\n\n"

            self.buffer["functs"] += label_end + ":\n"
            self.current_label = label_end
        else:
            if condition_node.type == 'int':
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp ne i32 %" + str(self.register_count-1) + ", 0\n"
                self.register_count += 1
            else:
                print("Something not implemented yet in ifstmtnode " + condition_node.type)
                return
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
            br_to = self.absolute_br.pop()
            if br_to != label_end:
                self.absolute_br.remove(label_end)
            self.buffer["functs"] += "\tbr label %" + br_to + "\n\n"

            if node.has_else:
                self.buffer["functs"] += label_false + ":\n"
                self.current_label = label_false
                self.absolute_branch.append(label_end)
                self.STT.child_scope()
                self.visit(node.children[2])
                self.STT.prev_scope()
                self.buffer["functs"] += "\tbr label %" + self.absolute_br + "\n\n"
                br_to = self.absolute_br.pop()
                if br_to != label_end:
                    self.absolute_br.remove(label_end)
                self.buffer["functs"] += "\tbr label %" + br_to + "\n\n"
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
                    # Amount of i8 string contains
                    byte_len = str(len(node.children[1].value)+node.children[1].offset+1)

                    if node.children[1].value in self.str_constants:
                        pass
                    else:
                        self.str_constants[node.children[1].value] = "@.str." + str(len(self.str_constants))
                        self.buffer["str"] += self.str_constants[node.children[1].value] + " = private unnamed_addr constant ["
                        self.buffer["str"] += byte_len + ' x i8] c"' + node.children[1].value + "\\00" +'", align 1\n'
                    
                    hold = {}

                    for form_data in node.children[2:(len(node.children))]:
                        self.visit(form_data)
                        if form_data.type == 'bool':
                            self.buffer["functs"] += "\t%" + str(self.register_count) + " = zext i1 %" + str(self.register_count-1) + " to i32\n"
                            self.register_count += 1
                            hold[str(self.register_count-1)] = "i32"
                        elif form_data.type == 'int':
                            hold[str(self.register_count-1)] = "i32"
                        elif form_data.type == 'float':
                            self.buffer["functs"] += "\t%" + str("conv" + str(self.conv_count)) + " = fpext float %"+str(self.register_count-1)+" to double\n"
                            self.conv_count += 1
                            hold[str("conv" + str(self.conv_count-1))] = "double"
                        elif form_data.type == 'char':
                            hold[str(self.register_count-1)] = "i8"
                        else:
                            print("oopsiee")
                    
                    # debug
                    # print(hold)

                    format_type = "i32"
                    self.buffer["functs"] += "\t%call" + str(self.call_count) + " = call i32 (i8*, ...) "
                    self.buffer["functs"] += "@printf(i8* getelementptr inbounds (["+ byte_len +" x i8], ["+ byte_len
                    self.buffer["functs"] += " x i8]* "+ self.str_constants[node.children[1].value] +", i32 0, i32 0)"
                    if len(hold) == 0:
                        self.buffer["functs"] += ')\n'
                    else:
                        self.buffer["functs"] += ', '
                        for i, form_data in enumerate(hold):
                            if i == len(hold) - 1:
                                self.buffer["functs"] += hold[form_data]+" %" + form_data + ")\n"
                            else:
                                self.buffer["functs"] += hold[form_data]+" %" + form_data + ", "
                    self.call_count += 1
            else:
                hold = {}

                for form_data in node.children[1:(len(node.children))]:
                    self.visit(form_data)
                    if form_data.type == 'bool':
                        self.buffer["functs"] += "\t%" + str(self.register_count) + " = zext i1 %" + str(self.register_count-1) + " to i32\n"
                        self.register_count += 1
                        hold[str(self.register_count-1)] = "i32"
                    elif form_data.type == 'int':
                        hold[str(self.register_count-1)] = "i32"
                    elif form_data.type == 'float':
                        self.buffer["functs"] += "\t%" + str("conv" + str(self.conv_count)) + " = fpext float %"+str(self.register_count-1)+" to double\n"
                        self.conv_count += 1
                        hold[str("conv" + str(self.conv_count-1))] = "double"
                    elif form_data.type == 'char':
                        hold[str(self.register_count-1)] = "i8"

                if funct_node.return_type == "void":
                    self.buffer["functs"] += "\tcall void @" + funct_node.id + "("
                    if len(hold) == 0:
                        self.buffer["functs"] += ')\n'
                    else:
                        for i, form_data in enumerate(hold):
                            if i == len(hold) - 1:
                                self.buffer["functs"] += hold[form_data]+" %" + form_data + ")\n"
                            else:
                                self.buffer["functs"] += hold[form_data]+" %" + form_data + ", "
                elif funct_node.return_type == "int":
                    self.buffer["functs"] += "\t%call" + str(self.call_count) + " = call i32 @" + funct_node.id + "("
                    self.call_count += 1
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
        
        lhs_register_count = self.register_count + 1 

        if issubclass(type(node.lhs_child), LiteralNode):
            if node.lhs_child.type == 'int':
                self.buffer["functs"] += "\t%" + str(lhs_register_count-1) + " = alloca i32, align 4\n"
                self.buffer["functs"] += "\tstore i32 " + str(node.lhs_child.value) + ", i32* %"+ str(lhs_register_count-1) +", align 4\n"
                self.register_count += 1
                self.buffer["functs"] += "\t%" + str(lhs_register_count) + " = load i32, i32* %"+str(lhs_register_count-1)+", align 4\n"
                self.register_count += 1
            elif node.lhs_child.type == 'float':
                self.buffer["functs"] += "\t%" + str(lhs_register_count-1) + " = alloca float, align 4\n"
                self.buffer["functs"] += "\tstore float " + str(node.lhs_child.value) + ", float* %"+ str(lhs_register_count-1) +", align 4\n"
                self.register_count += 1
                self.buffer["functs"] += "\t%" + str(lhs_register_count) + " = load float, float* %"+str(lhs_register_count-1)+", align 4\n"
                self.register_count += 1
            else:
                raise Exception("LLVM panic")
        else:
            if type(node.lhs_child) is BinExprNode:
                self.visitBinExprNode(node.lhs_child)
                lhs_register_count = self.register_count - 1
            elif type(node.lhs_child) is UnaryExprNode:
                self.visitUnaryExprNode(node.lhs_child)
                lhs_register_count = self.register_count - 1
            elif type(node.lhs_child) is ImplicitCastExprNode:
                if node.operation == "=":
                    pass
                else:
                    self.visit(node.lhs_child)
                    lhs_register_count = self.register_count - 1
            elif (type(node.lhs_child) is DeclRefExprNode or type(node.lhs_child) is ArraySubscriptExprNode) and node.operation == "=":
                self.visit(node.lhs_child)
                lhs_register_count = self.register_count - 1
            else:
                raise Exception("Bad BinExpr")
        
        rhs_register_count = self.register_count + 1

        if issubclass(type(node.rhs_child), LiteralNode):
            if node.rhs_child.type == 'int':
                self.buffer["functs"] += "\t%" + str(rhs_register_count-1) + " = alloca i32, align 4\n"
                self.buffer["functs"] += "\tstore i32 " + str(node.rhs_child.value) + ", i32* %"+ str(rhs_register_count-1) +", align 4\n"
                self.register_count += 1
                self.buffer["functs"] += "\t%" + str(rhs_register_count) + " = load i32, i32* %"+str(rhs_register_count-1)+", align 4\n"
                self.register_count += 1
            elif node.rhs_child.type == 'float':
                self.buffer["functs"] += "\t%" + str(rhs_register_count-1) + " = alloca float, align 4\n"
                self.buffer["functs"] += "\tstore float " + str(node.rhs_child.value) + ", float* %"+ str(rhs_register_count-1) +", align 4\n"
                self.register_count += 1
                self.buffer["functs"] += "\t%" + str(rhs_register_count) + " = load float, float* %"+str(self.register_count-1)+", align 4\n"
                self.register_count += 1
            elif node.rhs_child.type == 'char':
                self.buffer["functs"] += "\t%" + str(rhs_register_count-1) + " = alloca i8, align 4\n"
                self.buffer["functs"] += "\tstore i8 " + str(node.rhs_child.value) + ", i8* %"+ str(rhs_register_count-1) +", align 4\n"
                self.register_count += 1
                self.buffer["functs"] += "\t%" + str(rhs_register_count) + " = load i8, i8* %"+str(self.register_count-1)+", align 4\n"
                self.register_count += 1
            else:
                raise Exception("LLVM panic")
        else:
            if type(node.rhs_child) is BinExprNode:
                self.visitBinExprNode(node.rhs_child)
                rhs_register_count = self.register_count - 1
            elif type(node.rhs_child) is UnaryExprNode:
                self.visitUnaryExprNode(node.rhs_child)
                rhs_register_count = self.register_count - 1
            elif type(node.rhs_child) is ImplicitCastExprNode:
                self.visit(node.rhs_child)
                rhs_register_count = self.register_count - 1
            else:
                raise Exception("Bad BinExpr")

        if node.operation == "+":
            if node.type == "int":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = add nsw i32 %"+str(lhs_register_count)+", %"+str(rhs_register_count)+"\n"
                self.register_count += 1
            elif node.type == 'float':
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = fadd float %"+str(lhs_register_count)+", %"+str(rhs_register_count)+"\n"
                self.register_count += 1
        elif node.operation == "-":
            if node.type == "int":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = sub nsw i32 %"+str(lhs_register_count)+", %"+str(rhs_register_count)+"\n"
                self.register_count += 1
            elif node.type == 'float':
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = fsub float %"+str(lhs_register_count)+", %"+str(rhs_register_count)+"\n"
                self.register_count += 1
        elif node.operation == "*":
            if node.type == "int":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = mul nsw i32 %"+str(lhs_register_count)+", %"+str(rhs_register_count)+"\n"
                self.register_count += 1
            elif node.type == 'float':
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = fmul float %"+str(lhs_register_count)+", %"+str(rhs_register_count)+"\n"
                self.register_count += 1
        elif node.operation == "/":
            if node.type == "int":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = sdiv i32 %"+str(lhs_register_count)+", %"+str(rhs_register_count)+"\n"
                self.register_count += 1
            elif node.type == 'float':
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = fdiv float %"+str(lhs_register_count)+", %"+str(rhs_register_count)+"\n"
                self.register_count += 1
        elif node.operation == ">":
            fcomp = False
            if node.lhs_child.type == "int" and node.rhs_child.type == "int":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp ne i32 %" + str(lhs_register_count) + ", 0\n"
                self.register_count += 1
            elif node.lhs_child.type == "int" and node.rhs_child.type == "float":
                # Implicit cast: sitofp
                fcomp = True
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = sitofp i32 %" + str(lhs_register_count) + " to float\n"
                self.register_count += 1
                lhs_register_count = self.register_count - 1
            elif node.lhs_child.type == "float":
                fcomp = True
            else:
                raise Exception("Bad BinExpr > ", node.lhs_child.type)

            if node.rhs_child.type == "int" and node.lhs_child.type == "int":
                pass
            elif node.rhs_child.type == "int" and node.rhs_child.type == "float":
                # Implicit cast: sitofp
                fcomp = True
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = sitofp i32 %" + str(rhs_register_count) + " to float\n"
                self.register_count += 1
                rhs_register_count = self.register_count - 1
            elif node.rhs_child.type == "float":
                fcomp = True
            else:
                raise Exception("Bad BinExpr >", node.rhs_child.type)

            if fcomp:
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = fcmp ogt float %" + str(lhs_register_count) + ", %" + str(rhs_register_count) +"\n"
                self.register_count += 1
            else:
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp sgt i32 %" + str(lhs_register_count) + ", %" + str(rhs_register_count) +"\n"
                self.register_count += 1
            
            # self.buffer["functs"] += "\t%" + str(self.register_count) + " = zext i1 %" + str(self.register_count-1) + " to i32\n"
            # self.register_count += 1
        elif node.operation == "<":
            fcomp = False
            if node.lhs_child.type == "int" and node.rhs_child.type == "int":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp ne i32 %" + str(lhs_register_count) + ", 0\n"
                self.register_count += 1
            elif node.lhs_child.type == "int" and node.rhs_child.type == "float":
                # Implicit cast: sitofp
                fcomp = True
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = sitofp i32 %" + str(lhs_register_count) + " to float\n"
                self.register_count += 1
                lhs_register_count = self.register_count - 1
            elif node.lhs_child.type == "float":
                fcomp = True
            else:
                raise Exception("Bad BinExpr < ", node.lhs_child.type)

            if node.rhs_child.type == "int" and node.lhs_child.type == "int":
                pass
            elif node.rhs_child.type == "int" and node.rhs_child.type == "float":
                # Implicit cast: sitofp
                fcomp = True
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = sitofp i32 %" + str(rhs_register_count) + " to float\n"
                self.register_count += 1
                rhs_register_count = self.register_count - 1
            elif node.rhs_child.type == "float":
                fcomp = True
            else:
                raise Exception("Bad BinExpr <", node.rhs_child.type)

            if fcomp:
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = fcmp olt float %" + str(lhs_register_count) + ", %" + str(rhs_register_count) +"\n"
                self.register_count += 1
            else:
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp slt i32 %" + str(lhs_register_count) + ", %" + str(rhs_register_count) +"\n"
                self.register_count += 1
            
            # self.buffer["functs"] += "\t%" + str(self.register_count) + " = zext i1 %" + str(self.register_count-1) + " to i32\n"
            # self.register_count += 1
        elif node.operation == "<=":
            fcomp = False
            if node.lhs_child.type == "int" and node.rhs_child.type == "int":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp ne i32 %" + str(lhs_register_count) + ", 0\n"
                self.register_count += 1
            elif node.lhs_child.type == "int" and node.rhs_child.type == "float":
                # Implicit cast: sitofp
                fcomp = True
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = sitofp i32 %" + str(lhs_register_count) + " to float\n"
                self.register_count += 1
                lhs_register_count = self.register_count - 1
            elif node.lhs_child.type == "float":
                fcomp = True
            else:
                raise Exception("Bad BinExpr <= ", node.lhs_child.type)

            if node.rhs_child.type == "int" and node.lhs_child.type == "int":
                pass
            elif node.rhs_child.type == "int" and node.rhs_child.type == "float":
                # Implicit cast: sitofp
                fcomp = True
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = sitofp i32 %" + str(rhs_register_count) + " to float\n"
                self.register_count += 1
                rhs_register_count = self.register_count - 1
            elif node.rhs_child.type == "float":
                fcomp = True
            else:
                raise Exception("Bad BinExpr <=", node.rhs_child.type)

            if fcomp:
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = fcmp ole float %" + str(lhs_register_count) + ", %" + str(rhs_register_count) +"\n"
                self.register_count += 1
            else:
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp sle i32 %" + str(lhs_register_count) + ", %" + str(rhs_register_count) +"\n"
                self.register_count += 1
            
            # self.buffer["functs"] += "\t%" + str(self.register_count) + " = zext i1 %" + str(self.register_count-1) + " to i32\n"
            # self.register_count += 1
        elif node.operation == ">=":
            fcomp = False
            if node.lhs_child.type == "int" and node.rhs_child.type == "int":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp ne i32 %" + str(lhs_register_count) + ", 0\n"
                self.register_count += 1
            elif node.lhs_child.type == "int" and node.rhs_child.type == "float":
                # Implicit cast: sitofp
                fcomp = True
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = sitofp i32 %" + str(lhs_register_count) + " to float\n"
                self.register_count += 1
                lhs_register_count = self.register_count - 1
            elif node.lhs_child.type == "float":
                fcomp = True
            else:
                raise Exception("Bad BinExpr >= ", node.lhs_child.type)

            if node.rhs_child.type == "int" and node.lhs_child.type == "int":
                pass
            elif node.rhs_child.type == "int" and node.rhs_child.type == "float":
                # Implicit cast: sitofp
                fcomp = True
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = sitofp i32 %" + str(rhs_register_count) + " to float\n"
                self.register_count += 1
                rhs_register_count = self.register_count - 1
            elif node.rhs_child.type == "float":
                fcomp = True
            else:
                raise Exception("Bad BinExpr >=", node.rhs_child.type)

            if fcomp:
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = fcmp oge float %" + str(lhs_register_count) + ", %" + str(rhs_register_count) +"\n"
                self.register_count += 1
            else:
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp sge i32 %" + str(lhs_register_count) + ", %" + str(rhs_register_count) +"\n"
                self.register_count += 1
            
            # self.buffer["functs"] += "\t%" + str(self.register_count) + " = zext i1 %" + str(self.register_count-1) + " to i32\n"
            # self.register_count += 1
        elif node.operation == "!=":
            # Define fcomp here for readability, should always be set to True or False before use thanks to closure of if/else.
            fcomp = None
            # Extend lhs to i32 where needed
            if node.lhs_child.type == "bool":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = zext i1 %" + str(lhs_register_count) + " to i32\n"
                self.register_count += 1
                lhs_register_count = self.register_count - 1
            elif node.lhs_child.type == "char":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = sext i8 %" + str(lhs_register_count) + " to i32\n"
                self.register_count += 1
                lhs_register_count = self.register_count - 1
            # Extend rhs to i32 where needed
            if node.rhs_child.type == "bool":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = zext i1 %" + str(rhs_register_count) + " to i32\n"
                self.register_count += 1
                rhs_register_count = self.register_count - 1
            elif node.rhs_child.type == "char":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = sext i8 %" + str(rhs_register_count) + " to i32\n"
                self.register_count += 1
                rhs_register_count = self.register_count - 1
            # When lhs and rhs of equal type we only need to determine fcomp thanks to previous extends
            if node.lhs_child.type == node.rhs_child.type:
                if node.lhs_child.type == "float":
                    fcomp = True
                else:
                    fcomp = False
            else:
                if node.lhs_child.type == "float":
                    # lhs.type != rhs.type, rhs must be i32 due to earlier extends
                    fcomp = True
                    self.buffer["functs"] += "\t%" + str(self.register_count) + " = sitofp i32 %" + str(rhs_register_count) + " to float\n"
                    self.register_count += 1
                    rhs_register_count = self.register_count - 1
                elif node.rhs_child.type == "float":
                    # lhs.type != rhs.type, lhs must be i32 due to earlier extends
                    fcomp = True
                    self.buffer["functs"] += "\t%" + str(self.register_count) + " = sitofp i32 %" + str(lhs_register_count) + " to float\n"
                    self.register_count += 1
                    lhs_register_count = self.register_count - 1
                else:
                    # no promotion needed since neither is float
                    fcomp = False
            # Write correct LLVM compare based on fcomp  
            if fcomp:
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = fcmp une float %" + str(lhs_register_count) + ", %" + str(rhs_register_count) +"\n"
                self.register_count += 1
            else:
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp ne i32 %" + str(lhs_register_count) + ", %" + str(rhs_register_count) +"\n"
                self.register_count += 1
        elif node.operation == "==":
            fcomp = False
            if node.lhs_child.type == "int" and node.rhs_child.type == "int":
                pass
                # self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp eq i32 %" + str(lhs_register_count) + ", 0\n"
                # self.register_count += 1
            elif node.lhs_child.type == "int" and node.rhs_child.type == "float":
                # Implicit cast: sitofp
                fcomp = True
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = sitofp i32 %" + str(lhs_register_count) + " to float\n"
                self.register_count += 1
                lhs_register_count = self.register_count - 1
            elif node.lhs_child.type == "float":
                fcomp = True
            else:
                raise Exception("Bad BinExpr != ", node.lhs_child.type)

            if node.rhs_child.type == "int" and node.lhs_child.type == "int":
                pass
            elif node.rhs_child.type == "int" and node.rhs_child.type == "float":
                # Implicit cast: sitofp
                fcomp = True
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = sitofp i32 %" + str(rhs_register_count) + " to float\n"
                self.register_count += 1
                rhs_register_count = self.register_count - 1
            elif node.rhs_child.type == "float":
                fcomp = True
            else:
                raise Exception("Bad BinExpr !=", node.rhs_child.type)

            if fcomp:
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = fcmp oeq float %" + str(lhs_register_count) + ", %" + str(rhs_register_count) +"\n"
                self.register_count += 1
            else:
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp eq i32 %" + str(lhs_register_count) + ", %" + str(rhs_register_count) +"\n"
                self.register_count += 1
            
            # self.buffer["functs"] += "\t%" + str(self.register_count) + " = zext i1 %" + str(self.register_count-1) + " to i32\n"
            # self.register_count += 1
        elif node.operation == "||":
            label_true = "lor.end" + str(self.lor_count)
            label_false = "lor.rhs" + str(self.lor_count)
            label_prev = self.current_label
            self.lor_count += 1
            if node.lhs_child.type == "bool":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp ne i8 %" + str(lhs_register_count) + ", 0\n"
                self.register_count += 1
            elif node.lhs_child.type == "int":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp ne i32 %" + str(lhs_register_count) + ", 0\n"
                self.register_count += 1
            elif node.lhs_child.type == "float":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = fcmp une float %" + str(lhs_register_count) + ", 0.000000e+00\n"
                self.register_count += 1
            else:
                raise Exception("Unsupported lhs_child.type for LLVM BinExpr ||")
            self.buffer["functs"] += "\tbr i1 %" + str(self.register_count-1) + ", label %" + label_true + ", label %" + label_false + "\n\n"

            self.buffer["functs"] += label_false + ":\n"
            self.current_label = label_false
            if node.rhs_child.type == "bool":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp ne i1 %" + str(rhs_register_count) + ", 0\n"
                self.register_count += 1
            elif node.rhs_child.type == "int":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp ne i32 %" + str(rhs_register_count) + ", 0\n"
                self.register_count += 1
            elif node.rhs_child.type == "float":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = fcmp une float %" + str(rhs_register_count) + ", 0.000000e+00\n"
                self.register_count += 1
            else:
                raise Exception("Unsupported rhs_child.type for LLVM BinExpr ||")
            self.buffer["functs"] += "\tbr label %" + label_true + "\n\n"

            self.buffer["functs"] += label_true + ":\n"
            self.current_label = label_true
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = phi i1 [ true, %" + label_prev + " ], [ %" + str(self.register_count-1) + ", %" + label_false + " ]\n"
            self.register_count += 1
            # self.buffer["functs"] += "\t%" + str(self.register_count) + " = zext i1 %" + str(self.register_count-1) + " to i32\n"
            # self.register_count += 1
            
        elif node.operation == "&&":
            label_true = "land.rhs" + str(self.land_count)
            label_false = "land.end" + str(self.land_count)
            label_prev = self.current_label
            self.land_count += 1
            if node.lhs_child.type == "bool":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp ne i1 %" + str(lhs_register_count) + ", 0\n"
                self.register_count += 1
            elif node.lhs_child.type == "int":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp ne i32 %" + str(lhs_register_count) + ", 0\n"
                self.register_count += 1
            elif node.lhs_child.type == "float":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = fcmp une float %" + str(lhs_register_count) + ", 0.000000e+00\n"
                self.register_count += 1
            else:
                raise Exception("Unsupported lhs_child.type for LLVM BinExpr &&")
            self.buffer["functs"] += "\tbr i1 %" + str(self.register_count-1) + ", label %" + label_true + ", label %" + label_false + "\n\n"

            self.buffer["functs"] += label_true + ":\n"
            self.current_label = label_true
            if node.rhs_child.type == "bool":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp ne i1 %" + str(rhs_register_count) + ", 0\n"
                self.register_count += 1
            elif node.rhs_child.type == "int":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp ne i32 %" + str(rhs_register_count) + ", 0\n"
                self.register_count += 1
            elif node.rhs_child.type == "float":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = fcmp une float %" + str(rhs_register_count) + ", 0.000000e+00\n"
                self.register_count += 1
            else:
                raise Exception("Unsupported rhs_child.type for LLVM BinExpr &&")
            self.buffer["functs"] += "\tbr label %" + label_false + "\n\n"

            self.buffer["functs"] += label_false + ":\n"
            self.current_label = label_false
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = phi i1 [ false, %" + label_prev + " ], [ %" + str(self.register_count-1) + ", %" + label_true + " ]\n"
            self.register_count += 1
            # self.buffer["functs"] += "\t%" + str(self.register_count) + " = zext i1 %" + str(self.register_count-1) + " to i32\n"
            # self.register_count += 1
        elif node.operation == "=":
            self.visit(node.lhs_child)
            if node.lhs_child.type == 'int':
                self.buffer["functs"] += "\t" + "store i32 " + "%"+str(rhs_register_count)
                self.buffer["functs"] += ", i32* %" + str(self.register_count-1) + ", align 4\n"
            elif node.lhs_child.type == 'float':
                self.buffer["functs"] += "\t" + "store float " + "%"+str(rhs_register_count)
                self.buffer["functs"] += ", float* %" + str(self.register_count-1) + ", align 4\n"
            elif node.lhs_child.type == 'char':
                self.buffer["functs"] += "\t" + "store i8 " + "%"+str(rhs_register_count)
                self.buffer["functs"] += ", i8* %" + str(self.register_count-1) + ", align 4\n"
            else:
                raise Exception("LLVM Panic")
        else:
            print("I dont know this bin op yet kind regards ~compiler")

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
            if type(node.child) is BinExprNode:
                self.visitBinExprNode(node.child)
                child_register_count = self.register_count - 1
            elif type(node.child) is UnaryExprNode:
                self.visitUnaryExprNode(node.child)
                child_register_count = self.register_count - 1
            elif type(node.child) is DeclRefExprNode:
                self.visitDeclRefExprNode(node.child)
                child_register_count = self.register_count - 1
            elif type(node.child) is ImplicitCastExprNode:
                self.visit(node.child)
                child_register_count = self.register_count - 1
            else:
                raise Exception("Bad UnaryExpr")
        
        if node.operation == "!":
            # self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp ne i32 %" + str(child_register_count) + ", 0\n"
            # self.register_count += 1
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = xor i1 %" +str(child_register_count)+", true\n"
            self.register_count += 1
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = zext i1 %" + str(self.register_count-1) + " to i32\n"
            self.register_count += 1
        elif node.operation == "&":
            type_split = node.type.split(" ")
            if type_split[0] == "int":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = load i32"+type_split[1]+" %" +str(child_register_count)+", align 8\n"
                self.register_count += 1
            else:
                print("Not implemented yet")
        elif node.operation == "++" and not node.prefix:
            '''Stores rvalue before operation in latest register, excute operation'''
            if not (type(node.child) is DeclRefExprNode):
                print("I can only perform this on IdRef")
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
        else:
            raise Exception("LLVM Panic")

    def visitDeclStmtNode(self, node):
        pass
    
    def visitImplicitCastExprNode(self, node):
        if node.cast == "<LValueToRValue>":
            # Store the LValue in latest register
            self.visit(node.child)
            # Convert to RValue
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
        elif node.cast == "<ArrayToPointerDecay>":
            '''Currently not build for multidim yet'''
            llvm_array_type = None

            child_type = node.child.ref["ast_node"].type.split(" ")
            llvm_type = None
            if child_type[0] == "char":
                llvm_type = "i8"
            elif child_type[0] == "int":
                llvm_type = "i32"
            elif child_type[0] == "float":
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

            # Write partial LLVM instruction, parent ArraySubscriptExpr should finish it with index.
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = getelementptr inbounds "+llvm_array_type+", "+llvm_array_type+"* "+llvm_pre+llvm_id+", i64 0, i64 "
            

    def visitArraySubscriptExprNode(self, node):
        '''Writes LLVM that stores referenced lvalue in latest register'''
        self.visit(node.index_child)
        self.buffer["functs"] += "\t%" + str(self.register_count) + " = sext i32 %" + str(self.register_count-1) + " to i64\n"
        self.register_count += 1
        self.visit(node.array_child)
        self.buffer["functs"] += "%" + str(self.register_count-1) + "\n"
        self.register_count += 1


    def visitDeclRefExprNode(self, node):
        result = self.STT.lookup(node.ref["ast_node"].id)
        if result is None:
            print("gotta fix this")
        else:
            serial = node.ref["serial"]
            child_type = node.ref["ast_node"].type.split(" ")
            llvm_type = None
            if child_type[0] == "char":
                llvm_type = "i8"
            elif child_type[0] == "int":
                llvm_type = "i32"
            elif child_type[0] == "float":
                llvm_type = "float"
            else:
                print("what is this")

            if len(child_type) == 2:
                llvm_type += child_type[1]
            
            llvm_pre = "%"

            if node.ref["global"]:
                llvm_pre = "@"
                llvm_id = node.ref["ast_node"].id
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

    
from ASTVisitor import ASTVisitor
from ASTNodes import *

class LLVMASTVisitor(ASTVisitor):

    def __init__(self):
        self.buffer = {}
        self.register = -1
        self.str_constants = {}
        self.call_count = 0
        self.register_count = 0
        self.lor_count = 0
        self.land_count = 0
        self.current_label = None
        self.currentST = None

    def checkST(self, id, st_node):
        if id in st_node.symbols:
            return (False, 0)
        index = st_node.index
        st_node.index += 1
        return (True, index)

    def findST(self, id, st_node):
        lookST = st_node

        while not (lookST is None):
            if id in lookST.symbols:
                return (True, lookST.symbols[id])
            lookST = lookST.parent
        
        return (False, None)

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
            if node.return_type is None:
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

            if node.id == "main":
                self.buffer["functs"] += "\t" + "%retval = alloca i32, align 4\n"

            self.visit(node.children[-1]) # ScopeStmtNode is last in children of initialised FuncDecl
            
            self.buffer["functs"] += "}\n\n"

    def visitScopeStmtNode(self, node):
        # Declare and initialise where needed
        for Symbol in node.symboltable.symbols:
            if type(node.symboltable.symbols[Symbol][1]) is ParmVarDeclNode:
                arg = node.symboltable.symbols[Symbol][1]
                # Allocate
                if arg.type == 'int':
                    self.buffer["functs"] += "\t" + "%" + arg.id
                    self.buffer["functs"] += ".addr = alloca i32, align 4\n"
                elif arg.type == 'float':
                    self.buffer["functs"] += "\t" + "%" + arg.id
                    self.buffer["functs"] += ".addr = alloca float, align 4\n"
                # Init
                if arg.type == 'int':
                    self.buffer["functs"] += "\t" + "store i32 %" + arg.id
                    self.buffer["functs"] += ", i32* %" + arg.id + ".addr, align 4\n"
                elif arg.type == 'float':
                    self.buffer["functs"] += "\t" + "store float %" + arg.id
                    self.buffer["functs"] += ", float* %" + arg.id + ".addr, align 4\n"
            else:
                var = node.symboltable.symbols[Symbol][1]
                # Allocate
                if var.type == 'int':
                    self.buffer["functs"] += "\t" + "%" + str(self.register_count)
                    self.buffer["functs"] += " = alloca i32, align 4\n"
                elif var.type == 'float':
                    self.buffer["functs"] += "\t" + "%" + str(self.register_count)
                    self.buffer["functs"] += " = alloca float, align 4\n"
                elif var.type == 'char':
                    self.buffer["functs"] += "\t" + "%" + str(self.register_count)
                    self.buffer["functs"] += " = alloca i8, align 4\n"
                self.register_count += 1
                if var.init:
                    if not var.init_expr is None and issubclass(type(var.init_expr), LiteralNode):
                        # Init
                        if var.type == 'int':
                            self.buffer["functs"] += "\t" + "store i32 " + str(var.init_expr.value)
                            self.buffer["functs"] += ", i32* %" + str(self.register_count-1) + ", align 4\n"
                        elif var.type == 'float':
                            self.buffer["functs"] += "\t" + "store float " + str(var.init_expr.value)
                            self.buffer["functs"] += ", float* %" + str(self.register_count-1) + ", align 4\n"
                        elif var.type == 'char':
                            self.buffer["functs"] += "\t" + "store i8 " + str(var.init_expr.value)
                            self.buffer["functs"] += ", i8* %" + str(self.register_count-1) + ", align 4\n"

        self.call_count = 0

        returnFlag = False

        for StmtNode in node.children:
            # DeclStmts already done above with symboltable
            if type(StmtNode) is DeclNode:
                pass
            else:
                if type(StmtNode) is ReturnStmtNode:
                    returnFlag = True
                self.visit(StmtNode)
        
        if not returnFlag:
            self.buffer["functs"] += "\tstore i32 "+str(0)+", i32* %retval, align 4\n"
            self.buffer["functs"] += "\t%"+str(self.register_count)+" = load i32, i32* %retval, align 4\n"
            self.buffer["functs"] += "\tret i32 %"+str(self.register_count)+"\n"
            self.register_count += 1
        
        self.call_count = 0

    def visitReturnStmtNode(self, node):
        self.buffer["functs"] += "\tstore i32 "+str(node.child.value)+", i32* %retval, align 4\n"
        self.buffer["functs"] += "\t%"+str(self.register_count)+" = load i32, i32* %retval, align 4\n"
        self.buffer["functs"] += "\tret i32 %"+str(self.register_count)+"\n"
        self.register_count += 1


    def visitExprStmtNode(self, node):
        if type(node.child) is BinExprNode:
            if node.child.operation == "=":
                pass
            else:
                self.visit(node.child)
        else:
            self.visit(node.child)
            

    def visitCallExprNode(self, node):
        funct_node = node.children[0]
        (idIsOk, Ref) = self.findST(funct_node.id, funct_node.symboltable)
        if idIsOk:
            if Ref[1].included:
                if funct_node.id == "printf":
                    if node.children[1].value in self.str_constants:
                        pass
                    else:
                        self.str_constants[node.children[1].value] = "@.str." + str(len(self.str_constants))
                        self.buffer["str"] += self.str_constants[node.children[1].value] + " = private unnamed_addr constant ["
                        self.buffer["str"] += str(len(node.children[1].value)+2) + ' x i8] c"' + node.children[1].value + "\\0A\\00" +'", align 1\n'
                    
                    hold = {}

                    for form_data in node.children[2:(len(node.children))]:
                        self.visit(form_data)
                        if form_data.type == 'int':
                            hold[str(self.register_count-1)] = "i32"
                        elif form_data.type == 'float':
                            self.buffer["functs"] += "\t%" + str(self.register_count) + " = fpext float %"+str(self.register_count-1)+" to double\n"
                            self.register_count += 1
                            hold[str(self.register_count-1)] = "double"
                        elif form_data.type == 'char':
                            hold[str(self.register_count-1)] = "i8"

                    print(hold)
                    format_type = "i32"
                    self.buffer["functs"] += "\t%call" + str(self.call_count) + " = call i32 (i8*, ...) "
                    self.buffer["functs"] += "@printf(i8* getelementptr inbounds (["+ str(len(node.children[1].value)+2) +" x i8], ["+str(len(node.children[1].value)+2)
                    self.buffer["functs"] += " x i8]* "+ self.str_constants[node.children[1].value] +", i32 0, i32 0), "
                    for i, form_data in enumerate(hold):
                        if i == len(hold) - 1:
                            self.buffer["functs"] += hold[form_data]+" %" + form_data + ")\n"
                        else:
                            self.buffer["functs"] += hold[form_data]+" %" + form_data + ", "
                    self.call_count += 1


        else:
            raise Exception("Cannot generate LLVM for call at line: {}, ID not found in symboltables", node.line)

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
            elif type(node.lhs_child) is DeclRefExprNode:
                self.visitDeclRefExprNode(node.lhs_child)
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
            else:
                raise Exception("LLVM panic")
        else:
            if type(node.rhs_child) is BinExprNode:
                self.visitBinExprNode(node.rhs_child)
                rhs_register_count = self.register_count - 1
            elif type(node.rhs_child) is UnaryExprNode:
                self.visitUnaryExprNode(node.rhs_child)
                rhs_register_count = self.register_count - 1
            elif type(node.rhs_child) is DeclRefExprNode:
                self.visitDeclRefExprNode(node.rhs_child)
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
            
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = zext i1 %" + str(self.register_count-1) + " to i32\n"
            self.register_count += 1
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
            
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = zext i1 %" + str(self.register_count-1) + " to i32\n"
            self.register_count += 1
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
            
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = zext i1 %" + str(self.register_count-1) + " to i32\n"
            self.register_count += 1
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
            
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = zext i1 %" + str(self.register_count-1) + " to i32\n"
            self.register_count += 1
        elif node.operation == "!=":
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
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = fcmp une float %" + str(lhs_register_count) + ", %" + str(rhs_register_count) +"\n"
                self.register_count += 1
            else:
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp ne i32 %" + str(lhs_register_count) + ", %" + str(rhs_register_count) +"\n"
                self.register_count += 1
            
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = zext i1 %" + str(self.register_count-1) + " to i32\n"
            self.register_count += 1
        elif node.operation == "||":
            label_true = "lor.end" + str(self.lor_count)
            label_false = "lor.rhs" + str(self.lor_count)
            label_prev = self.current_label
            self.lor_count += 1
            if node.lhs_child.type == "int":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp ne i32 %" + str(lhs_register_count) + ", 0\n"
                self.register_count += 1
            elif node.lhs_child.type == "float":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = fcmp une float %" + str(lhs_register_count) + ", 0.000000e+00\n"
                self.register_count += 1
            self.buffer["functs"] += "\tbr i1 %" + str(self.register_count-1) + ", label %" + label_true + ", label %" + label_false + "\n\n"

            self.buffer["functs"] += label_false + ":\n"
            self.current_label = label_false
            if node.rhs_child.type == "int":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp ne i32 %" + str(rhs_register_count) + ", 0\n"
                self.register_count += 1
            elif node.rhs_child.type == "float":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = fcmp une float %" + str(rhs_register_count) + ", 0.000000e+00\n"
                self.register_count += 1
            self.buffer["functs"] += "\tbr label %" + label_true + "\n\n"

            self.buffer["functs"] += label_true + ":\n"
            self.current_label = label_true
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = phi i1 [ true, %" + label_prev + " ], [ %" + str(self.register_count-1) + ", %" + label_false + " ]\n"
            self.register_count += 1
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = zext i1 %" + str(self.register_count-1) + " to i32\n"
            self.register_count += 1
            
        elif node.operation == "&&":
            label_true = "land.rhs" + str(self.land_count)
            label_false = "land.end" + str(self.land_count)
            label_prev = self.current_label
            self.land_count += 1
            if node.lhs_child.type == "int":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp ne i32 %" + str(lhs_register_count) + ", 0\n"
                self.register_count += 1
            elif node.lhs_child.type == "float":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = fcmp une float %" + str(lhs_register_count) + ", 0.000000e+00\n"
                self.register_count += 1
            self.buffer["functs"] += "\tbr i1 %" + str(self.register_count-1) + ", label %" + label_true + ", label %" + label_false + "\n\n"

            self.buffer["functs"] += label_true + ":\n"
            self.current_label = label_true
            if node.rhs_child.type == "int":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp ne i32 %" + str(rhs_register_count) + ", 0\n"
                self.register_count += 1
            elif node.rhs_child.type == "float":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = fcmp une float %" + str(rhs_register_count) + ", 0.000000e+00\n"
                self.register_count += 1
            self.buffer["functs"] += "\tbr label %" + label_false + "\n\n"

            self.buffer["functs"] += label_false + ":\n"
            self.current_label = label_false
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = phi i1 [ false, %" + label_prev + " ], [ %" + str(self.register_count-1) + ", %" + label_true + " ]\n"
            self.register_count += 1
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
            if type(node.child) is BinExprNode:
                self.visitBinExprNode(node.child)
                child_register_count = self.register_count - 1
            elif type(node.child) is UnaryExprNode:
                self.visitUnaryExprNode(node.child)
                child_register_count = self.register_count - 1
            elif type(node.child) is DeclRefExprNode:
                self.visitDeclRefExprNode(node.child)
                child_register_count = self.register_count - 1
            else:
                raise Exception("Bad UnaryExpr")
        
        if node.operation == "!":
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = icmp ne i32 %" + str(child_register_count) + ", 0\n"
            self.register_count += 1
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = xor i1 %" +str(self.register_count-1)+", true\n"
            self.register_count += 1
            self.buffer["functs"] += "\t%" + str(self.register_count) + " = zext i1 %" + str(self.register_count-1) + " to i32\n"
            self.register_count += 1

    def visitDeclStmtNode(self, node):
        pass
        # if node.child.init:
        #     if node.child.type == "int":
        #         self.buffer["functs"] += "\t%" + str(self.register_count) + " = alloca i32, align 4\n"
        #         self.register_count += 1
        #     elif node.child.type == "float":
        #         self.buffer["functs"] += "\t%" + str(self.register_count) + " = alloca float, align 4\n"
        #         self.register_count += 1
        # else:
        #     if node.child.type == "int":
        #             self.buffer["functs"] += "\t%" + str(self.register_count) + " = alloca i32, align 4\n"
        #             self.register_count += 1
        #     elif node.child.type == "float":
        #         self.buffer["functs"] += "\t%" + str(self.register_count) + " = alloca float, align 4\n"
        #         self.register_count += 1

    def visitDeclRefExprNode(self, node):
        (Ok, Ref) = self.findST(node.ref.id, node.symboltable)
        if Ok:
            if Ref[1].type == "int":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = load i32, i32* %"+str(Ref[0])+", align 4\n"
                self.register_count += 1
            elif Ref[1].type == "float":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = load float, float* %"+str(Ref[0])+", align 4\n"
                self.register_count += 1
            elif Ref[1].type == "char":
                self.buffer["functs"] += "\t%" + str(self.register_count) + " = load i8, i8* %"+str(Ref[0])+", align 4\n"
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
        pass
    
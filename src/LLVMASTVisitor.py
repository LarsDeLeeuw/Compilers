from ASTVisitor import ASTVisitor
from Nodes import *

class LLVMASTVisitor(ASTVisitor):

    def __init__(self):
        self.buffer = {}
        self.register = -1
        # SHOULD PROB WORK WITH SYMBOLTABLE OR SMTHING BUT FIRST ATTEMPT SO ICBA
        self.memory = {}

    def getRegister(self):
        self.register += 1
        return self.register

    def visitProgNode(self, node):
        self.buffer["pre"] = 'declare i32 @printf(i8*, ...)\n@format = private constant [8 x i8] c"d = %d\\0A\\00"\n'
        self.buffer["main"] = "define i32 @main() {\n\tstart:\n"   
        self.buffer["printf"] = 'define void @print(i32 %a){\n\t%p = call i32 (i8*, ...)\n\t\t@printf(i8* getelementptr inbounds ([8 x i8],[8 x i8]* @format,i32 0, i32 0),i32 %a)\n\tret void\n}\n\n'       
 
        for Statement in node.StatementNodes:
            self.visit(Statement)
            
        

        self.buffer["main"] += "\t\tret i32 0\n}\n"
        output = open("main.ll", 'w')
        output.write(self.buffer["pre"]+self.buffer["printf"]+self.buffer["main"])
        output.close()
        return 0

    def visitInitNode(self, node):
        id_node = node.InnerNode

        self.memory[id_node.ID] = str("%" + str(self.getRegister()))
        id_node_type = "i32" # default type
        if type(id_node.PrimitiveNode) is PrimitiveIntNode:
            id_node_type = "i32"
        elif type(id_node.PrimitiveNode) is PrimitiveFloatNode:
            id_node_type = "float"
        else:
            id_node_type = "CHAR???"

        self.buffer["main"] += "\t\t" + self.memory[id_node.ID] + " = alloca "+ id_node_type + ", align 4\n"

        id_node_val = id_node.ExpressionNode.value
        id_node_out = str(id_node_val)
        if id_node_type == "float":
            if str(id_node_val) == str(int(id_node_val)):
                id_node_out += ".0"

        if issubclass(type(id_node.ExpressionNode), LiteralNode):
            self.buffer["main"] += "\t\tstore " + id_node_type + " " 
            self.buffer["main"] += id_node_out + ", " + id_node_type
            self.buffer["main"] += "* " + self.memory[id_node.ID] + ", align 4\n"

    def visitAssignNode(self, node):
        pass

    def visitFunctionNode(self, node):
        temp = str("%" + str(self.getRegister()))
        self.buffer["main"] += "\t\t" + temp + " = load float, float* " + self.memory[node.Args]
        self.buffer["main"] += ", align 4\n"
        temp1 = str("%" + str(self.getRegister()))
        self.buffer["main"] += "\t\t" + temp1 + " = fptosi float " + temp + " to i32\n"
        self.buffer["main"] += "\t\tcall void (i32) @print(i32 " + temp1+ ")\n"



    def visitStatementNode(self, node):
        return self.visit(node.InnerNode)

    def visitBinaryExpressionNode(self, node):
        pass
        
    def visitNegateNode(self, node):
        pass

    def visitLiteralNode(self, node):
        pass

    def visitPrimitiveNode(self, node):
        pass

    def visitIdNode(self, node):
        self.visit(node.ExpressionNode)

    
from subprocess import check_call


class STT:

    def __init__(self): 
        self.root = None
    
    def accept(self, visitor):
        node = self.root
        visitor.visit(node)

    def generateImage(self):
        self.labelbuffer = "node [shape=record]; \n"
        self.edgebuffer = ""
        self.nodecount = 0
        self.refcount = 0
        
        node = self.root
        symbolsstr = "|{ index | id | init}"
        index = 0
        for Symbol in node.symbols:
            if index == len(node.symbols) -1:
                symbolsstr += "|{ " + str(node.symbols[Symbol][0]) + "| " + Symbol + "|" +  str(node.symbols[Symbol][1].init) + "}"
            else:
                symbolsstr += "|{ " + str(node.symbols[Symbol][0]) + "| " + Symbol + "|" +  str(node.symbols[Symbol][1].init) + "}"
            index += 1
        self.labelbuffer += "n"+str(self.nodecount)+' [label="{SymbolTable '+ symbolsstr +'}"];\n'
        storeref = self.nodecount

        for childTable in node.children:
            self.refcount = storeref
            self.nodecount += 1
            self.outNode(childTable)

        outputdotfile = open("symboltable.dot", 'w')
        outputdotfile.write("digraph {" + self.labelbuffer + self.edgebuffer + "}")
        outputdotfile.close()
        check_call(['dot','-Tjpg','symboltable.dot','-o','SymbolOutput.jpg'])
        # Convert to darkmode to spare my eyes.
        check_call(['magick','SymbolOutput.jpg','-negate','SymbolOutput.jpg'])
        


    def outNode(self, node):
        thisnode = "n"+str((self.nodecount))
        self.edgebuffer +=  "n"+str((self.refcount)) +" -> "+ thisnode +"\n"
        symbolsstr = "|{ index | id | init}"
        index = 0
        for Symbol in node.symbols:
            if index == len(node.symbols) -1:
                symbolsstr += "|{ " + str(node.symbols[Symbol][0]) + "| " + Symbol + "|" +  str(node.symbols[Symbol][1].init) + "}"
            else:
                symbolsstr += "|{ " + str(node.symbols[Symbol][0]) + "| " + Symbol + "|" +  str(node.symbols[Symbol][1].init) + "}"
            index += 1
        self.labelbuffer += "n"+str(self.nodecount)+' [label="{SymbolTable '+ symbolsstr +'}"];\n'

        storeref = self.nodecount

        for childTable in node.children:
            self.refcount = storeref
            self.nodecount += 1
            self.outNode(childTable)


class STNode:

    def __init__(self):
        self.parent = None
        self.children = []
        self.symbols = {}
        self.index = 0
    
class STTVisitor:

    def visit(self, node):
        pass
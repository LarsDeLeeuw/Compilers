from subprocess import check_call
import sys

class STT:

    def __init__(self): 
        self.root = None
        self.current_symboltablenode = None

    def lookup(self, symbol_id):
        # Starts looking for symbol_id in current_symboltablenode
        search_symboltablenode = self.current_symboltablenode
        while not (search_symboltablenode is None):
            '''root symboltablenode has None parent'''
            temp = search_symboltablenode.lookup(symbol_id)
            if temp is None:
                search_symboltablenode = search_symboltablenode.parent
            else:
                return temp
        return None

    def insert(self, symbol_id):
        return self.current_symboltablenode.insert(symbol_id)

    def set_attribute(self, symbol_id, attr_name, attr_value):
        return self.current_symboltablenode.set_attribute(symbol_id, attr_name, attr_value)

    def get_attribute(self, symbol_id, attr_name):
        return self.current_symboltablenode.get_attribute(symbol_id, attr_name)

    def new_scope(self):
        if self.root is None:
            self.root = SymbolTableNode()
            self.current_symboltablenode = self.root
            return 0
        new_symboltablenode = SymbolTableNode()
        new_symboltablenode.parent = self.current_symboltablenode
        self.current_symboltablenode.children.append(new_symboltablenode)
        self.current_symboltablenode = new_symboltablenode
        return 0

    def child_scope(self):
        if self.current_symboltablenode.visitcount >= len(self.current_symboltablenode.children):
            raise Exception("All children of scope already visited")
            return None
        self.current_symboltablenode.visitcount += 1
        self.current_symboltablenode = self.current_symboltablenode.children[self.current_symboltablenode.visitcount-1]

    def prev_scope(self):
        if not (self.current_symboltablenode.parent is None):
            self.current_symboltablenode.visitcount = 0
            self.current_symboltablenode = self.current_symboltablenode.parent
            return 0
        else:
            sys.stderr.write("Tried prev_scope on root symboltablenode\n")
            return 1

    def generateImage(self):
        self.labelbuffer = "node [shape=record]; \n"
        self.edgebuffer = ""
        self.nodecount = 0
        self.refcount = 0
        
        node = self.root
        symbolsstr = "|{ index | id | used}"
        index = 0
        for symbol_id in self.root.hashtable.keys():
            if index == self.current_symboltablenode.size -1:
                symbolsstr += "|{ " + str(self.root.hashtable[symbol_id]) + "| " + symbol_id + "|" +  str(self.lookup(symbol_id)["ast_node"].used) + "}"
            else:
                symbolsstr += "|{ " + str(self.root.hashtable[symbol_id]) + "| " + symbol_id + "|" +  str(self.lookup(symbol_id)["ast_node"].used) + "}"
            index += 1
        self.labelbuffer += "n"+str(self.nodecount)+' [label="{SymbolTable '+ symbolsstr +'}"];\n'
        storeref = self.nodecount

        for childTable in self.root.children:
            self.child_scope()
            self.refcount = storeref
            self.nodecount += 1
            self.outNode()
            self.prev_scope()

        self.current_symboltablenode.visitcount = 0
        outputdotfile = open("symboltable.dot", 'w')
        outputdotfile.write("digraph {" + self.labelbuffer + self.edgebuffer + "}")
        outputdotfile.close()
        check_call(['dot','-Tjpg','symboltable.dot','-o','SymbolOutput.jpg'])
        # Convert to darkmode to spare my eyes.
        check_call(['magick','SymbolOutput.jpg','-negate','SymbolOutput.jpg'])
        
    def outNode(self):
        thisnode = "n"+str((self.nodecount))
        self.edgebuffer +=  "n"+str((self.refcount)) +" -> "+ thisnode +"\n"
        symbolsstr = "|{ index | id | used}"
        index = 0
        for symbol_id in self.current_symboltablenode.hashtable.keys():
            if index == self.current_symboltablenode.size -1:
                symbolsstr += "|{ " + str(self.current_symboltablenode.hashtable[symbol_id]) + "| " + symbol_id + "|" +  str(self.lookup(symbol_id)["ast_node"].used) + "}"
            else:
                symbolsstr += "|{ " + str(self.current_symboltablenode.hashtable[symbol_id]) + "| " + symbol_id + "|" +  str(self.lookup(symbol_id)["ast_node"].used) + "}"
            index += 1
        self.labelbuffer += "n"+str(self.nodecount)+' [label="{SymbolTable '+ symbolsstr +'}"];\n'

        storeref = self.nodecount

        for childTable in self.current_symboltablenode.children:
            self.child_scope()
            self.refcount = storeref
            self.nodecount += 1
            self.outNode()
            self.prev_scope()


class SymbolTableNode:

    def __init__(self):
        self.parent = None
        self.children = []    
        self.symboltable = {}   # index -> {atr1 : val_atr1, atr2 : val_atr2, ...}
        self.hashtable = {}     # ID -> index (0..len(symbols)-1)
        self.size = 0
        self.visitcount = 0

    def insert(self, symbol_id):
        # Check if symbol_id already in symboltable
        if symbol_id in self.hashtable.keys():
            sys.stderr.write("Tried inserting symbol_id that was already present in symboltable")
            return None
        else:
            self.hashtable[symbol_id] = self.size
            self.symboltable[self.size] = {}        # Attribute dictionary
            self.size += 1
            return self.symboltable[self.size-1]

    def lookup(self, symbol_id):
        # Check if symbol_id in symboltable
        if symbol_id in self.hashtable.keys():
            return self.symboltable[self.hashtable[symbol_id]] # Return the attribute dictionary
        else:
            return None

    def set_attribute(self, symbol_id, attr_name, attr_value):
        # Check if symbol_id in symboltable
        if symbol_id in self.hashtable.keys():
            self.symboltable[self.hashtable[symbol_id]][attr_name] = attr_value
            return 0
        else:
            sys.stderr.write("Tried set_attribute for symbol_id not present in symboltable\n")
            return 1

    def get_attribute(self, symbol_id, attr_name):
         # Check if symbol_id in symboltable
        if symbol_id in self.hashtable.keys():
            if attr_name in self.symboltable[self.hashtable[symbol_id]].keys():
                return self.symboltable[self.hashtable[symbol_id]][attr_name]
            else:
                sys.stderr.write("Tried get_attribute for attr_name not present in the attributes of symbol_id\n")
                return None
        else:
            sys.stderr.write("Tried get_attribute for symbol_id not present in symboltable\n")
            return None



    
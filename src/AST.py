#===================================================================#
# Name        : test_ass1.py                                        #
# Author      : Lars De Leeuw                                       #
# Date        : 11/03/2022                                          #
# Version     : 0.1                                                 #
# Description : unittest.TestSuite containing all unittest.TestCase #
#               associated with testing the quality, features       #
#               and requirements implemented for assignment 1.      #
#===================================================================#


class AST:

    def __init__(self): 
        self.root = None

    def setRoot(self, node):
        self.root = node
    
    def accept(self, visitor):
        node = self.root
        visitor.visit(node)
    
    def save(self, file):
        output = open(file, 'w')
        output.write("<Ast>\n" + self.root.save() + "</Ast>")
        return 0
    
    def load(self, file):
        return 0
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
        print(type(node))
        visitor.visit(node)
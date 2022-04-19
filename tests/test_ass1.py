#===================================================================#
# Name        : test_ass1.py                                        #
# Author      : Lars De Leeuw                                       #
# Date        : 11/03/2022                                          #
# Version     : 0.1                                                 #
# Description : unittest.TestSuite containing all unittest.TestCase #
#               associated with testing the quality, features       #
#               and requirements implemented for assignment 1.      #
#===================================================================#
import unittest
import sys
from os.path import exists
from antlr4 import *
from src.GrammarLexer import GrammarLexer
from src.GrammarParser import GrammarParser
from src.BuildASTVisitor import BuildASTVisitor
from src.VisualASTVisitor import VisualASTVisitor
from src.ConstFoldingASTVisitor import ConstFoldingASTVisitor


class TestStringMethods(unittest.TestCase):
    """Example of unittest.TestCase, try and use docstrings like this"""
    def test_upper(self):
        """Tests the upper method of a string object."""
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        """Tests the isupper method of a string object."""
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        """Tests the split method of a string object."""
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

class TestBinaryOperators(unittest.TestCase):
    """TestCase for expressions containing only binary operators"""
        
    def test_binOp1(self):
        if not exists("input/bin_op_1"):
            self.skipTest("required inputfile missing")
        input_stream = FileStream("input/bin_op_1")
        lexer = GrammarLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = GrammarParser(stream)
        cst = parser.prog()
        builder = BuildASTVisitor()
        builder.visit(cst)
        AST = builder.getAST()
        
        self.assertEqual('foo', 'foo')
    
    def test_binOp2(self):
        self.assertEqual('ff', 'ff')
    

def suite():
    """Creates unittest.TestSuite"""
    suite = unittest.TestSuite()
    suite.addCase(TestBinaryOperator)
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
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


def suite():
    """Creates unittest.TestSuite"""
    suite = unittest.TestSuite()
    suite.addCase(TestStringMethods)
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
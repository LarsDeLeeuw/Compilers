'''
╔═══════════════════════════════════════════════════════════════════╗
║ Name        : test_correctcode_mips.py                            ║
║ Author      : Lars De Leeuw                                       ║
║ Date        : 03/06/2022                                          ║
║ Version     : 0.1                                                 ║
║ Description : unittest.TestSuite containing all unittest.TestCase ║
║               associated with testing the output MIPS generated   ║
║               by my compiler.                                     ║
╚═══════════════════════════════════════════════════════════════════╝
'''
import unittest
import sys
import re
import io
from os.path import exists
from subprocess import call, run


class TestBenchmarkCorrectCodeMIPS(unittest.TestCase):
    """Test"""
        
    def test_binaryOperations1(self):
        name = "binaryOperations1"
        inputfile = "../CompilersBenchmark/CorrectCode/"+name+".c"

        if not exists(name):
            self.skipTest("Could not find Reference Output.")
        
        call(['python', '../../src/main.py', "-f"+inputfile, "-c 1"])
        MIPSOutput = open("MIPSOutput", "w")
        Copyrightcleanup = re.split(r"b'MARS 4.5  Copyright 2003-2014 Pete Sanderson and Kenneth Vollmar\\n\\n", str(run(['java','-jar', 'Mars4_5.jar', "main.asm"], capture_output=True).stdout))
        Copyrightcleanup = re.split(r"\\n'$", Copyrightcleanup[1])
        Copyrightcleanup = Copyrightcleanup[0]
        MIPSOutput.write(Copyrightcleanup)
        MIPSOutput.close()

        GeneratedFile = open("MIPSOutput", "r")
        RefFile = open(name, "r")
        self.assertListEqual(list(GeneratedFile), list(RefFile))
        GeneratedFile.close()
        RefFile.close()

    def test_binaryOperations2(self):
        name = "binaryOperations2"
        inputfile = "../CompilersBenchmark/CorrectCode/"+name+".c"

        if not exists(name):
            self.skipTest("Could not find Reference Output.")
        
        call(['python', '../../src/main.py', "-f"+inputfile, "-c 1"])
        MIPSOutput = open("MIPSOutput", "w")
        Copyrightcleanup = re.split(r"b'MARS 4.5  Copyright 2003-2014 Pete Sanderson and Kenneth Vollmar\\n\\n", str(run(['java','-jar', 'Mars4_5.jar', "main.asm"], capture_output=True).stdout))
        Copyrightcleanup = re.split(r"\\n'$", Copyrightcleanup[1])
        Copyrightcleanup = Copyrightcleanup[0]
        MIPSOutput.write(Copyrightcleanup)
        MIPSOutput.close()

        GeneratedFile = open("MIPSOutput", "r")
        RefFile = open(name, "r")
        self.assertListEqual(list(GeneratedFile), list(RefFile))
        GeneratedFile.close()
        RefFile.close()


def suite():
    """Creates unittest.TestSuite"""
    suite = unittest.TestSuite()
    suite.addCase(TestBenchmarkCorrectCodeLLVM)
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
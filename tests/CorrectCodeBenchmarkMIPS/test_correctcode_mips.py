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
        name = "oracle/{}".format(name)
        if not exists(name):
            self.skipTest("Could not find Reference Output.")
        
        call(['python', '../../src/main.py', "-f"+inputfile, "-c 1"])
        MIPSOutput = open("MIPSOutput", "w")
        Copyrightcleanup = re.split(r"^MARS 4.5  Copyright 2003-2014 Pete Sanderson and Kenneth Vollmar\n\n", (run(['java','-jar', 'Mars4_5.jar', "main.asm"], capture_output=True).stdout).decode("utf-8"))
        Copyrightcleanup = Copyrightcleanup[1][0:-1]
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
        name = "oracle/{}".format(name)
        if not exists(name):
            self.skipTest("Could not find Reference Output.")
        
        call(['python', '../../src/main.py', "-f"+inputfile, "-c 1"])
        MIPSOutput = open("MIPSOutput", "w")
        Copyrightcleanup = re.split(r"^MARS 4.5  Copyright 2003-2014 Pete Sanderson and Kenneth Vollmar\n\n", (run(['java','-jar', 'Mars4_5.jar', "main.asm"], capture_output=True).stdout).decode("utf-8"))
        Copyrightcleanup = Copyrightcleanup[1][0:-1]
        MIPSOutput.write(Copyrightcleanup)
        MIPSOutput.close()

        GeneratedFile = open("MIPSOutput", "r")
        RefFile = open(name, "r")
        self.assertListEqual(list(GeneratedFile), list(RefFile))
        GeneratedFile.close()
        RefFile.close()

    def test_comparisons1(self):
        name = "comparisons1"
        inputfile = "../CompilersBenchmark/CorrectCode/"+name+".c"
        name = "oracle/{}".format(name)
        if not exists(name):
            self.skipTest("Could not find Reference Output.")
        
        call(['python', '../../src/main.py', "-f"+inputfile, "-c 1"])
        MIPSOutput = open("MIPSOutput", "w")
        Copyrightcleanup = re.split(r"^MARS 4.5  Copyright 2003-2014 Pete Sanderson and Kenneth Vollmar\n\n", (run(['java','-jar', 'Mars4_5.jar', "main.asm"], capture_output=True).stdout).decode("utf-8"))
        Copyrightcleanup = Copyrightcleanup[1][0:-1]
        MIPSOutput.write(Copyrightcleanup)
        MIPSOutput.close()

        GeneratedFile = open("MIPSOutput", "r")
        RefFile = open(name, "r")
        self.assertListEqual(list(GeneratedFile), list(RefFile))
        GeneratedFile.close()
        RefFile.close()

    def test_comparisons2(self):
        name = "comparisons2"
        inputfile = "../CompilersBenchmark/CorrectCode/"+name+".c"
        name = "oracle/{}".format(name)
        if not exists(name):
            self.skipTest("Could not find Reference Output.")
        
        call(['python', '../../src/main.py', "-f"+inputfile, "-c 1"])
        MIPSOutput = open("MIPSOutput", "w")
        Copyrightcleanup = re.split(r"^MARS 4.5  Copyright 2003-2014 Pete Sanderson and Kenneth Vollmar\n\n", (run(['java','-jar', 'Mars4_5.jar', "main.asm"], capture_output=True).stdout).decode("utf-8"))
        Copyrightcleanup = Copyrightcleanup[1][0:-1]
        MIPSOutput.write(Copyrightcleanup)
        MIPSOutput.close()

        GeneratedFile = open("MIPSOutput", "r")
        RefFile = open(name, "r")
        self.assertListEqual(list(GeneratedFile), list(RefFile))
        GeneratedFile.close()
        RefFile.close()

    def test_dereferenceAssignment(self):
        name = "dereferenceAssignment"
        inputfile = "../CompilersBenchmark/CorrectCode/"+name+".c"
        name = "oracle/{}".format(name)
        if not exists(name):
            self.skipTest("Could not find Reference Output.")
        
        call(['python', '../../src/main.py', "-f"+inputfile, "-c 1"])
        MIPSOutput = open("MIPSOutput", "w")
        Copyrightcleanup = re.split(r"^MARS 4.5  Copyright 2003-2014 Pete Sanderson and Kenneth Vollmar\n\n", (run(['java','-jar', 'Mars4_5.jar', "main.asm"], capture_output=True).stdout).decode("utf-8"))
        Copyrightcleanup = Copyrightcleanup[1][0:-1]
        MIPSOutput.write(Copyrightcleanup)
        MIPSOutput.close()

        GeneratedFile = open("MIPSOutput", "r")
        RefFile = open(name, "r")
        self.assertListEqual(list(GeneratedFile), list(RefFile))
        GeneratedFile.close()
        RefFile.close()

    def test_if(self):
        name = "if"
        inputfile = "../CompilersBenchmark/CorrectCode/"+name+".c"
        name = "oracle/{}".format(name)
        if not exists(name):
            self.skipTest("Could not find Reference Output.")
        
        call(['python', '../../src/main.py', "-f"+inputfile, "-c 1"])
        MIPSOutput = open("MIPSOutput", "w")
        Copyrightcleanup = re.split(r"^MARS 4.5  Copyright 2003-2014 Pete Sanderson and Kenneth Vollmar\n\n", (run(['java','-jar', 'Mars4_5.jar', "main.asm"], capture_output=True).stdout).decode("utf-8"))
        Copyrightcleanup = Copyrightcleanup[1][0:-1]
        MIPSOutput.write(Copyrightcleanup)
        MIPSOutput.close()

        GeneratedFile = open("MIPSOutput", "r")
        RefFile = open(name, "r")
        self.assertListEqual(list(GeneratedFile), list(RefFile))
        GeneratedFile.close()
        RefFile.close()

    def test_ifElse(self):
        name = "ifElse"
        inputfile = "../CompilersBenchmark/CorrectCode/"+name+".c"
        name = "oracle/{}".format(name)
        if not exists(name):
            self.skipTest("Could not find Reference Output.")
        
        call(['python', '../../src/main.py', "-f"+inputfile, "-c 1"])
        MIPSOutput = open("MIPSOutput", "w")
        Copyrightcleanup = re.split(r"^MARS 4.5  Copyright 2003-2014 Pete Sanderson and Kenneth Vollmar\n\n", (run(['java','-jar', 'Mars4_5.jar', "main.asm"], capture_output=True).stdout).decode("utf-8"))
        Copyrightcleanup = Copyrightcleanup[1][0:-1]
        MIPSOutput.write(Copyrightcleanup)
        MIPSOutput.close()

        GeneratedFile = open("MIPSOutput", "r")
        RefFile = open(name, "r")
        self.assertListEqual(list(GeneratedFile), list(RefFile))
        GeneratedFile.close()
        RefFile.close()

    def test_printf1(self):
        name = "printf1"
        inputfile = "../CompilersBenchmark/CorrectCode/"+name+".c"
        name = "oracle/{}".format(name)
        if not exists(name):
            self.skipTest("Could not find Reference Output.")
        
        call(['python', '../../src/main.py', "-f"+inputfile, "-c 1"])
        MIPSOutput = open("MIPSOutput", "w")
        Copyrightcleanup = re.split(r"^MARS 4.5  Copyright 2003-2014 Pete Sanderson and Kenneth Vollmar\n\n", (run(['java','-jar', 'Mars4_5.jar', "main.asm"], capture_output=True).stdout).decode("utf-8"))
        Copyrightcleanup = Copyrightcleanup[1][0:-1]
        MIPSOutput.write(Copyrightcleanup)
        MIPSOutput.close()

        GeneratedFile = open("MIPSOutput", "r")
        RefFile = open(name, "r")
        self.assertListEqual(list(GeneratedFile), list(RefFile))
        GeneratedFile.close()
        RefFile.close()
    
    def test_printf2(self):
        name = "printf2"
        inputfile = "../CompilersBenchmark/CorrectCode/"+name+".c"
        name = "oracle/{}".format(name)
        if not exists(name):
            self.skipTest("Could not find Reference Output.")
        
        call(['python', '../../src/main.py', "-f"+inputfile, "-c 1"])
        MIPSOutput = open("MIPSOutput", "w")
        Copyrightcleanup = re.split(r"^MARS 4.5  Copyright 2003-2014 Pete Sanderson and Kenneth Vollmar\n\n", (run(['java','-jar', 'Mars4_5.jar', "main.asm"], capture_output=True).stdout).decode("utf-8"))
        Copyrightcleanup = Copyrightcleanup[1][0:-1]
        MIPSOutput.write(Copyrightcleanup)
        MIPSOutput.close()

        GeneratedFile = open("MIPSOutput", "r")
        RefFile = open(name, "r")
        self.assertListEqual(list(GeneratedFile), list(RefFile))
        GeneratedFile.close()
        RefFile.close()

    def test_printf3(self):
        name = "printf3"
        inputfile = "../CompilersBenchmark/CorrectCode/"+name+".c"
        name = "oracle/{}".format(name)
        if not exists(name):
            self.skipTest("Could not find Reference Output.")
        
        call(['python', '../../src/main.py', "-f"+inputfile, "-c 1"])
        MIPSOutput = open("MIPSOutput", "w")
        Copyrightcleanup = re.split(r"^MARS 4.5  Copyright 2003-2014 Pete Sanderson and Kenneth Vollmar\n\n", (run(['java','-jar', 'Mars4_5.jar', "main.asm"], capture_output=True).stdout).decode("utf-8"))
        Copyrightcleanup = Copyrightcleanup[1][0:-1]
        MIPSOutput.write(Copyrightcleanup)
        MIPSOutput.close()

        GeneratedFile = open("MIPSOutput", "r")
        RefFile = open(name, "r")
        self.assertListEqual(list(GeneratedFile), list(RefFile))
        GeneratedFile.close()
        RefFile.close()

    def test_scoping(self):
        name = "scoping"
        inputfile = "../CompilersBenchmark/CorrectCode/"+name+".c"

        name = "oracle/{}".format(name)

        if not exists(name):
            self.skipTest("Could not find Reference Output.")
        
        call(['python', '../../src/main.py', "-f"+inputfile, "-c 1"])
        MIPSOutput = open("MIPSOutput", "w")
        Copyrightcleanup = re.split(r"^MARS 4.5  Copyright 2003-2014 Pete Sanderson and Kenneth Vollmar\n\n", (run(['java','-jar', 'Mars4_5.jar', "main.asm"], capture_output=True).stdout).decode("utf-8"))
        Copyrightcleanup = Copyrightcleanup[1][0:-1]
        MIPSOutput.write(Copyrightcleanup)
        MIPSOutput.close()

        GeneratedFile = open("MIPSOutput", "r")
        RefFile = open(name, "r")
        self.assertListEqual(list(GeneratedFile), list(RefFile))
        GeneratedFile.close()
        RefFile.close()
    
    def test_variables1(self):
        name = "variables1"
        inputfile = "../CompilersBenchmark/CorrectCode/"+name+".c"
        name = "oracle/{}".format(name)
        if not exists(name):
            self.skipTest("Could not find Reference Output.")
        
        call(['python', '../../src/main.py', "-f"+inputfile, "-c 1"])
        MIPSOutput = open("MIPSOutput", "w")
        Copyrightcleanup = re.split(r"^MARS 4.5  Copyright 2003-2014 Pete Sanderson and Kenneth Vollmar\n\n", (run(['java','-jar', 'Mars4_5.jar', "main.asm"], capture_output=True).stdout).decode("utf-8"))
        Copyrightcleanup = Copyrightcleanup[1][0:-1]
        MIPSOutput.write(Copyrightcleanup)
        MIPSOutput.close()

        GeneratedFile = open("MIPSOutput", "r")
        RefFile = open(name, "r")
        self.assertListEqual(list(GeneratedFile), list(RefFile))
        GeneratedFile.close()
        RefFile.close()
    
    def test_variables2(self):
        name = "variables2"
        inputfile = "../CompilersBenchmark/CorrectCode/"+name+".c"
        name = "oracle/{}".format(name)
        if not exists(name):
            self.skipTest("Could not find Reference Output.")
        
        call(['python', '../../src/main.py', "-f"+inputfile, "-c 1"])
        MIPSOutput = open("MIPSOutput", "w")
        Copyrightcleanup = re.split(r"^MARS 4.5  Copyright 2003-2014 Pete Sanderson and Kenneth Vollmar\n\n", (run(['java','-jar', 'Mars4_5.jar', "main.asm"], capture_output=True).stdout).decode("utf-8"))
        Copyrightcleanup = Copyrightcleanup[1][0:-1]
        MIPSOutput.write(Copyrightcleanup)
        MIPSOutput.close()

        GeneratedFile = open("MIPSOutput", "r")
        RefFile = open(name, "r")
        self.assertListEqual(list(GeneratedFile), list(RefFile))
        GeneratedFile.close()
        RefFile.close()

    def test_variables4(self):
        name = "variables4"
        inputfile = "../CompilersBenchmark/CorrectCode/"+name+".c"
        name = "oracle/{}".format(name)
        if not exists(name):
            self.skipTest("Could not find Reference Output.")
        
        call(['python', '../../src/main.py', "-f"+inputfile, "-c 1"])
        MIPSOutput = open("MIPSOutput", "w")
        Copyrightcleanup = re.split(r"^MARS 4.5  Copyright 2003-2014 Pete Sanderson and Kenneth Vollmar\n\n", (run(['java','-jar', 'Mars4_5.jar', "main.asm"], capture_output=True).stdout).decode("utf-8"))
        Copyrightcleanup = Copyrightcleanup[1][0:-1]
        MIPSOutput.write(Copyrightcleanup)
        MIPSOutput.close()

        GeneratedFile = open("MIPSOutput", "r")
        RefFile = open(name, "r")
        self.assertListEqual(list(GeneratedFile), list(RefFile))
        GeneratedFile.close()
        RefFile.close()
    
    def test_variables5(self):
        name = "variables5"
        inputfile = "../CompilersBenchmark/CorrectCode/"+name+".c"
        name = "oracle/{}".format(name)
        if not exists(name):
            self.skipTest("Could not find Reference Output.")
        
        call(['python', '../../src/main.py', "-f"+inputfile, "-c 1"])
        MIPSOutput = open("MIPSOutput", "w")
        Copyrightcleanup = re.split(r"^MARS 4.5  Copyright 2003-2014 Pete Sanderson and Kenneth Vollmar\n\n", (run(['java','-jar', 'Mars4_5.jar', "main.asm"], capture_output=True).stdout).decode("utf-8"))
        Copyrightcleanup = Copyrightcleanup[1][0:-1]
        MIPSOutput.write(Copyrightcleanup)
        MIPSOutput.close()

        GeneratedFile = open("MIPSOutput", "r")
        RefFile = open(name, "r")
        self.assertListEqual(list(GeneratedFile), list(RefFile))
        GeneratedFile.close()
        RefFile.close()

    def test_variables6(self):
        name = "variables6"
        inputfile = "../CompilersBenchmark/CorrectCode/"+name+".c"
        name = "oracle/{}".format(name)
        if not exists(name):
            self.skipTest("Could not find Reference Output.")
        
        call(['python', '../../src/main.py', "-f"+inputfile, "-c 1"])
        MIPSOutput = open("MIPSOutput", "w")
        Copyrightcleanup = re.split(r"^MARS 4.5  Copyright 2003-2014 Pete Sanderson and Kenneth Vollmar\n\n", (run(['java','-jar', 'Mars4_5.jar', "main.asm"], capture_output=True).stdout).decode("utf-8"))
        Copyrightcleanup = Copyrightcleanup[1][0:-1]
        MIPSOutput.write(Copyrightcleanup)
        MIPSOutput.close()

        GeneratedFile = open("MIPSOutput", "r")
        RefFile = open(name, "r")
        self.assertListEqual(list(GeneratedFile), list(RefFile))
        GeneratedFile.close()
        RefFile.close()

    def test_while(self):
        name = "while"
        inputfile = "../CompilersBenchmark/CorrectCode/"+name+".c"
        name = "oracle/{}".format(name)
        if not exists(name):
            self.skipTest("Could not find Reference Output.")
        
        call(['python', '../../src/main.py', "-f"+inputfile, "-c 1"])
        MIPSOutput = open("MIPSOutput", "w")
        Copyrightcleanup = re.split(r"^MARS 4.5  Copyright 2003-2014 Pete Sanderson and Kenneth Vollmar\n\n", (run(['java','-jar', 'Mars4_5.jar', "main.asm"], capture_output=True).stdout).decode("utf-8"))
        Copyrightcleanup = Copyrightcleanup[1][0:-1]
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
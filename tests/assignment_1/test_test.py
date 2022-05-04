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
import io
from os.path import exists
from subprocess import call, run


class TestBenchmarkCorrectCode(unittest.TestCase):
    """TestCase for expressions containing only binary operators"""
        
    def test_binaryOperations1(self):
        inputfile = "../CompilersBenchmark/CorrectCode/binaryOperations1.c"
        call(['python', '../../src/main.py', "-f"+inputfile])
        LLVMOutput = open("LLVMOutput", "w")
        LLVMOutput.write(str(run(['lli', 'main.ll'], capture_output=True).stdout))
        LLVMOutput.close()
        
        if not exists("binaryOperations1.ll"):
            run(["clang", "-w", "-S", inputfile, "-emit-llvm"])        

        CLANGLLVM = open("CLANGLLVM", 'w')
        CLANGLLVM.write(str(run(['lli', 'binaryOperations1.ll'], capture_output=True).stdout))
        CLANGLLVM.close()

        LLVMINPUT = open("LLVMOutput", "r")
        CLANGLLVM = open("CLANGLLVM", "r")
        self.assertListEqual(list(LLVMINPUT), list(CLANGLLVM))
        LLVMINPUT.close()
        CLANGLLVM.close()

    
    def test_binaryOperations2(self):
        inputfile = "../CompilersBenchmark/CorrectCode/binaryOperations2.c"
        call(['python', '../../src/main.py', "-f"+inputfile])
        LLVMOutput = open("LLVMOutput", "w")
        LLVMOutput.write(str(run(['lli', 'main.ll'], capture_output=True).stdout))
        LLVMOutput.close()
        
        if not exists("binaryOperations2.ll"):
            run(["clang", "-w", "-S", inputfile, "-emit-llvm"])
        
        CLANGLLVM = open("CLANGLLVM", 'w')
        CLANGLLVM.write(str(run(['lli', 'binaryOperations2.ll'], capture_output=True).stdout))
        CLANGLLVM.close()

        LLVMINPUT = open("LLVMOutput", "r")
        CLANGLLVM = open("CLANGLLVM", "r")
        self.assertListEqual(list(LLVMINPUT), list(CLANGLLVM))
        LLVMINPUT.close()
        CLANGLLVM.close()

    def test_breakAndContinue(self):
        if not exists("input/dummy"):
            self.skipTest("not developed yet")
        inputfile = "../CompilersBenchmark/CorrectCode/breakAndContinue.c"
        call(['python', '../../src/main.py', "-f"+inputfile])
        LLVMOutput = open("LLVMOutput", "w")
        LLVMOutput.write(str(run(['lli', 'main.ll'], capture_output=True).stdout))
        LLVMOutput.close()
        
        if not exists("breakAndContinue.ll"):
            run(["clang", "-w", "-S", inputfile, "-emit-llvm"])
        
        CLANGLLVM = open("CLANGLLVM", 'w')
        CLANGLLVM.write(str(run(['lli', 'breakAndContinue.ll'], capture_output=True).stdout))
        CLANGLLVM.close()

        LLVMINPUT = open("LLVMOutput", "r")
        CLANGLLVM = open("CLANGLLVM", "r")
        self.assertListEqual(list(LLVMINPUT), list(CLANGLLVM))
        LLVMINPUT.close()
        CLANGLLVM.close()

    def test_comparisons1(self):
        inputfile = "../CompilersBenchmark/CorrectCode/comparisons1.c"
        call(['python', '../../src/main.py', "-f"+inputfile])
        LLVMOutput = open("LLVMOutput", "w")
        LLVMOutput.write(str(run(['lli', 'main.ll'], capture_output=True).stdout))
        LLVMOutput.close()
        
        if not exists("comparisons1.ll"):
            run(["clang", "-w", "-S", inputfile, "-emit-llvm"])
        
        CLANGLLVM = open("CLANGLLVM", 'w')
        CLANGLLVM.write(str(run(['lli', 'comparisons1.ll'], capture_output=True).stdout))
        CLANGLLVM.close()

        LLVMINPUT = open("LLVMOutput", "r")
        CLANGLLVM = open("CLANGLLVM", "r")
        self.assertListEqual(list(LLVMINPUT), list(CLANGLLVM))
        LLVMINPUT.close()
        CLANGLLVM.close()
    
    def test_comparisons2(self):
        inputfile = "../CompilersBenchmark/CorrectCode/comparisons2.c"
        call(['python', '../../src/main.py', "-f"+inputfile])
        LLVMOutput = open("LLVMOutput", "w")
        LLVMOutput.write(str(run(['lli', 'main.ll'], capture_output=True).stdout))
        LLVMOutput.close()
        
        if not exists("comparisons2.ll"):
            run(["clang", "-w", "-S", inputfile, "-emit-llvm"])

        CLANGLLVM = open("CLANGLLVM", 'w')
        CLANGLLVM.write(str(run(['lli', 'comparisons2.ll'], capture_output=True).stdout))
        CLANGLLVM.close()

        LLVMINPUT = open("LLVMOutput", "r")
        CLANGLLVM = open("CLANGLLVM", "r")
        self.assertListEqual(list(LLVMINPUT), list(CLANGLLVM))
        LLVMINPUT.close()
        CLANGLLVM.close()

    def test_variables1(self):
        inputfile = "../CompilersBenchmark/CorrectCode/variables1.c"
        call(['python', '../../src/main.py', "-f"+inputfile])
        LLVMOutput = open("LLVMOutput", "w")
        LLVMOutput.write(str(run(['lli', 'main.ll'], capture_output=True).stdout))
        LLVMOutput.close()
        
        if not exists("variables1.ll"):
            run(["clang", "-w", "-S", inputfile, "-emit-llvm"])

        CLANGLLVM = open("CLANGLLVM", 'w')
        CLANGLLVM.write(str(run(['lli', 'variables1.ll'], capture_output=True).stdout))
        CLANGLLVM.close()

        LLVMINPUT = open("LLVMOutput", "r")
        CLANGLLVM = open("CLANGLLVM", "r")
        self.assertListEqual(list(LLVMINPUT), list(CLANGLLVM))
        LLVMINPUT.close()
        CLANGLLVM.close()

    def test_if(self):
        inputfile = "../CompilersBenchmark/CorrectCode/if.c"
        call(['python', '../../src/main.py', "-f"+inputfile])
        LLVMOutput = open("LLVMOutput", "w")
        LLVMOutput.write(str(run(['lli', 'main.ll'], capture_output=True).stdout))
        LLVMOutput.close()
        
        if not exists("if.ll"):
            run(["clang", "-w", "-S", inputfile, "-emit-llvm"])

        CLANGLLVM = open("CLANGLLVM", 'w')
        CLANGLLVM.write(str(run(['lli', 'if.ll'], capture_output=True).stdout))
        CLANGLLVM.close()

        LLVMINPUT = open("LLVMOutput", "r")
        CLANGLLVM = open("CLANGLLVM", "r")
        self.assertListEqual(list(LLVMINPUT), list(CLANGLLVM))
        LLVMINPUT.close()
        CLANGLLVM.close()

    def test_ifElse(self):
        inputfile = "../CompilersBenchmark/CorrectCode/ifElse.c"
        call(['python', '../../src/main.py', "-f"+inputfile])
        LLVMOutput = open("LLVMOutput", "w")
        LLVMOutput.write(str(run(['lli', 'main.ll'], capture_output=True).stdout))
        LLVMOutput.close()
        
        if not exists("ifElse.ll"):
            run(["clang", "-w", "-S", inputfile, "-emit-llvm"])

        CLANGLLVM = open("CLANGLLVM", 'w')
        CLANGLLVM.write(str(run(['lli', 'ifElse.ll'], capture_output=True).stdout))
        CLANGLLVM.close()

        LLVMINPUT = open("LLVMOutput", "r")
        CLANGLLVM = open("CLANGLLVM", "r")
        self.assertListEqual(list(LLVMINPUT), list(CLANGLLVM))
        LLVMINPUT.close()
        CLANGLLVM.close()

    

def suite():
    """Creates unittest.TestSuite"""
    suite = unittest.TestSuite()
    suite.addCase(TestBenchmarkCorrectCode)
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
#!/usr/bin/env python3
"""
Unit tests for SimpleCPU
"""

import unittest
from cpu import SimpleCPU
from assembler import Assembler

class TestCPU(unittest.TestCase):
    def setUp(self):
        self.cpu = SimpleCPU()
        self.asm = Assembler()

    def test_load_immediate(self):
        """Test LI instruction"""
        code = self.asm.assemble("LI R1, 42\nHLT")
        self.cpu.load_program(code)
        self.cpu.run()
        self.assertEqual(self.cpu.registers[1], 42)

    def test_add(self):
        """Test ADD instruction"""
        code = self.asm.assemble("""
            LI R1, 10
            LI R2, 20
            ADD R1, R2
            HLT
        """)
        self.cpu.load_program(code)
        self.cpu.run()
        self.assertEqual(self.cpu.registers[1], 30)

    def test_sub(self):
        """Test SUB instruction"""
        code = self.asm.assemble("""
            LI R1, 50
            LI R2, 30
            SUB R1, R2
            HLT
        """)
        self.cpu.load_program(code)
        self.cpu.run()
        self.assertEqual(self.cpu.registers[1], 20)

    def test_loop(self):
        """Test loop with JNZ"""
        code = self.asm.assemble("""
            LI R1, 5
            LI R2, 0
        loop:
            INC R2
            DEC R1
            JNZ R1, loop
            HLT
        """)
        self.cpu.load_program(code)
        self.cpu.run()
        self.assertEqual(self.cpu.registers[1], 0)
        self.assertEqual(self.cpu.registers[2], 5)

    def test_memory(self):
        """Test LOAD/STORE"""
        self.cpu.memory[100] = 999
        code = self.asm.assemble("""
            LOAD R1, 100
            LI R2, 50
            ADD R1, R2
            STORE R1, 101
            HLT
        """)
        self.cpu.load_program(code)
        self.cpu.run()
        self.assertEqual(self.cpu.memory[101], 1049)

    def test_r0_always_zero(self):
        """Test that R0 is always 0"""
        code = self.asm.assemble("""
            LI R0, 100
            HLT
        """)
        self.cpu.load_program(code)
        self.cpu.run()
        self.assertEqual(self.cpu.registers[0], 0)

class TestAssembler(unittest.TestCase):
    def setUp(self):
        self.asm = Assembler()

    def test_labels(self):
        """Test label resolution"""
        code = self.asm.assemble("""
        start:
            LI R1, 1
            JMP end
            LI R2, 2
        end:
            HLT
        """)
        self.assertEqual(len(code), 4)

    def test_comments(self):
        """Test comment handling"""
        code = self.asm.assemble("""
            LI R1, 10  ; this is a comment
            # another comment style
            HLT
        """)
        self.assertEqual(len(code), 2)

def run_tests():
    """Run all tests with verbose output"""
    print("Running CPU tests...\n")
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestCPU))
    suite.addTests(loader.loadTestsFromTestCase(TestAssembler))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print(f"\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"{'='*50}")

    return result.wasSuccessful()

if __name__ == '__main__':
    run_tests()

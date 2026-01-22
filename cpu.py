"""
SimpleCPU - 16-bit processor simulator
Architecture: 8 registers (R0=0 fixed), 64KB memory, 16-bit instructions
"""

class SimpleCPU:
    def __init__(self, memory_size: int = 65536, verbose: bool = False):
        self.memory = [0] * memory_size
        self.registers = [0] * 8  # R0 always 0
        self.pc = 0
        self.halted = False
        self.verbose = verbose
        self.cycle_count = 0

    def reset(self):
        self.registers = [0] * 8
        self.pc = 0
        self.halted = False
        self.cycle_count = 0

    def load_program(self, program: list[int], start_addr: int = 0):
        """Load binary program into memory at start_addr"""
        for i, word in enumerate(program):
            self.memory[start_addr + i] = word & 0xFFFF

    def _decode(self, instr: int) -> tuple:
        """Decode instruction into (opcode, regA, regB, immediate)"""
        opcode = (instr >> 12) & 0xF
        reg_a = (instr >> 8) & 0xF
        reg_b = (instr >> 4) & 0xF
        imm = instr & 0xFF  # 8-bit immediate for extended range
        return opcode, reg_a, reg_b, imm

    def _log(self, msg: str):
        if self.verbose:
            print(f"[Cycle {self.cycle_count:4d}] {msg}")

    def step(self) -> bool:
        """Execute one instruction. Returns False if halted."""
        if self.halted or self.pc >= len(self.memory):
            return False

        instr = self.memory[self.pc]
        opcode, a, b, imm = self._decode(instr)
        self.registers[0] = 0  # R0 hardwired to 0

        old_pc = self.pc
        self.pc += 1

        if opcode == 0x0:  # LOAD Rd, addr
            self.registers[a] = self.memory[imm]
            self._log(f"LOAD R{a} <- mem[{imm}] = {self.registers[a]}")

        elif opcode == 0x1:  # STORE Rs, addr
            self.memory[imm] = self.registers[a]
            self._log(f"STORE mem[{imm}] <- R{a} = {self.registers[a]}")

        elif opcode == 0x2:  # ADD Rd, Rs
            result = (self.registers[a] + self.registers[b]) & 0xFFFF
            self._log(f"ADD R{a} = {self.registers[a]} + R{b}({self.registers[b]}) = {result}")
            self.registers[a] = result

        elif opcode == 0x3:  # SUB Rd, Rs
            result = (self.registers[a] - self.registers[b]) & 0xFFFF
            self._log(f"SUB R{a} = {self.registers[a]} - R{b}({self.registers[b]}) = {result}")
            self.registers[a] = result

        elif opcode == 0x4:  # AND Rd, Rs
            self.registers[a] &= self.registers[b]
            self._log(f"AND R{a} &= R{b} -> {self.registers[a]}")

        elif opcode == 0x5:  # OR Rd, Rs
            self.registers[a] |= self.registers[b]
            self._log(f"OR R{a} |= R{b} -> {self.registers[a]}")

        elif opcode == 0x6:  # XOR Rd, Rs
            self.registers[a] ^= self.registers[b]
            self._log(f"XOR R{a} ^= R{b} -> {self.registers[a]}")

        elif opcode == 0x7:  # LI Rd, imm (Load Immediate)
            self.registers[a] = imm
            self._log(f"LI R{a} <- {imm}")

        elif opcode == 0x8:  # JMP addr
            self.pc = imm
            self._log(f"JMP -> {imm}")

        elif opcode == 0x9:  # JZ Rs, addr
            if self.registers[a] == 0:
                self.pc = imm
                self._log(f"JZ R{a}=0, jumping to {imm}")
            else:
                self._log(f"JZ R{a}={self.registers[a]}, not jumping")

        elif opcode == 0xA:  # JNZ Rs, addr
            if self.registers[a] != 0:
                self.pc = imm
                self._log(f"JNZ R{a}={self.registers[a]}, jumping to {imm}")
            else:
                self._log(f"JNZ R{a}=0, not jumping")

        elif opcode == 0xB:  # MOV Rd, Rs
            self.registers[a] = self.registers[b]
            self._log(f"MOV R{a} <- R{b} = {self.registers[a]}")

        elif opcode == 0xC:  # INC Rd
            self.registers[a] = (self.registers[a] + 1) & 0xFFFF
            self._log(f"INC R{a} -> {self.registers[a]}")

        elif opcode == 0xD:  # DEC Rd
            self.registers[a] = (self.registers[a] - 1) & 0xFFFF
            self._log(f"DEC R{a} -> {self.registers[a]}")

        elif opcode == 0xE:  # OUT Rd (print register value)
            print(f"OUTPUT: R{a} = {self.registers[a]}")
            self._log(f"OUT R{a} = {self.registers[a]}")

        elif opcode == 0xF:  # HLT
            self.halted = True
            self._log("HLT - CPU halted")
            return False

        self.cycle_count += 1
        return True

    def run(self, max_cycles: int = 10000) -> int:
        """Run until HLT or max_cycles. Returns cycle count."""
        while self.cycle_count < max_cycles and self.step():
            pass
        return self.cycle_count

    def dump_state(self):
        """Print CPU state for debugging"""
        print("=" * 50)
        print(f"PC: {self.pc}  Cycles: {self.cycle_count}  Halted: {self.halted}")
        print("Registers:")
        for i in range(8):
            print(f"  R{i} = {self.registers[i]:5d} (0x{self.registers[i]:04X})")
        print("=" * 50)

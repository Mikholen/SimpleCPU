"""
Simple assembler for SimpleCPU
Supports labels, comments, and basic pseudo-instructions
"""

class Assembler:
    OPCODES = {
        'LOAD': 0x0, 'STORE': 0x1, 'ADD': 0x2, 'SUB': 0x3,
        'AND': 0x4, 'OR': 0x5, 'XOR': 0x6, 'LI': 0x7,
        'JMP': 0x8, 'JZ': 0x9, 'JNZ': 0xA, 'MOV': 0xB,
        'INC': 0xC, 'DEC': 0xD, 'OUT': 0xE, 'HLT': 0xF
    }

    def __init__(self):
        self.labels = {}
        self.errors = []

    def _parse_register(self, token: str) -> int:
        """Parse register like R1, R2, etc."""
        token = token.upper().strip(',')
        if token.startswith('R') and token[1:].isdigit():
            reg = int(token[1:])
            if 0 <= reg <= 7:
                return reg
        raise ValueError(f"Invalid register: {token}")

    def _parse_value(self, token: str) -> int:
        """Parse immediate value or label"""
        token = token.strip(',')
        if token in self.labels:
            return self.labels[token]
        if token.startswith('0x'):
            return int(token, 16)
        return int(token)

    def _first_pass(self, lines: list[str]):
        """Collect labels"""
        self.labels = {}
        addr = 0
        for line in lines:
            line = line.split(';')[0].split('#')[0].strip()
            if not line:
                continue
            if ':' in line:
                label = line.split(':')[0].strip()
                self.labels[label] = addr
                line = line.split(':', 1)[1].strip()
                if not line:
                    continue
            addr += 1

    def _second_pass(self, lines: list[str]) -> list[int]:
        """Generate machine code"""
        code = []
        line_num = 0
        for line in lines:
            line_num += 1
            line = line.split(';')[0].split('#')[0].strip()
            if not line:
                continue
            if ':' in line:
                line = line.split(':', 1)[1].strip()
                if not line:
                    continue

            tokens = line.split()
            op = tokens[0].upper()

            if op not in self.OPCODES:
                self.errors.append(f"Line {line_num}: Unknown opcode '{op}'")
                continue

            opcode = self.OPCODES[op]
            reg_a, reg_b, imm = 0, 0, 0

            try:
                if op in ('LOAD', 'STORE'):
                    reg_a = self._parse_register(tokens[1])
                    imm = self._parse_value(tokens[2])
                elif op in ('ADD', 'SUB', 'AND', 'OR', 'XOR', 'MOV'):
                    reg_a = self._parse_register(tokens[1])
                    reg_b = self._parse_register(tokens[2])
                elif op == 'LI':
                    reg_a = self._parse_register(tokens[1])
                    imm = self._parse_value(tokens[2])
                elif op == 'JMP':
                    imm = self._parse_value(tokens[1])
                elif op in ('JZ', 'JNZ'):
                    reg_a = self._parse_register(tokens[1])
                    imm = self._parse_value(tokens[2])
                elif op in ('INC', 'DEC', 'OUT'):
                    reg_a = self._parse_register(tokens[1])
                elif op == 'HLT':
                    pass
            except (IndexError, ValueError) as e:
                self.errors.append(f"Line {line_num}: {e}")
                continue

            instr = (opcode << 12) | (reg_a << 8) | (reg_b << 4) | (imm & 0xFF)
            code.append(instr)

        return code

    def assemble(self, source: str) -> list[int]:
        """Assemble source code into binary"""
        self.errors = []
        lines = source.strip().split('\n')
        self._first_pass(lines)
        code = self._second_pass(lines)

        if self.errors:
            print("Assembly errors:")
            for err in self.errors:
                print(f"  {err}")

        return code

    def assemble_file(self, filename: str) -> list[int]:
        """Assemble from file"""
        with open(filename, 'r') as f:
            return self.assemble(f.read())

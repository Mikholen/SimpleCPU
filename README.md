# SimpleCPU Simulator

A 16-bit processor simulator (Python).

## Architecture

- **Registers**: 8 general-purpose (R0-R7), R0 hardwired to 0
- **Memory**: 64KB (65536 x 16-bit words)
- **Instructions**: 16-bit fixed width

## Instruction Set

| Opcode | Mnemonic | Format | Description |
|--------|----------|--------|-------------|
| 0x0 | LOAD | Rd, addr | Load from memory |
| 0x1 | STORE | Rs, addr | Store to memory |
| 0x2 | ADD | Rd, Rs | Rd = Rd + Rs |
| 0x3 | SUB | Rd, Rs | Rd = Rd - Rs |
| 0x4 | AND | Rd, Rs | Rd = Rd & Rs |
| 0x5 | OR | Rd, Rs | Rd = Rd | Rs |
| 0x6 | XOR | Rd, Rs | Rd = Rd ^ Rs |
| 0x7 | LI | Rd, imm | Load immediate |
| 0x8 | JMP | addr | Unconditional jump |
| 0x9 | JZ | Rs, addr | Jump if zero |
| 0xA | JNZ | Rs, addr | Jump if not zero |
| 0xB | MOV | Rd, Rs | Copy register |
| 0xC | INC | Rd | Increment |
| 0xD | DEC | Rd | Decrement |
| 0xE | OUT | Rs | Output register |
| 0xF | HLT | - | Halt CPU |

## Usage

```bash
# Run interactive demo
python main.py

# Run unit tests
python test_cpu.py
```

## Project Structure

```
simplecpu/
├── cpu.py          # CPU core implementation
├── assembler.py    # Assembler (source -> binary)
├── programs.py     # Example programs
├── main.py         # Main entry point
├── test_cpu.py     # Unit tests
└── README.md       # Documentation
```

## Example Program

```asm
; Calculate factorial of 5
        LI R1, 5        ; n = 5
        LI R2, 1        ; result = 1
loop:
        JZ R1, done     ; if n == 0, done
        MOV R3, R2
        ; multiply R2 by R1 (simplified)
        ADD R2, R3
        DEC R1
        JMP loop
done:
        OUT R2
        HLT
```
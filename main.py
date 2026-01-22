"""
SimpleCPU Simulator - Main entry point
Demonstrates processor simulation with multiple test programs
"""

import time
from cpu import SimpleCPU
from assembler import Assembler
from programs import ALL_PROGRAMS

def run_demo(name: str, title: str, source: str, verbose: bool = False, delay: float = 0.1):
    """Run a single demo program with visual output"""
    print("\n" + "=" * 60)
    print(f"Demo: {title}")
    print("=" * 60)
    print(f"\nSource code:\n{source}")
    print("-" * 40)
    print("Execution output:")
    print("-" * 40)

    asm = Assembler()
    binary = asm.assemble(source)

    if asm.errors:
        print("Assembly failed!")
        return

    cpu = SimpleCPU(verbose=verbose)
    cpu.load_program(binary)

    # Run with step-by-step delay for demonstration
    while not cpu.halted and cpu.cycle_count < 1000:
        cpu.step()
        time.sleep(delay)

    print("-" * 40)
    cpu.dump_state()

def interactive_mode():
    """Interactive mode for custom programs"""
    print("\nInteractive mode - enter assembly code (empty line to finish):")
    lines = []
    while True:
        line = input("> ")
        if not line:
            break
        lines.append(line)

    if not lines:
        return

    source = "\n".join(lines)
    asm = Assembler()
    binary = asm.assemble(source)

    if asm.errors:
        return

    cpu = SimpleCPU(verbose=True)
    cpu.load_program(binary)
    cpu.run()
    cpu.dump_state()

def main():
    print("=" * 60)
    print("SimpleCPU Simulator v1.0")
    print("16-bit processor with 8 registers and 16 instructions")
    print("=" * 60)

    print("\nAvailable demos:")
    for key, (title, _) in ALL_PROGRAMS.items():
        print(f"  {key:12} - {title}")
    print("  all          - Run all demos")
    print("  interactive  - Enter custom assembly")

    choice = input("\nSelect demo (or 'all'): ").strip().lower()

    if choice == 'all':
        for name, (title, source) in ALL_PROGRAMS.items():
            run_demo(name, title, source, delay=0.05)
            input("\nPress Enter for next demo...")
    elif choice == 'interactive':
        interactive_mode()
    elif choice in ALL_PROGRAMS:
        title, source = ALL_PROGRAMS[choice]
        run_demo(choice, title, source, verbose=True, delay=0.1)
    else:
        print("Running default demo: Fibonacci")
        title, source = ALL_PROGRAMS['fibonacci']
        run_demo('fibonacci', title, source, delay=0.1)

if __name__ == '__main__':
    main()

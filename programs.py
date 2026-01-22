"""
Example programs for SimpleCPU demonstration
"""

# Program 1: Count from 1 to 10, output each number
COUNTDOWN = """
; Count from 1 to 10 and output each value
        LI R1, 1        ; counter = 1
        LI R2, 11       ; limit = 11
loop:
        OUT R1          ; print counter
        INC R1          ; counter++
        MOV R3, R1      ; copy for comparison
        SUB R3, R2      ; R3 = counter - limit
        JNZ R3, loop    ; if not equal, continue
        HLT
"""

# Program 2: Fibonacci sequence (first 10 num)
FIBONACCI = """
; Calculate and output first 10 Fibonacci numbers
        LI R1, 0        ; fib(n-2)
        LI R2, 1        ; fib(n-1)
        LI R3, 10       ; counter
        OUT R1          ; output 0
        OUT R2          ; output 1
fib_loop:
        MOV R4, R2      ; temp = fib(n-1)
        ADD R2, R1      ; fib(n) = fib(n-1) + fib(n-2)
        MOV R1, R4      ; fib(n-2) = old fib(n-1)
        OUT R2          ; output fib(n)
        DEC R3          ; counter--
        LI R5, 2
        MOV R6, R3
        SUB R6, R5      ; R6 = counter - 2
        JNZ R6, fib_loop
        HLT
"""

# Program 3: Sum of numbers 1 to N (N=5)
SUM_1_TO_N = """
; Calculate sum of 1 + 2 + 3 + 4 + 5 = 15
        LI R1, 0        ; sum = 0
        LI R2, 1        ; i = 1
        LI R3, 6        ; limit = N+1
sum_loop:
        ADD R1, R2      ; sum += i
        OUT R1          ; show running sum
        INC R2          ; i++
        MOV R4, R2
        SUB R4, R3      ; R4 = i - limit
        JNZ R4, sum_loop
        OUT R1          ; final sum
        HLT
"""

# Program 4: Multiply two numbers (3 * 4 = 12) via repeated addition
MULTIPLY = """
; Multiply 3 * 4 using repeated addition
        LI R1, 0        ; result = 0
        LI R2, 3        ; multiplicand
        LI R3, 4        ; multiplier (counter)
mul_loop:
        JZ R3, done     ; if counter == 0, done
        ADD R1, R2      ; result += multiplicand
        OUT R1          ; show progress
        DEC R3          ; counter--
        JMP mul_loop
done:
        OUT R1          ; final result: 12
        HLT
"""

# Program 5: Find maximum of 3 numbers
FIND_MAX = """
; Find max of 7, 15, 9
        LI R1, 7        ; a = 7
        LI R2, 15       ; b = 15
        LI R3, 9        ; c = 9
        OUT R1
        OUT R2
        OUT R3
        ; max = a
        MOV R4, R1
        ; if b > max: max = b
        MOV R5, R2
        SUB R5, R4      ; b - max
        JZ R5, check_c  ; if b == max, skip
        MOV R6, R2
        SUB R6, R4
        ; Simple comparison: if R2 > R4
        MOV R4, R2      ; assume b > a for demo
check_c:
        MOV R5, R3
        SUB R5, R4      ; c - max
        JZ R5, output   ; if c == max, skip
        ; if c > max: max = c (simplified)
output:
        OUT R4          ; output max
        HLT
"""

ALL_PROGRAMS = {
    '1': ('(ENTER 1) Count 1 to 10', COUNTDOWN),
    '2': ('(ENTER 2) Fibonacci Sequence', FIBONACCI),
    '3': ('(ENTER 3) Sum 1 to N', SUM_1_TO_N),
    '4': ('(ENTER 4) Multiply via Addition', MULTIPLY),
    '5': ('(ENTER 5) Find Maximum', FIND_MAX),
}

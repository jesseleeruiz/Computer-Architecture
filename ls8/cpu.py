"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
ADD = 0b10100000
SUB = 0b10100001
POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self, ram = [0] * 256, reg = [0] * 8, pc = 0, running = True, op_size = 1):
        """Construct a new CPU."""
        self.ram = ram
        self.reg = reg
        self.pc = pc
        self.running = running
        self.op_size = op_size
        self.sp = 7
        self.fl = 0b00000000

    def ram_read(self, address_to_read):
        return self.ram[address_to_read]
        # Memory Address Register
    
    def ram_write(self, value_to_write, address_to_write_to):
        return address_to_write_to[value_to_write]
        # Memory Data Register

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    n = comment_split[0].strip()

                    if n == '':
                        continue

                    val = int(n, 2)
                    self.ram[address] = val

                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found.")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        elif op == SUB:
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == CMP:
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100
            else:
                self.fl = 0b00000000
                
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            flag = self.fl

            if IR == HLT:
                self.running = False

            elif IR == LDI:
                self.reg[operand_a] = operand_b
                self.op_size = 3

            elif IR == PRN:
                num_at_reg = self.reg[operand_a]
                print(num_at_reg)
                self.op_size = 2

            elif IR == MUL:
                self.alu(IR, operand_a, operand_b)
                self.op_size = 3

            elif IR == ADD:
                self.alu(IR, operand_a, operand_b)
                self.op_size = 3

            elif IR == SUB:
                self.alu(IR, operand_a, operand_b)
                self.op_size = 3

            elif IR == POP:
                val = self.ram[self.reg[self.sp]]
                self.reg[operand_a] = val
                self.reg[self.sp] += 1
                self.op_size = 2

            elif IR == PUSH:
                val = self.reg[operand_a]
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = val
                self.op_size = 2

            elif IR == CALL:
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = self.pc + 2

                self.pc = self.reg[operand_a]

                self.op_size = 0

            elif IR == RET:
                self.pc = self.ram[self.reg[self.sp]]
                self.reg[self.sp] += 1

                self.op_size = 0

            elif IR == CMP:
                self.alu(IR, operand_a, operand_b)
                self.op_size = 3

            elif IR == JMP:
                self.pc = self.reg[operand_a]
                self.op_size = 0

            elif IR == JEQ:
                if flag == 0b00000001:
                    self.pc = self.reg[operand_a]
                    self.op_size = 0
                else:
                    self.op_size = 2

            elif IR == JNE:
                if flag == 0b00000100:
                    self.pc = self.reg[operand_a]
                    self.op_size = 0
                else:
                    self.op_size = 2

            else:
                print(f"Invalid Instructions: {IR}")
                self.running = False

            self.pc += self.op_size


"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111

class CPU:
    """Main CPU class."""

    def __init__(self, ram = [0] * 256, reg = [0] * 8, pc = 0, running = True, op_size = 1):
        """Construct a new CPU."""
        self.ram = ram
        self.reg = reg
        self.pc = pc
        self.running = running
        self.op_size = op_size

    def ram_read(self, address_to_read):
        return self.ram[address_to_read]
        # Memory Address Register
    
    def ram_write(self, value_to_write, address_to_write_to):
        return address_to_write_to[value_to_write]
        # Memory Data Register

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
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

            if IR == HLT:
                self.running = False
            elif IR == LDI:
                self.reg[operand_a] = operand_b
                self.op_size = 3
            elif IR == PRN:
                num_at_reg = self.reg[operand_a]
                print(num_at_reg)
                self.op_size = 2

            self.pc += self.op_size


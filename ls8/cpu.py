"""CPU functionality."""

import sys

HLT = 0b00000001    # HLT
LDI = 0b10000010    # LDI
PRN = 0b01000111    # PRN
MUL = 0b10100010    # MUL
ADD = 0b10100000    # ADD
SUB = 0b10100001    # SUB

class CPU:
    """Main CPU class."""

    def __init__(self, ram = [0] * 256, reg = [0] * 8, pc = 0, running = True, op_size = 1):
        """Construct a new CPU."""
        self.ram = ram
        self.reg = reg
        self.pc = pc
        self.running = running
        self.op_size = op_size
        self.branchtable = {}
        # self.branchtable[OP1] = self.handle_op1
        # self.branchtable[OP2] = self.handle_op2
        # self.branchtable[OP3] = self.handle_op3
        # self.branchtable[OP4] = self.handle_op4
        # self.branchtable[OP5] = self.handle_op5
        # self.branchtable[OP6] = self.handle_op6

    def handle_op1(self):
        self.running = False

    def handle_op2(self, a):
        pass

    def handle_op3(self, a):
        pass

    def handle_op4(self, a):
        pass

    def handle_op5(self, a):
        pass

    def handle_op6(self, a):
        pass

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



            # For now, we've just hardcoded a program:
            # program = [
            #     # From print8.ls8
            #     0b10000010, # LDI R0,8
            #     0b00000000,
            #     0b00001000,
            #     0b01000111, # PRN R0
            #     0b00000000,
            #     0b00000001, # HLT
            # ]

            # for instruction in program:
            #     self.ram[address] = instruction
            #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        elif op == SUB:
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
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
            elif IR == MUL:
                self.alu(IR, operand_a, operand_b)
                self.op_size = 3
            elif IR == ADD:
                self.alu(IR, operand_a, operand_b)
                self.op_size = 3
            elif IR == SUB:
                self.alu(IR, operand_a, operand_b)
                self.op_size = 3

            self.pc += self.op_size


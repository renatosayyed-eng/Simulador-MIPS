class Registers:
    def __init__(self):
        self.regs = [0]*32
    
    def read(self, registrador):
        return self.regs[registrador]
    
    def write(self, registrador, value):
        self.regs[registrador] = value

    def report(self):
        print("$zero >> {", self.regs[0], end = " }\n")
        print("$at >> {", self.regs[1], end = " }\n")
        print("$v0 >> {", self.regs[2], end = " } | ")
        print("$v1 >> {", self.regs[3], end = " }\n")
        print("$a0 >> {", self.regs[4], end = " } | ")
        print("$a1 >> {", self.regs[5], end = " } | ")
        print("$a2 >> {", self.regs[6], end = " } | ")
        print("$a3 >> {", self.regs[7], end = " }\n")
        print("$t0 >> {", self.regs[8], end = " } | ")
        print("$t1 >> {", self.regs[9], end = " } | ")
        print("$t2 >> {", self.regs[10], end = " } | ")
        print("$t3 >> {", self.regs[11], end = " } | ")
        print("$t4 >> {", self.regs[12], end = " }\n")
        print("$t5 >> {", self.regs[13], end = " } | ")
        print("$t6 >> {", self.regs[14], end = " } | ")
        print("$t7 >> {", self.regs[15], end = " } | ")
        print("$t8 >> {", self.regs[24], end = " } | ")
        print("$t9 >> {", self.regs[25], end = " }\n")
        print("$s0 >> {", self.regs[16], end = " } | ")
        print("$s1 >> {", self.regs[17], end = " } | ")
        print("$s2 >> {", self.regs[18], end = " } | ")
        print("$s3 >> {", self.regs[19], end = " }\n")
        print("$s4 >> {", self.regs[20], end = " } | ")
        print("$s5 >> {", self.regs[21], end = " } | ")
        print("$s6 >> {", self.regs[22], end = " } | ")
        print("$s7 >> {", self.regs[23], end = " }\n")
        print("$k0 >> {", self.regs[26], end = " } | ")
        print("$k1 >> {", self.regs[27], end = " }\n")
        print("$gp >> {", self.regs[28], end = " }\n")
        print("$sp >> {", self.regs[29], end = " }\n")
        print("$fp >> {", self.regs[30], end = " }\n")
        print("$ra >> {", self.regs[31], end = " }\n")
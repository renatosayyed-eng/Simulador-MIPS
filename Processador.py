import Manipulacoes as MPS
import Registradores as REGS
import StaticRAM as SRAM

class Processor:
    def __init__(self, c_cap, vias, pal, unity, d_cap, instructions):
        self.registradores = REGS.Registers()
        self.cache = SRAM.SRAM(c_cap, vias, pal, unity, d_cap, instructions)
        self.ciclos = 0
        self.pc = 0
        self.n_instrucoes = self.cache.dram.ammount_instrucoes
        self.cache_hit = 0
        self.cache_miss = 0
        self.access_cache = 0
        self.exec_instrucoes = 0
        self.fail_instrucoes = 0
        self.total_instrucoes = 0

    def load_instruction(self):
        print("Foi realizado o load de uma instrução da DRAM >> + 50 ciclos")
        value = self.cache.dram.read(self.pc+self.cache.rep_max+1)
        self.ciclos += 50
        self.instruction(value)

    def instruction(self, instrucao):
        self.total_instrucoes += 1
        self.increase_pc()
        binary = MPS.dec_to_bin(instrucao)
        op = MPS.bin_to_dec(MPS.fix_str(binary[:6]))
        # TIPO I
        if op == 35 or op == 43 or op == 4:
            rs = MPS.bin_to_dec(MPS.fix_str(binary[6:11]))
            rt = MPS.bin_to_dec(MPS.fix_str(binary[11:16]))
            address = MPS.bin_to_dec(MPS.fix_str(binary[16:]))
            if op == 35: #LW
                if rt == 0:
                    print("O registrador $zero não pode ser usado para armazenar valores")
                    self.fail_instrucoes += 1
                elif rt == 31:
                    print("O registrador $ra não pode ser usado para armazenar valores fora da instrucao JAL")
                    self.fail_instrucoes += 1
                else:
                    self.access_cache += 1
                    address += self.registradores.read(rs)
                    value = self.cache.read(address, 0)
                    if value[0] == "ERRO":
                        self.fail_instrucoes += 1
                        self.ciclos += value[1]
                    else:
                        if value[1] != 1:
                            self.cache_miss += 1
                            print("Ocorreu um cache miss >> + 51 ciclos")
                        else:
                            self.cache_hit += 1
                            print("Ocorreu um cache hit >> + 1 ciclo")
                        self.ciclos += value[1]
                        self.registradores.write(rt, value[0])
                        self.exec_instrucoes += 1
            elif op == 43: #SW
                self.access_cache += 1
                address += self.registradores.read(rs)
                value = self.registradores.read(rt)
                answer = self.cache.write_on(address, value, 0)
                if type(answer) == list:
                    self.fail_instrucoes += 1
                else:
                    old = self.ciclos
                    self.ciclos += answer
                    old = self.ciclos - old
                    if old != 1:
                        self.cache_miss += 1
                        print("Ocorreu um cache miss >> + 51 ciclos")
                    else:
                        self.cache_hit += 1
                        print("Ocorreu um cache hit >> + 1 ciclo")
                    self.exec_instrucoes += 1
            else: #BEQ
                self.ciclos += 1
                if address < 0 or address > (self.n_instrucoes-1):
                    print("O endereço indicado para realizar o desvio está fora dos limites disponíveis")
                    self.fail_instrucoes += 1
                else:
                    if self.registradores.read(rs) == self.registradores.read(rt):
                        self.pc = address
                    print("A instrucão BEQ (Branch if Equal) é realizada diretamente nos registradores, assim, há acréscimo de 1 nos ciclos")
                    self.exec_instrucoes += 1
        # TIPO J
        elif op == 2 or op == 3:
            self.ciclos += 1
            address = MPS.bin_to_dec(MPS.fix_str(binary[6:]))
            if address < 0 or address > (self.n_instrucoes-1):
                print("O endereço indicado para realizar o jump está fora dos limites disponíveis")
                self.fail_instrucoes += 1
            else:
                if op == 2: #J
                    self.pc = address
                    print("A instrução J(Jump) é realizada diretamente nos registradores, assim, há acréscimo de 1 nos ciclos")
                    self.exec_instrucoes += 1
                else: #JAL
                    self.registradores.write(31, self.pc)
                    self.pc = address
                    print("A instrução JAL(Jump and Link) é realizada diretamente nos registradores, assim, há acréscimo de 1 nos ciclos")
                    self.exec_instrucoes += 1
        # TIPO R        
        elif op == 0:
            self.ciclos += 1
            rs = MPS.bin_to_dec(MPS.fix_str(binary[6:11]))
            rt = MPS.bin_to_dec(MPS.fix_str(binary[11:16]))
            rd = MPS.bin_to_dec(MPS.fix_str(binary[16:21]))
            shamt = MPS.bin_to_dec(MPS.fix_str(binary[21:26]))
            funct = MPS.bin_to_dec(MPS.fix_str(binary[26:]))
            if funct == 0: #SLL
                if rd == 0:
                    print("O registrador $zero não pode ser usado para armazenar valores")
                    self.fail_instrucoes += 1
                elif rd == 31:
                    print("O registrador $ra não pode ser usado para armazenar valores fora da instrucao JAL")
                    self.fail_instrucoes += 1
                else:
                    value = self.registradores.read(rs) << shamt
                    self.registradores.write(rd, value)
                    print("A instrução SLL(Shift Left) é realizada diretamente nos registradores, assim, há acréscimo de 1 nos ciclos")
                    self.exec_instrucoes += 1
            elif funct == 2: #SRL
                if rd == 0:
                    print("O registrador $zero não pode ser usado para armazenar valores")
                    self.fail_instrucoes += 1
                elif rd == 31:
                    print("O registrador $ra não pode ser usado para armazenar valores fora da instrucao JAL")
                    self.fail_instrucoes += 1
                else:
                    value = self.registradores.read(rs) >> shamt
                    self.registradores.write(rd, value)
                    print("A instrução SRL(Shift Right) é realizada diretamente nos registradores, assim, há acréscimo de 1 nos ciclos")
                    self.exec_instrucoes += 1
            elif funct == 8: #JR
                    if rs != 31:
                        print("O registrador $ra não foi informado no campo rs >> | OP | RS | RT | RD | SHAMT | FUNCT |\nA instrução JR não será executada")
                        self.fail_instrucoes += 1
                    else:
                        value = self.registradores.read(rs)
                        if value < 0 or value > (self.n_instrucoes-1):
                            print("O endereço indicado para realizar o jump está fora dos limites disponíveis")
                            self.fail_instrucoes += 1
                        else:
                            self.pc = value
                            print("A instrução JR(Jump Register) é realizada diretamente nos registradores, assim, há acréscimo de 1 nos ciclos")
                            self.exec_instrucoes += 1
            elif funct == 32: #ADD
                if rd == 0:
                    print("O registrador $zero não pode ser usado para armazenar valores")
                    self.fail_instrucoes += 1
                elif rd == 31:
                    print("O registrador $ra não pode ser usado para armazenar valores fora da instrucao JAL")
                    self.fail_instrucoes += 1
                else:
                    value = self.registradores.read(rs) + self.registradores.read(rt)
                    self.registradores.write(rd, value)
                    print("A instrução ADD é realizada diretamente nos registradores, assim, há acréscimo de 1 nos ciclos")
                    self.exec_instrucoes += 1
            elif funct == 34: #SUB
                if rd == 0:
                    print("O registrador $zero não pode ser usado para armazenar valores")
                    self.fail_instrucoes += 1
                elif rd == 31:
                    print("O registrador $ra não pode ser usado para armazenar valores fora da instrucao JAL")
                    self.fail_instrucoes += 1
                else:
                    value = self.registradores.read(rs) - self.registradores.read(rt)
                    self.registradores.write(rd, value)
                    print("A instrução SUB é realizada diretamente nos registradores, assim, há acréscimo de 1 nos ciclos")
                    self.exec_instrucoes += 1
            elif funct == 36: #AND
                if rd == 0:
                    print("O registrador $zero não pode ser usado para armazenar valores")
                    self.fail_instrucoes += 1
                elif rd == 31:
                    print("O registrador $ra não pode ser usado para armazenar valores fora da instrucao JAL")
                    self.fail_instrucoes += 1
                else:
                    op1 = MPS.dec_to_bin(self.registradores.read(rs))
                    op2 = MPS.dec_to_bin(self.registradores.read(rt))
                    value = []
                    for i in range(0,32):
                        if op1[i] == "1" and op2[i] == "1":
                            value.append(1)
                        else:
                            value.append(0)
                    value = MPS.fix_str(value)
                    value = int(value,2)
                    self.registradores.write(rd, value)
                    print("A instrução AND é realizada diretamente nos registradores, assim, há acréscimo de 1 nos ciclos")
                    self.exec_instrucoes += 1
            elif funct == 37: #OR
                if rd == 0:
                    print("O registrador $zero não pode ser usado para armazenar valores")
                    self.fail_instrucoes += 1
                elif rd == 31:
                    print("O registrador $ra não pode ser usado para armazenar valores fora da instrucao JAL")
                    self.fail_instrucoes += 1
                else:
                    op1 = MPS.dec_to_bin(self.registradores.read(rs))
                    op2 = MPS.dec_to_bin(self.registradores.read(rt))
                    value = []
                    for i in range(0,32):
                        if op1[i] == "1" or op2[i] == "1":
                            value.append(1)
                        else:
                            value.append(0)
                    value = MPS.fix_str(value)
                    value = int(value,2)
                    self.registradores.write(rd, value)
                    print("A instrução OR é realizada diretamente nos registradores, assim, há acréscimo de 1 nos ciclos")
                    self.exec_instrucoes += 1
            elif funct == 39: #NOR
                if rd == 0:
                    print("O registrador $zero não pode ser usado para armazenar valores")
                    self.fail_instrucoes += 1
                elif rd == 31:
                    print("O registrador $ra não pode ser usado para armazenar valores fora da instrucao JAL")
                    self.fail_instrucoes += 1
                else:
                    op1 = MPS.dec_to_bin(self.registradores.read(rs))
                    op2 = MPS.dec_to_bin(self.registradores.read(rt))
                    value = []
                    for i in range(0,32):
                        if op1[i] == "1" or op2[i] == "1":
                            value.append(0)
                        else:
                            value.append(1)
                    value = MPS.fix_str(value)
                    value = int(value,2)
                    self.registradores.write(rd, value)
                    print("A instrução NOR é realizada diretamente nos registradores, assim, há acréscimo de 1 nos ciclos")
                    self.exec_instrucoes += 1
            elif funct == 42: #SLT
                if rd == 0:
                    print("O registrador $zero não pode ser usado para armazenar valores")
                    self.fail_instrucoes += 1
                elif rd == 31:
                    print("O registrador $ra não pode ser usado para armazenar valores fora da instrucao JAL")
                    self.fail_instrucoes += 1
                else:
                    op1 = self.registradores.read(rs)
                    op2 = self.registradores.read(rt)
                    value = 5
                    if op1 < op2:
                        value = 1
                    else:
                        value = 0
                    self.registradores.write(rd, value)
                    print("A instrução SLT é realizada diretamente nos registradores, assim, há acréscimo de 1 nos ciclos")
                    self.exec_instrucoes += 1
            else:
                print("Nenhuma instrução válida foi identificada -- funct >> ", funct)
                self.fail_instrucoes += 1
                self.ciclos += 1
            
        else:
            print("Nenhuma instrução válida foi identificada -- op >> ", op)
            self.fail_instrucoes += 1
            self.ciclos += 1

    def increase_pc(self):
        if self.pc + 1 <= self.n_instrucoes:
            self.pc += 1
        else:
            self.pc = 0

    def report(self):
        falha = self.cache_miss/self.access_cache
        acerto = self.cache_hit/self.access_cache
        exec = self.exec_instrucoes/self.total_instrucoes
        fail = self.fail_instrucoes/self.total_instrucoes
        print("INSTRUÇÕES")
        print("Ao todo foram realizadas " + str(self.total_instrucoes) + " intruções, onde:")
        print(str(exec*100) + "% ou " + str(self.exec_instrucoes) + " foram executadas corretamente")
        print(str(fail*100) + "% ou " + str(self.fail_instrucoes) + " não puderam ser executadas corretamente\n")
        print("ACESSO A CACHE")
        print("Ao todo foram realizados " + str(self.access_cache) + " acessos a cache, onde:")
        print(str(acerto*100) + "% ou " + str(self.cache_hit) + " foram cache hit")
        print(str(falha*100) + "% ou " + str(self.cache_miss) + " foram cache miss\n")
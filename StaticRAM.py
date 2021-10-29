import Manipulacoes as MPS
import math
import DynamicRAM as DRAM

class SRAM:
    def calc_num_conjuntos(self, capacidade, vias, palavras_bloco):
        capacidade *= 1024
        conjuntos = capacidade / (vias*palavras_bloco*4)
        if (conjuntos % 1) != 0:
            return math.ceil(conjuntos)
        else:
            return int(conjuntos)
    
    def calc_indice(self, n_conjuntos):
        return int(math.log(n_conjuntos,2))

    def calc_word_offset(self, palavras_bloco):
        return int(math.log(palavras_bloco,2))

    def calc_byte_offset(self):
        return int(math.log(4,2))
    
    def calc_tag(self, indice, word, byte):
        return (32 - indice - word - byte)

    def __init__(self, capacidade, vias, palavras_bloco, unidade, dram_capacidade, instrucoes):
        self.dram = DRAM.DRAM(unidade, dram_capacidade, palavras_bloco, instrucoes)
        self.rep_max = len(self.dram.palavras)-(self.dram.ammount_instrucoes + 1)
        self.n_conjuntos = self.calc_num_conjuntos(capacidade, vias, palavras_bloco)
        self.n_indice = self.calc_indice(self.n_conjuntos)
        self.n_word = self.calc_word_offset(palavras_bloco)
        self.n_byte = self.calc_byte_offset()
        self.n_tag = self.calc_tag(self.n_indice, self.n_word, self.n_byte)
        self.conjuntos = []
        for i in range (0, self.n_conjuntos):
            bloco = []
            for x in range(0, vias):
                palavras = []
                for y in range(0, palavras_bloco):
                    palavras.append(0)
                bloco.append([i,x,False,False,False,0,palavras])
            self.conjuntos.append(bloco)
        self.lru = []
        for i in range (0, self.n_conjuntos):
            bloco = []
            for j in range(0,vias):
                bloco.append(0)
            self.lru.append(bloco)

    def read(self, endereco, ciclos):
        address = MPS.dec_to_bin(endereco)
        tag = MPS.bin_to_dec(MPS.fix_str(address[:self.n_tag]))
        indice = MPS.bin_to_dec(MPS.fix_str(address[self.n_tag:(self.n_tag + self.n_indice)]))
        if indice > len(self.conjuntos)-1:
            print("O indice do bloco de cache indicado esta fora dos limites disponíveis")
            return ["ERRO",1]
        else:
            if self.n_word == 0:
                word = 0
            else:
                word = MPS.bin_to_dec(MPS.fix_str(address[(self.n_tag + self.n_indice):(self.n_tag + self.n_indice + self.n_word)]))
            byte = MPS.bin_to_dec(MPS.fix_str(address[(self.n_tag + self.n_indice + self.n_word):]))
            for i in range(0, len(self.conjuntos[indice])):
                if self.conjuntos[indice][i][2] == True:
                    if self.conjuntos[indice][i][5] == tag:
                        self.conjuntos[indice][i][4] = True
                        self.lru[indice][i] = 1
                        binary = MPS.dec_to_bin(self.conjuntos[indice][i][6][word])
                        ciclos += 1
                        return [MPS.bin_to_dec(MPS.fix_str(binary[32-((byte*8)+8):32-(byte*8)])), ciclos]
            bloco_dram = MPS.bin_to_dec(MPS.fix_str(address[:32-(self.n_word+self.n_byte)]))
            if bloco_dram < 0 or bloco_dram > self.rep_max:
                print("O bloco de memória indicado está fora dos limites disponíveis")
                return ["ERRO",1]
            else:
                ciclos += self.write(bloco_dram, tag, indice)
                return self.read(endereco,ciclos)
    
    def write(self, endereco, tag, indice):
        bloco = self.dram.read(endereco)
        control = 0
        for i in range(0, len(self.conjuntos[indice])):
            if self.conjuntos[indice][i][2] == False:
                self.conjuntos[indice][i][2] = True
                self.conjuntos[indice][i][5] = tag
                for j in range(0, len(self.conjuntos[indice][i][6])):
                    self.conjuntos[indice][i][6][j] = bloco[j]
                self.lru[indice][i] = 0
                control = 1
                break
        if control == 0:
            count = sum(self.lru[indice])
            if count == len(self.lru[indice]):
                for i in range(0, len(self.lru[indice])):
                    self.lru[indice][i] = 0
            pos = []
            for i in range(0, len(self.lru[indice])):
                if self.lru[indice][i] == 0:
                    pos.append(i)
            pos = pos[0]
            if self.conjuntos[indice][pos][3] == True:
                parte1_ram = MPS.tag_to_bin(self.conjuntos[indice][pos][5])
                parte2_ram = MPS.fix_str(MPS.indice_ext_bin(indice, self.n_indice))
                bloco_ram = parte1_ram + parte2_ram
                bloco_ram = MPS.bin_to_dec(bloco_ram)
                value_escrita = []
                for j in range(0, len(self.conjuntos[indice][pos][6])):
                    value_escrita.append(self.conjuntos[indice][pos][6][j])
                self.dram.write(bloco_ram, value_escrita)
            self.conjuntos[indice][pos][2] = True
            self.conjuntos[indice][pos][3] = False
            self.conjuntos[indice][pos][4] = False
            self.conjuntos[indice][pos][5] = tag
            for j in range(0, len(self.conjuntos[indice][pos][6])):
                    self.conjuntos[indice][pos][6][j] = bloco[j]
            self.lru[indice][pos] = 0
        return int(50)

    def write_on(self, endereco, value, ciclos):
        address = MPS.dec_to_bin(endereco)
        tag = MPS.bin_to_dec(MPS.fix_str(address[:self.n_tag]))
        indice = MPS.bin_to_dec(MPS.fix_str(address[self.n_tag:(self.n_tag + self.n_indice)]))
        if indice > len(self.conjuntos)-1:
            print("O indice do bloco de cache indicado esta fora dos limites disponíveis")
            return ["ERRO",1]
        else:
            if self.n_word == 0:
                word = 0
            else:
                word = MPS.bin_to_dec(MPS.fix_str(address[(self.n_tag + self.n_indice):(self.n_tag + self.n_indice + self.n_word)]))
            for i in range(0, len(self.conjuntos[indice])):
                if self.conjuntos[indice][i][2] == True:
                    if self.conjuntos[indice][i][5] == tag:
                        self.conjuntos[indice][i][3] = True
                        self.conjuntos[indice][i][4] = True
                        self.lru[indice][i] = 1
                        self.conjuntos[indice][i][6][word] = value
                        ciclos += 1
                        return ciclos
            bloco_dram = MPS.bin_to_dec(MPS.fix_str(address[:32-(self.n_word+self.n_byte)]))
            if bloco_dram < 0 or bloco_dram > self.rep_max:
                print("O bloco de memória indicado está fora dos limites disponíveis")
                return ["ERRO",1]
            else:
                ciclos += self.write(bloco_dram, tag, indice)
                return self.write_on(endereco, value, ciclos)
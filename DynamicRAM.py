import random

class DRAM:
    def __init__(self, unidade, capacidade, palavras_bloco, instrucoes):
        self.ammount_instrucoes = 0
        self.palavras = []
        for i in range(0,int((((1024**unidade)*capacidade)/4)/palavras_bloco)):
            bloco = []
            for j in range(0, palavras_bloco):
                bloco.append(random.randint(0,4294967295))
            self.palavras.append(bloco)
        for i in instrucoes:
            self.ammount_instrucoes += 1
            self.palavras.append(i)
    
    def read(self, bloco):
        return self.palavras[bloco]

    def write(self, bloco_escrita, bloco_valores):
        for i in range(0, len(self.palavras[bloco_escrita])):
            self.palavras[bloco_escrita][i] = bloco_valores[i]
# Converte um valor binario em string para um int decimal
def bin_to_dec(value):
    return int(value, 2)

# Converte um int decimal para um valor binario em string 
def dec_to_bin(value):
    temp = bin(value)
    temp = temp[2:]
    filler = [0]*(32-len(temp))
    for i in temp:
        filler.append(i)
    return filler

# Coverte um vetor em uma string
def fix_str(value):
    aux = ""
    for i in value:
        aux += str(i)
    return aux

def indice_ext_bin(value, n_bits):
    temp = bin(value)
    temp = temp[2:]
    filler = [0]*(n_bits-len(temp))
    for i in temp:
        filler.append(i)
    return filler

def tag_to_bin(value):
    temp = bin(value)
    temp = temp[2:]
    return temp
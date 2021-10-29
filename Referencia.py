# 0 >> $0
# 1 >> $at
# 2 >> $v0 - 3 >> $v1
# 4 >> $a0 - 5 >> $a1 - 6 >> $a2 - 7 >> $a3
# 8 >> $t0 - 9 >> $t1 - 10 >> $t2 - 11 >> $t3
# 12 >> $t4 - 13 >> $t5 - 14 >> $t6 - 15 >> $t7
# 24 >> $t8 - 25 >> $t9
# 16 >> $s0 - 17 >> $s1 - 18 >> $s2 - 19 >> $s3
# 20 >> $s4 - 21 >> $s5 - 22 >> $s6 - 23 >> $s7 
# 26 >> $k0 - 27 >> $k1
# 28 >> $gp
# 29 >> $sp
# 30 >> $fp
# 31 >> $ra

# BITS                      6    5    5    5    5       6
#                           OP | RS | RT | RD | SHAMT | FUNCT 
# (LW)Load Word         >>  35 | REG| REG|     ENDERECO         OK OK
# (SW)Store Word        >>  43 | REG| REG|     ENDERECO         OK OK
# (BEQ)Branch Equal     >>   4 | REG| REG|     ENDERECO         OK OK
# (SLL)Shift Left       >>   0 | REG| REG| REG| DESLOC| 0       OK OK
# (SRL)Shift Right      >>   0 | REG| REG| REG| DESLOC| 2       OK OK
# Add                   >>   0 | REG| REG| REG|   0   | 32      OK OK
# Sub                   >>   0 | REG| REG| REG|   0   | 34      OK OK
# And                   >>   0 | REG| REG| REG|   0   | 36      OK OK
# OR                    >>   0 | REG| REG| REG|   0   | 37      OK OK
# NOR                   >>   0 | REG| REG| REG|   0   | 39      OK OK
# (SLT)Set on less than >>   0 | REG| REG| REG|   0   | 42      OK OK
# (JR)Jump Register     >>   0 | 31 | REG| REG|   0   | 8       OK OK
# (J)Jump               >>   2 |       ENDERECO                 OK OK
# (JAL)Jump and Link    >>   3 |       ENDERECO                 OK OK

# (LW)Load Word >> $rt = posicao da cache determinado por ($rs + endereco) OK
# (SW)Store Word >> cache[$rs + endereco] = $rt OK
# (BEQ)Branch Equal >> Ir para o endereco se $rs == $rt
# (SLL)Shift Left >> $rd = $rs deslocado pelo shamt para a esquerda -> $rs << shamt -> Multiplicacao OK
# (SRL)Shift Right >> $rd = $rs deslocado pelo shamt para a direita -> $rs >> shamt -> Divisao OK
# Add >> $rd = $rs + $rt OK
# Sub >> $rd = $rs - $rt OK
# And >> $rd = and bit a bit de $rs e $rt -> $rs & $rt OK
# OR >> $rd = or bit a bit de $rs e $rt -> $rs | $rt OK
# NOR >> $rd = nor bit a bit de $rs e $rt -> !($rs | $rt) OK 
# (SLT)Set on less than >> $rd = 1 se $rs < $rt OK
# (JR)Jump Register >> Pular para o endereco no registrador $ra OK
# (J)Jump >> Pula para o endereco informado OK
# (JAL)Jump and Link >> Salva o valor antes de pular em $ra e realiza o pulo para o endereco informado OK
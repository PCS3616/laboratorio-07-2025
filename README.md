# PCS3616 - Laboratório 7 - OP2MNEM

Na aula de hoje continuamos o estudo e uso da linguagem de montagem da
MVN, o ASM (assembly).
Continuaremos usando os módulos Montador, Ligador e Relocador.

## _"Como um montador traduz Mnemônicos para Opcodes?"_

Talvez você já tenha se perguntado isso, mas se não se perguntou,
não tem problema, porque hoje é seu dia de sorte!

Nossa tarefa será construir um pedaço importante de um montador:
subrotinas que fazem a tradução dos mnemônicos (ex.: "JP", "LD")
para os opcodes correspondentes (no caso, "0" e "8"), e vice-versa.


## 1. `op-mnem.asm`
Desenvolva duas sub-rotinas (`OP2MNEM` e `MNEM2OP`), cujas finalidades são:

### OP2MNEM (endereço inicial: 0x100)
Converte um número inteiro dado, 0≤ n ≤ 15, localizado na posição de
memória OPCODE (0x002) no mnemônico correspondente, formado por dois
caracteres ASCII (consultar a tabela de mnemônicos já fornecida).
O mnemônico deverá ser armazenado na posição de memória MNEM (0x004).

### MNEM2OP (endereço inicial: 0x200)
Faz a conversão oposta,
transformando um mnemônico válido localizado em MNEM, dado como dois
caracteres ASCII, em um número inteiro correspondente, , 0 ≤ n ≤ 15,
armazenado na posição de memória OPCODE, novamente conforme a tabela
de mnemônicos fornecida.

### Programa principal (endereço inicial: 0x300)
Não é necessário realizar o programa principal, por isso não utilize
nenhum endereço na faixa 0x300-0x3FF.

Observação: ambos os parâmetros, MNEM e OPCODE, são representados como
inteiros, ocupando, cada qual, dois bytes de memória.

Observação 2: recomenda-se criar um trecho de código separado para as tabelas
de mnemônicos e opcodes (vide Layout da Memória).

  -   Layout da memória:

  | **Endereço/Rótulo** | **Conteúdo**                          |
  |---------------------|---------------------------------------|
  | `0x000`             | Jump para o programa principal        |
  | `0x002` OPCODE      | Variável OPCODE (variável \"global\") |
  | `0x004` MNEM        | Variável MNEM (variável \"global\")   |
  | `0x100` OP2MNEM     | Sub-rotina OP2MNEM                    |
  | `0x200` MNEM2OP     | Sub-rotina MNEM2OP                    |
  | `0x300` MAIN        | Programa principal                    |
  | TABELA              | Tabela de mnemônicos                  |

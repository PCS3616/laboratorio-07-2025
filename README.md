# PCS3616 - Laboratório 7 - ASM 1

Na aula de hoje começamos o estudo e uso da linguagem de montagem da
MVN, o ASM (assembly), e da função de pilha implementada na MVN.
A partir desta aula você só escreverá códigos em ASM, e para isso
precisamos usar os módulos Montador, Ligador e Relocador.

## Instalação das ferramentas

Diferentemente do monitor, essas ferramentas foram escritas em uma
linguagem compilada ([Rust](https://www.rust-lang.org/)), então é
somente necessário instalar um executável.
Instruções sobre esse processo e sobre as opções disponíveis nas
ferramentas estão disponíveis
[em seu repositório](https://github.com/PCS3616/mvn-rs#readme)

### Execução do código gerado

Executar o código MVN gerado deve ser feito da mesma forma que com o
código MVN escrito manualmente.

## Exercícios

## 1.  `fatorial.asm`
No laboratório 4, você escreveu a sub-rotina fatorial. Agora,
    você irá reescrevê-la, mas na linguagem de montagem da MVN.
    Considere os rótulos N e RES, localizados nas posições de memória 0x100
    e 0x102, que representam respectivamente o argumento e o resultado do fatorial.

## 2.  `op-mnem.asm`
Desenvolva duas sub-rotinas (`OP2MNEM` e `MNEM2OP`), cujas finalidades são:

### OP2MNEM (endereço inicial: 0x100)
converte um número inteiro dado, 0≤ n ≤ 15, localizado na posição de 
memória OPCODE (0x002) no mnemônico correspondente, formado por dois
caracteres ASCII (consultar a tabela de mnemônicos fornecida adiante).
O mnemônico deverá ser armazenado na posição de memória MNEM (0x004).

### MNEM2OP (endereço inicial: 0x200)
faz a conversão oposta,
transformando um mnemônico válido localizado em MNEM, dado como dois
caracteres ASCII, em um número inteiro correspondente, , 0 ≤ n ≤ 15,
armazenado na posição de memória OPCODE, novamente conforme a tabela
de mnemônicos fornecida.

### Programa principal (endereço inicial: 0x300)
não é necessário realizar o programa principal, por isso não utilize
nenhum endereço na faixa 0x300-0x3FF.

Observação: ambos os parâmetros, MNEM e OPCODE, são representados como
inteiros, ocupando, cada qual, dois bytes de memória.

Observação 2: recomenda-se criar um trecho de código separado para as tabelas
de mneumônicos e opcodes (vide Layout da Memória).

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

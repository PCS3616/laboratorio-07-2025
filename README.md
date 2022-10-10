# PCS3616 - Laboratório 8 - ASM 1

Na aula de hoje começamos o estudo e uso da linguagem de montagem da
MVN, o ASM (assembly), e da função de pilha implementada na MVN. Para
isso precisamos usar os módulos Montador, Ligador e Relocador (MLR),
então a primeira coisa que devemos fazer é mudar nosso diretório para
onde possamos executar facilmente esses módulos:

  -----------------------------------------------------------------------
  cd \~/Documents/pcs3616/MLR/
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

À partir desta aula você só escreverá códigos em ASM, porém para
executá-los eles precisam estar em linguagem de máquina, para fazer essa
transposição você deverá usar o montador:

  -----------------------------------------------------------------------
  #Como usar o montador\
  python3 montador.py seu_codigo.asm\
  #Saída esperada:\
  #Arquivo seu_codigo.asm montado para seu_codigo.mvn com sucesso!
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

É comum que se escreva vários arquivos com funções a serem ligadas para
funcionarem em conjunto, os detalhes de como fazer isso já foram vistos
em sala, e para ligar arquivos **JÁ MONTADOS** usamos o ligador:

  -----------------------------------------------------------------------
  #Como usar o ligador\
  python3 ligador.py in1.mvn in2.mvn in3.mvn out.mvn\
  #Saída esperada:\
  #Códigos ligados para out.mvn
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

No script acima ligamos 3 arquivos (in1.mvn, in2.mvn e in3.mvn) e a
saída é escrita em out.mvn, mas podemos ligar quantos arquivos
quisermos.

Se você usou origens relocáveis no(s) seu(s) código(s), você também
precisará reloca-los para que se tornem absolutos:

  -----------------------------------------------------------------------
  #Como usar o relocador\
  python3 relocador.py in.mvn out.mvn\
  #Saida esperada:\
  #Código relocado para out.mvn
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

Para executar o código MVN gerado você tem que voltar para o diretório
\~/Documents/pcs3616/MVN/ ou referenciá-lo do diretório MLR/ para
executar o interpretador de MVN. Sugestão: deixe dois terminais abertos,
um em MVN/ e outro em MLR/, dessa forma não será necessário usar o
comando cd a todo momento.

Outra coisa legal dessa aula é que, para os usuários do editor de texto
Sublime, existe um syntax highlighter (o arquivo que deixa os códigos
coloridos) para ASM. Para usar basta você baixar o arquivo
"asm.sublime-syntax" que também está no Moodle desta semana. Para
instalar a linguagem, é só abrir o arquivo no Sublime e salvá-lo por lá.
A mágica está feita.

**Exercícios**

1.  No laboratório 5, você escreveu as sub-rotinas OP2MNEM e MNEM2OP.
    Neste primeiro exercício, você deverá escrever uma versão modificada
    deste programa, desta vez usando a linguagem de montagem da MVN.

Especificações do programa:

-   Nome do arquivo: **op-mnem.asm**

-   Layout da memória:

  -----------------------------------------------------------------------
  **Endereço/Rótulo**    **Conteúdo**
  ---------------------- ------------------------------------------------
  0x000                  Jump para o programa principal

  OPCODE                 Variável OPCODE (variável \"global\")

  MNEM                   Variável MNEM (variável \"global\")

  OP2MNEM                Sub-rotina OP2MNEM

  MNEM2OP                Sub-rotina MNEM2OP

  0x0300/MAIN            Programa principal

  TABELA                 Tabela de mnemônicos
  -----------------------------------------------------------------------

**Entrega:** enviar o arquivo **op-mnem.asm** dentro de um zip**.**

2.  Agora vamos aprender a usar a pilha implementada pela MVN.

A pilha implementada na MVN é muito simples e deve ser operada com
cautela. Para utilizar as funções auxiliares e implementar a pilha você
deve fazer uso da instrução OS (supervisor), o código da função a ser
executada pelo supervisor deve ser carregado no acumulador e o código de
operação da função a ser passado no operando de OS é 0x57. O uso da
instrução deve se dar da seguinte forma: **OS** \<NUM_ARG\> \<FUNC\>

NUM_ARG = 0 (para funções de get, sem parâmetro) ; Ex. de chamada: OS
/057

= 1 (para funções de set, com um parâmetro) ; Ex. de chamada: OS /157

FUNC = 0X57 ; indica qual a função a ser empregada

A pilha será implementada de forma decrescente, diferente daquela que
vocês utilizaram na disciplina de estrutura de dados. Ou seja, a cada
mudança do ponteiro deve-se decrementar o valor do endereço. E o valor
do decremento é de dois (2) e não de um (1) porque na MVN os dados
ocupam sempre dois bytes.

O endereço de stack-pointer da pilha estará inicializado quando vocês
forem iniciar as operações, para conhecer seu valor empregue a função
0x0, para preencher o novo valor (decrementando de dois) empregue a
função 0x1. A pilha deverá ter seu stack-pointer sempre apontando para o
próximo valor livre, de forma a que sempre se possa inserir algum valor
na pilha sem necessitar alterar seu ponteiro. Assim, para se colocar um
valor no endereço apontado pelo stack-pointer empregue a função 0x3 e
posteriormente corrija o stack-pointer decrementando dois do valor
atual. Para capturar um valor do topo da pilha empregue a função 0x2,
mas antes corrija o valor do stack-pointer incrementando dois ao valor
atual.

Para chamar uma das funções basta preencher o acumulador com o valor
correspondente. As funções para uso da pilha são:

-   0: get pointer, esta função salva no acumulador o valor armazenado
    no ponteiro stack-pointer, que está no endereço 0xFFE;

-   1: set pointer, esta função salva no ponteiro stack-pointer, que
    está no endereço 0xFFE, o valor passado como argumento;

-   2: get stacktop, esta função salva no acumulador o valor armazenado
    no endereço de memória apontado pelo ponteiro stack-pointer;

-   3: set stacktop, esta função salva no endereço de memória apontado
    pelo ponteiro stack-pointer o valor passado pelo argumento.

Seu trabalho será escrever 3 rotinas:

-   Empilha: uma rotina que lê uma variável global VALOR e empilha seu
    conteúdo, o rótulo para esta rotina deve ser EMPI;

-   Desempilha: uma rotina que desempilha um número e salva na variável
    global VALOR, o rótulo para esta rotina deve ser DEMP;

-   Principal: uma rotina que lê uma entrada do teclado, empilha,
    desempilha e escreve na tela, o rótulo para esta rotina deve ser
    MAIN.

> OBS.: Não esqueçam de exportar todos os nomes. E **[não]{.underline}**
> utilizem os endereços 0xf00 e 0xf02.

**Entrega:** enviar o arquivo **stack.asm** contendo as três rotinas.

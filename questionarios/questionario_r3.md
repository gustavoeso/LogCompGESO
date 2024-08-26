### 1: Explique como foi feito para reconhecer múltiplos dígitos e realizar múltiplas operações.

**Reconhecimento de Múltiplos Dígitos:**
- No `Tokenizer`, a leitura de números (inteiros) com múltiplos dígitos foi implementada utilizando um loop que acumula caracteres numéricos contíguos.
- Especificamente, quando o `Tokenizer` encontra um dígito (`current_char.isdigit()`), ele entra em um loop que continua a ler os caracteres subsequentes enquanto eles também forem dígitos. Esse conjunto de dígitos é então convertido em um número inteiro (`int(num)`) e armazenado como um token do tipo `NUMBER`.
- Isso permite ao `Tokenizer` reconhecer números como `123`, `45`, ou qualquer outro número composto de múltiplos dígitos.

**Realização de Múltiplas Operações:**
- A realização de múltiplas operações (como soma, subtração, multiplicação e divisão) é gerenciada pelo `Parser`.
- O `Parser` utiliza a abordagem de análise sintática recursiva para processar expressões compostas. Ele divide a expressão em **fatores**, **termos**, e **expressões** mais complexas, respeitando a precedência dos operadores.
- Por exemplo, a multiplicação e a divisão têm maior precedência e são processadas primeiro em `parseTerm`. Soma e subtração, que têm menor precedência, são processadas em `parseExpression`.
- O `Parser` lida com a associação à esquerda dos operadores e resolve a expressão na ordem correta, processando a expressão da esquerda para a direita, enquanto respeita a precedência.

### 2: Pense na estrutura de alguma linguagem procedural (C por exemplo), indique com detalhes como você expandiria o seu programa para compilar um programa nessa linguagem.

**Expansão do Compilador para Suportar uma Linguagem Procedural como C:**

Para expandir o compilador atual para suportar uma linguagem como C, seria necessário adicionar várias funcionalidades adicionais. Aqui está um plano detalhado de como essa expansão poderia ser feita:

**1. **Suporte a Tipos de Dados e Declarações**:
   - **Declarações de Variáveis**: Introduzir uma fase de análise para reconhecer e armazenar declarações de variáveis, como `int x;` ou `float y;`.
   - **Tabela de Símbolos**: Implementar uma tabela de símbolos para armazenar os identificadores das variáveis, seus tipos, e o escopo em que estão definidos.

**2. **Funções e Escopo**:
   - **Definição e Chamadas de Funções**: Adicionar suporte para a definição de funções, reconhecimento de seus parâmetros e tipos de retorno. O `Parser` precisaria identificar declarações como `int func(int a, int b) { ... }` e construir a árvore de sintaxe abstrata (AST) correspondente.
   - **Escopo e Contexto**: Gerenciar diferentes escopos de variáveis (local e global) e passar corretamente as variáveis para as funções.

**3. **Controle de Fluxo**:
   - **Condicionais e Loops**: Implementar estruturas de controle de fluxo como `if-else`, `switch-case`, `while`, e `for`. O `Parser` deve ser capaz de construir a AST para essas estruturas e o gerador de código precisaria traduzi-las para instruções equivalentes em assembly ou outra linguagem de máquina.
   - **Aninhamento e Blocos**: Gerenciar corretamente blocos aninhados de código, respeitando as regras de escopo.

**4. **Operadores Avançados**:
   - **Aritméticos e Lógicos**: Suporte a operadores aritméticos avançados (`++`, `--`, `%`) e operadores lógicos (`&&`, `||`, `!`).
   - **Atribuição e Expressões Complexas**: Permitir expressões complexas que incluem várias operações dentro de uma mesma expressão, como `a = b + c * (d - e);`.

**5. **Entrada e Saída**:
   - Implementar funções básicas de I/O, como `printf` e `scanf`, permitindo ao compilador lidar com a entrada do usuário e exibir saída.

**6. **Geração de Código**:
   - **Backend de Código**: Adicionar uma fase de geração de código que transforma a AST em código assembly ou bytecode específico de uma máquina.
   - **Alocação de Registradores e Memória**: Implementar um alocador de registradores e gerenciar a memória para variáveis locais e globais.

**7. **Suporte a Estruturas de Dados**:
   - **Arrays e Ponteiros**: Expandir o `Parser` para reconhecer e lidar com arrays, ponteiros e acesso a memória direta, características fundamentais de C.
   - **Estruturas (`structs`)**: Implementar suporte para estruturas, que são blocos de memória com múltiplos campos de diferentes tipos.

**8. **Análise Semântica e Otimização**:
   - **Verificação de Tipos**: Adicionar uma fase de verificação de tipos que garanta a compatibilidade dos tipos em expressões e chamadas de função.
   - **Otimizações**: Implementar otimizações de código durante a geração de código, como eliminação de código morto, otimização de loop, e inlining de funções.

**Resumo:**
Para transformar o compilador simples em um compilador de uma linguagem procedural como C, precisaríamos expandir significativamente sua capacidade de reconhecer e processar diferentes tipos de declarações, operadores, estruturas de controle de fluxo, funções, e escopos, além de incluir uma fase robusta de geração de código que traduzisse a AST em código executável ou em código assembly para uma máquina alvo específica.
# Perguntas de discussão — `busca_sem_informacao.py`

As perguntas estão organizadas em cinco blocos temáticos, em ordem crescente
de dificuldade dentro de cada bloco. Cada grupo deve elaborar respostas
justificadas, referenciando trechos do código sempre que possível.

---

## Bloco 1 — Representação do problema

**1.** O que representam os caracteres `S`, `G`, `.` e `#` no grid?
Como a classe `MazeProblem` localiza o estado inicial e o objetivo a partir
dessas marcações?

**2.** Quais movimentos o agente pode fazer e onde isso está definido no
código?
Por que a ação `"N"` corresponde a `(-1, 0)` e não a `(+1, 0)`?
O que isso revela sobre a convenção de indexação do grid?

**3.** Qual é a diferença entre `ACTIONS_fn`, `T` e `c`?
Como esses três métodos juntos definem o modelo de transição do problema?

**4.** O método `c()` sempre retorna `1.0`. O que esse valor representa?
O que precisaria mudar no código se o custo de atravessar certas células fosse
diferente — por exemplo, células com lama custando `3.0` e células normais
custando `1.0`?

**5.** O que o `GoalTest` verifica?
Por que ele é definido como método da classe `MazeProblem` em vez de ser
verificado diretamente dentro de `generic_graph_search`?

---

## Bloco 2 — Nós e reconstrução do caminho

**6.** Para que serve a classe `Node`?
Quais informações ela armazena e por que cada uma delas é necessária para
reconstruir o caminho ao final da busca?

**7.** O que significa o atributo `g` de um nó?
Por que ele foi declarado como `float` em vez de `int`?

**8.** O nó raiz é criado com `parent=None` e `action=None`.
Por que esses campos são `None` especificamente para o nó raiz?
O que aconteceria em `reconstruct_path` se esses campos fossem
obrigatoriamente não-nulos?

**9.** A função `reconstruct_path` constrói o caminho percorrendo os nós de
filho para pai e depois inverte as listas com `reverse()`.
Por que o caminho sai na ordem errada antes da inversão?
Por que não construir o caminho já na ordem correta, inserindo cada elemento
no início da lista?

---

## Bloco 3 — Esquema genérico de busca

**10.** Qual é a ideia geral de `generic_graph_search`?
Como BFS, DFS e UCS se tornam instâncias do mesmo esquema apenas trocando a
estrutura de fronteira?

**11.** O que é o conjunto `explored` e por que ele é importante?
O que poderia acontecer se ele fosse removido do código?

**12.** A função `generic_graph_search` recebe três funções
(`frontier_push`, `frontier_pop`, `frontier_empty`) em vez de receber
diretamente uma estrutura de dados como fila ou pilha.
Que vantagem de design isso traz?

**13.** O teste de objetivo está imediatamente após o `frontier_pop`, e não
no momento em que o nó filho é gerado.
Para a UCS, por que essa escolha é necessária para garantir otimalidade?
Construa um exemplo de grafo com três nós onde testar na geração retornaria
uma solução subótima.

**14.** O código contém este trecho logo após o teste de objetivo:

```python
if n.state in explored:
    continue
explored.add(n.state)
```

Para BFS e DFS, esse bloco nunca é ativado na prática.
Para UCS, ele pode ser ativado.
Explique por que, e descreva o cenário concreto em que um estado aparece mais
de uma vez na fronteira da UCS.

---

## Bloco 4 — Propriedades dos algoritmos

**15.** Qual estrutura de fronteira cada algoritmo usa: BFS, DFS e UCS?
Como a escolha da estrutura determina a ordem de expansão dos nós?

**16.** Em que condições BFS e UCS retornam solução ótima neste código?
Por que DFS não garante otimalidade em geral?

**17.** A UCS usa um contador de desempate na heap: `(n.g, counter, n)`.
O que aconteceria se o contador fosse removido e a tupla fosse apenas
`(n.g, n)`?
Por que o Python não consegue comparar dois objetos `Node` diretamente?

**18.** Compare o comportamento de BFS e DFS no grid `mini_3x3`.
Ambos encontram o mesmo caminho nesse grid.
Isso é sempre esperado?
Construa um grid onde BFS e DFS encontrariam caminhos diferentes e explique
por que isso ocorre.

**19.** Dê um exemplo de modificação simples no grid `mini_3x3` que torne o
problema sem solução.
O que acontece no código quando não há solução — quais funções são afetadas e
o que elas retornam?

---

## Bloco 5 — Infraestrutura e extensibilidade

**20.** Qual a utilidade da função `validate_grid`?
Identifique uma condição importante que ela **não** verifica e que poderia
causar comportamento inesperado durante a busca.
Como você acrescentaria essa verificação?

**21.** Qual a diferença entre usar `--grid` e `--grid-file`?
Para que serve a opção `--list-grids`?
Em que situação cada uma dessas opções seria mais útil na prática?

**22.** O que a opção `--check` valida?
Por que `run_assertions` verifica o custo retornado por BFS e UCS mas não faz
nenhuma afirmação sobre o custo retornado por DFS?

**23.** O código não registra quantos nós foram expandidos durante a busca.
Que modificação mínima você faria para coletar essa informação sem alterar a
lógica dos algoritmos?
Como você usaria esse dado para comparar a eficiência de BFS, DFS e UCS em
diferentes grids?

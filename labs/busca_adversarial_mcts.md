# Perguntas de discussão — `busca_adversarial_mcts.py`

Este laboratório acompanha uma implementação enxuta de **Monte Carlo Tree
Search (MCTS)** no **jogo da velha**. O foco é identificar, no código, os
elementos centrais da aula 05: motivação do MCTS, contadores `N/W`, quatro
passos do algoritmo, UCB1 e política de simulação.

Como o tempo de laboratório é curto, respondam de forma objetiva, sempre
referenciando funções e atributos do código.

---

## Bloco 1 — Representação do jogo e da árvore

**1.** Na classe `TicTacToe`, onde aparecem os equivalentes de:

- estado do jogo: def copy
- ações legais: def available_moves
- transição: def make_move
- teste terminal: def winner/def full/def game_over
- utilidade final: def render

**2.** Na classe `MCTSNode`, qual é o papel de cada atributo abaixo?

- `children`: filhos expandidos do estado do jogo atual
- `visits`: Número total de vezes que este nó foi visitado
- `wins`: Soma dos resultados dos playouts que passaram por este nó
- `untried_moves`: jogadas legais do estado que ainda não foram expandidas. quando estiver vazia é porque o nó foi totalmente expandido.
- `player_just_moved`:Identificador (``'X'`` ou ``'O'``) do jogador que realizou ``move`` para chegar a este nó. Usado na retropropagação para creditar a vitória ao jogador correto.

**3.** Por que o nó guarda contadores agregados (`visits` e `wins`) em vez de
guardar o histórico completo de todas as simulações?

Porque guardar mais que isso não é necessario a unica coisa que importa para esse calculo é quão bem cada nó performou o resto é apenas excesso de uso de memória.

## Bloco 2 — Os quatro passos do MCTS

**4.** Localize em `mcts_decision()` os quatro passos do MCTS:

- `Select`:
        while not node.untried_moves and node.children and not rollout_game.game_over():
            node = node.best_ucb_child(exploration)
            assert node.move is not None
            rollout_game.make_move(node.move)
- `Expand`:
        if node.untried_moves and not rollout_game.game_over():
            node = node.expand(rng)
            rollout_game = node.game.copy()

- `Simulate`:
        while not rollout_game.game_over():
            rollout_game.make_move(rng.choice(rollout_game.available_moves()))
- `Back-propagate`:
        winner = rollout_game.winner()
        while node is not None:
            node.update(winner)
            node = node.parent

Explique em uma frase o objetivo de cada passo.

-O select desce pela arvore, o Expand adiciona um filho se ainda tiver ações não tentadas, a simulation simula a partida com playout aleatorio e por fim o Back-propagate usa esses dados para atualizar os caminhos voltando até a raiz.

**5.** No passo de seleção, por que o algoritmo só desce automaticamente quando
`node.untried_moves` está vazio?

Pois ele vai descer a partir do melhor filho "node = node.best_ucb_child(exploration)" e se o nó atual ainda não esiver totalmente expandido pode ser que ele perca esse melhor filho.

**6.** O passo de simulação executa jogadas aleatórias até o fim da partida.
Por que essas jogadas não viram nós permanentes da árvore?

Porque aqui o objetivo é focar apenas nos estados e não na estrutura da arvore toda. Se tudo virasse nó iria se gastar muito poder computacional em nós ruins que provavelmente nem serão muito explorados.

## Bloco 3 — UCB1 e escolha de ações

**7.** A função `ucb1()` combina dois termos. O que representa:

- a parte `wins / visits`: representa a taxa de sucesso desse nó
- a parte com `sqrt(log(parent.visits) / visits)`: e essa parte mostra o quão ele já foi explorado

**8.** Por que `ucb1()` retorna `inf` quando `visits == 0`? O que isso força o
algoritmo a fazer?

- Faz com que torne prioritario um nó nunca visitado em cima dos já visitados, uma vez que infinito sempre será maior que qualquer valor UCB1 para nós já visitados.

**9.** No final de `mcts_decision()`, a ação retornada é o filho da raiz com
maior `visits`, e não necessariamente o maior `Q = wins / visits`. Qual é a
intuição dessa escolha?

O filho mais visitado, acabou sendo o mais visitado pois era considerado o mais promissor, porem as vezes um nó não muito promissor que foi visitado pouquissimas vezes e mesmo tendo muito menso vitorias que o outro por ter baixa amostragem a taxa de vitoria vai ficar maior, mas continua uma escolha arriscada.

## Bloco 4 — Experimentos curtos

**10.** Execute alguns testes com:

```bash
python3 labs/busca_adversarial_mcts.py --show-stats --iterations 50
python3 labs/busca_adversarial_mcts.py --show-stats --iterations 500
python3 labs/busca_adversarial_mcts.py --mode-x human --mode-o ai --iterations 300
```

Compare o efeito de aumentar o número de iterações sobre a estabilidade da
decisão e sobre os contadores da raiz.

Se mostrou que os testes com mais iterações foca nas jogadas que já se mostraram mais promissoras, tendo assim jogadas mais consitentes.

---

## Comandos úteis

```bash
python3 labs/busca_adversarial_mcts.py
python3 labs/busca_adversarial_mcts.py --show-stats
python3 labs/busca_adversarial_mcts.py --iterations 50 --seed 0
python3 labs/busca_adversarial_mcts.py --iterations 500 --seed 0
python3 labs/busca_adversarial_mcts.py --mode-x human --mode-o ai --iterations 300
```

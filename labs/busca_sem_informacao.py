from __future__ import annotations
import argparse
import time
from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Optional, Set, Tuple
from collections import deque
import heapq

State = Tuple[int, int]  # (row, col)


# ----------------------------
# Problema: Labirinto em grade
# ----------------------------

class MazeProblem:
    """
    Labirinto em grade.
    - '#' = parede
    - 'S' = início
    - 'G' = objetivo
    - '.' = livre
    Movimentos: N, S, L, O. Custo por passo: 1.
    """

    ACTIONS: Dict[str, Tuple[int, int]] = {
        "N": (-1, 0),
        "S": (1,  0),
        "L": (0,  1),
        "O": (0, -1),
    }

    def __init__(self, grid: List[str]):
        self.grid = grid
        self.R = len(grid)
        self.C = len(grid[0]) if self.R > 0 else 0
        self.s0   = self._find("S")
        self.goal = self._find("G")

    def _find(self, ch: str) -> State:
        for r in range(self.R):
            for c in range(self.C):
                if self.grid[r][c] == ch:
                    return (r, c)
        raise ValueError(f"Caractere '{ch}' não encontrado no grid.")

    def in_bounds(self, s: State) -> bool:
        r, c = s
        return 0 <= r < self.R and 0 <= c < self.C

    def passable(self, s: State) -> bool:
        r, c = s
        return self.grid[r][c] != "#"

    def GoalTest(self, s: State) -> bool:
        return s == self.goal

    def ACTIONS_fn(self, s: State) -> Iterable[str]:
        for a, (dr, dc) in self.ACTIONS.items():
            s2 = (s[0] + dr, s[1] + dc)
            if self.in_bounds(s2) and self.passable(s2):
                yield a

    def T(self, s: State, a: str) -> State:
        dr, dc = self.ACTIONS[a]
        return (s[0] + dr, s[1] + dc)

    def c(self, s: State, a: str) -> float:
        return 1.0

    def render_with_path(self, path_states: List[State]) -> str:
        path_set = set(path_states)
        out = []
        for r in range(self.R):
            row = []
            for c in range(self.C):
                ch = self.grid[r][c]
                if (r, c) in path_set and ch not in ("S", "G"):
                    row.append("*")
                else:
                    row.append(ch)
            out.append("".join(row))
        return "\n".join(out)

    def render_with_agent(self, agent: State, path_states: Optional[List[State]] = None) -> str:
        path_set = set(path_states) if path_states is not None else set()
        out = []
        for r in range(self.R):
            row = []
            for c in range(self.C):
                pos = (r, c)
                ch = self.grid[r][c]
                if pos == agent and ch not in ("S", "G"):
                    row.append("A")
                elif pos in path_set and ch not in ("S", "G"):
                    row.append("*")
                else:
                    row.append(ch)
            out.append("".join(row))
        return "\n".join(out)


# ----------------------------
# Nó de busca + reconstrução
# ----------------------------

@dataclass
class Node:
    state:  State
    parent: Optional["Node"]
    action: Optional[str]
    g:      float  # custo acumulado (float para suportar custos não-inteiros)

def reconstruct_path(n: Node) -> Tuple[List[State], List[str]]:
    states:  List[State] = []
    actions: List[str]   = []
    cur: Optional[Node]  = n
    while cur is not None:
        states.append(cur.state)
        if cur.action is not None:
            actions.append(cur.action)
        cur = cur.parent
    states.reverse()
    actions.reverse()
    return states, actions


# -----------------------------------------------------------------------
# Esquema genérico de busca em grafo
#
# Critério de parada: o teste de objetivo é aplicado quando o nó é
# *retirado* da fronteira (expansão), não quando é inserido (geração).
#
# Isso é necessário para garantir otimalidade na UCS: no momento em que
# um nó é gerado, pode ainda existir na fronteira um caminho mais barato
# até o mesmo estado. Só ao expandir o nó confirmamos que seu custo g é
# o mínimo possível.
#
# Para BFS com custo unitário, testar na geração também seria correto
# (e ligeiramente mais eficiente), mas testar na expansão nunca está
# errado. Manter o mesmo critério para todos os algoritmos torna o
# esquema genérico mais claro e uniforme.
# -----------------------------------------------------------------------

def generic_graph_search(
    problem:        MazeProblem,
    frontier_push:  Callable[[Node], None],
    frontier_pop:   Callable[[], Node],
    frontier_empty: Callable[[], bool],
) -> Optional[Node]:

    start = Node(state=problem.s0, parent=None, action=None, g=0.0)
    frontier_push(start)
    explored: Set[State] = set()

    while not frontier_empty():
        n = frontier_pop()

        # Critério de parada: testar na expansão, não na geração.
        if problem.GoalTest(n.state):
            return n

        # Se o estado já foi expandido por um caminho de custo menor
        # (pode ocorrer na UCS quando há duplicatas na fronteira),
        # descartamos este nó sem reexpandir.
        if n.state in explored:
            continue
        explored.add(n.state)

        for a in problem.ACTIONS_fn(n.state):
            s2 = problem.T(n.state, a)
            if s2 in explored:
                continue
            n2 = Node(
                state=s2,
                parent=n,
                action=a,
                g=n.g + problem.c(n.state, a),
            )
            frontier_push(n2)

    return None  # fronteira esgotada sem encontrar o objetivo


# -----------------------------------------------------------------------
# BFS — Busca em Largura
#
# Fronteira: fila FIFO. Expande sempre o nó inserido há mais tempo,
# garantindo que os estados sejam alcançados em ordem crescente de
# profundidade. Ótima quando todos os custos de ação são iguais.
# -----------------------------------------------------------------------

def bfs(problem: MazeProblem) -> Optional[Node]:
    q: deque[Node] = deque()
    return generic_graph_search(
        problem,
        frontier_push=q.append,
        frontier_pop=q.popleft,
        frontier_empty=lambda: len(q) == 0,
    )


# -----------------------------------------------------------------------
# DFS — Busca em Profundidade
#
# Fronteira: pilha LIFO. Expande sempre o nó inserido mais recentemente,
# mergulhando em um ramo antes de tentar os demais. Não garante
# otimalidade nem completude em espaços com ciclos (sem explored).
# -----------------------------------------------------------------------

def dfs(problem: MazeProblem) -> Optional[Node]:
    st: List[Node] = []
    return generic_graph_search(
        problem,
        frontier_push=st.append,
        frontier_pop=st.pop,
        frontier_empty=lambda: len(st) == 0,
    )


# -----------------------------------------------------------------------
# UCS — Busca de Custo Uniforme
#
# Fronteira: fila de prioridade ordenada por g (custo acumulado).
# Garante otimalidade para qualquer custo de ação não-negativo.
#
# Diferentemente de BFS e DFS, a UCS permite que um mesmo estado apareça
# na fronteira mais de uma vez, com custos diferentes, quando é
# alcançável por múltiplos caminhos. O conjunto `explored` garante que
# cada estado seja *expandido* no máximo uma vez: quando um estado é
# retirado da fronteira pela primeira vez, seu custo g é necessariamente
# o mínimo (pois a fila de prioridade sempre retorna o menor g), e todas
# as cópias subsequentes do mesmo estado na fronteira são descartadas
# pelo teste `if n.state in explored`.
#
# Por isso, ao contrário de BFS e DFS, a UCS não usa `in_frontier` para
# bloquear inserções: bloquear seria incorreto, pois impediria a
# atualização do custo de um estado já na fronteira com um caminho
# mais barato.
# -----------------------------------------------------------------------

def ucs(problem: MazeProblem) -> Optional[Node]:
    # Heap de tuplas (g, contador, nó). O contador garante desempate
    # estável quando dois nós têm o mesmo g, evitando comparação entre
    # objetos Node (que não implementam __lt__).
    heap:    List[Tuple[float, int, Node]] = []
    counter: int = 0

    def push(n: Node) -> None:
        nonlocal counter
        heapq.heappush(heap, (n.g, counter, n))
        counter += 1

    def pop() -> Node:
        return heapq.heappop(heap)[2]

    return generic_graph_search(
        problem,
        frontier_push=push,
        frontier_pop=pop,
        frontier_empty=lambda: len(heap) == 0,
    )


# ----------------------------
# Execução / CLI
# ----------------------------

Solver = Callable[[MazeProblem], Optional[Node]]

SOLVERS: List[Tuple[str, Solver]] = [
    ("BFS", bfs),
    ("DFS", dfs),
    ("UCS", ucs),
]

STRATEGY_TO_SOLVER: Dict[str, Tuple[str, Solver]] = {
    "bfs": ("BFS", bfs),
    "dfs": ("DFS", dfs),
    "ucs": ("UCS", ucs),
}

GRID_CATALOG: Dict[str, List[str]] = {
    "mini_3x3": [
        "S..",
        "##.",
        "..G",
    ],
    # Grid 4x5 da figura "reflexo vs planejador":
    # S em (0,0) e G em (0,4), com bifurcação visual em (1,1).
    "bifurcacao_reflexo_planejador": [
        "S.##",
        "#...",
        "..#.",
        "###.",
        "G...",
    ],
    "corredores": [
        "S......",
        ".#####.",
        ".......",
        ".#####.",
        "......G",
    ],
    # Sem solução: o objetivo fica completamente cercado por paredes.
    "sem_solucao": [
        "S....",
        ".###.",
        ".#G#.",
        ".###.",
        ".....",
    ],
}


def validate_grid(grid: List[str]) -> None:
    if not grid:
        raise ValueError("Grid vazio.")

    cols = len(grid[0])
    if cols == 0:
        raise ValueError("Grid com linha vazia.")

    for i, row in enumerate(grid, start=1):
        if len(row) != cols:
            raise ValueError(
                f"Grid não retangular: linha {i} tem tamanho {len(row)}, esperado {cols}."
            )
        for ch in row:
            if ch not in {"S", "G", ".", "#"}:
                raise ValueError(f"Caractere inválido no grid: '{ch}'.")

    starts = sum(row.count("S") for row in grid)
    goals = sum(row.count("G") for row in grid)
    if starts != 1:
        raise ValueError(f"Grid deve conter exatamente 1 'S' (encontrado: {starts}).")
    if goals != 1:
        raise ValueError(f"Grid deve conter exatamente 1 'G' (encontrado: {goals}).")


def load_grid_from_file(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    return [line for line in lines if line.strip() != ""]


def run_searches(
    grid: List[str],
    solvers: List[Tuple[str, Solver]] = SOLVERS,
    label: Optional[str] = None,
    animate: bool = False,
    delay: float = 0.3,
) -> Dict[str, Optional[Node]]:
    validate_grid(grid)
    problem = MazeProblem(grid)

    if label:
        print(f"\n=== Grid: {label} ===")
    else:
        print("\n=== Grid ===")
    for row in grid:
        print(" ", row)

    results: Dict[str, Optional[Node]] = {}
    for name, solver in solvers:
        goal_node = solver(problem)
        results[name] = goal_node
        print(f"\n--- {name} ---")
        if goal_node is None:
            print("Sem solução.")
            continue
        states, actions = reconstruct_path(goal_node)
        print(f"Ações : {actions}")
        print(f"Custo : {goal_node.g}")
        print(f"Estados: {states}")
        print(problem.render_with_path(states))
        if animate:
            animate_execution(problem, states, name, delay)

    return results


def animate_execution(problem: MazeProblem, states: List[State], algo_name: str, delay: float) -> None:
    for step, state in enumerate(states):
        visited = states[:step]
        # Limpa a tela e redesenha o grid a cada passo.
        print("\033[H\033[J", end="")
        print(f"Animação: {algo_name} | passo {step}/{len(states) - 1}")
        print(problem.render_with_agent(state, path_states=visited))
        time.sleep(delay)
    print("\nAnimação finalizada.")


def run_assertions(animate: bool = False, delay: float = 0.3) -> None:
    # Em custo unitário, BFS e UCS devem retornar caminho ótimo (custo 6).
    # DFS pode coincidir aqui, mas isso não é garantido em geral.
    results = run_searches(
        GRID_CATALOG["corredores"],
        label="corredores (check)",
        animate=animate,
        delay=delay,
    )
    assert results["BFS"] is not None and results["BFS"].g == 6.0
    assert results["UCS"] is not None and results["UCS"].g == 6.0
    assert results["DFS"] is not None
    print("\nChecks de corretude passaram.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Tutorial de busca sem informação (BFS, DFS, UCS)."
    )
    parser.add_argument(
        "--grid",
        default="mini_3x3",
        choices=sorted(GRID_CATALOG.keys()),
        help="Nome do grid do catálogo.",
    )
    parser.add_argument(
        "--grid-file",
        default=None,
        help="Arquivo .txt com o grid (uma linha por linha da grade).",
    )
    parser.add_argument(
        "--strategy",
        choices=sorted(STRATEGY_TO_SOLVER.keys()),
        default=None,
        help="Estratégia de busca: bfs, dfs ou ucs. Se omitido, executa todas.",
    )
    parser.add_argument(
        "--list-grids",
        action="store_true",
        help="Lista grids disponíveis no catálogo e sai.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Roda checagens de corretude adicionais.",
    )
    parser.add_argument(
        "--animate",
        action="store_true",
        help="Anima a execução do plano encontrado no terminal.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.3,
        help="Atraso (em segundos) entre passos da animação.",
    )
    return parser.parse_args()


def main() -> None:
    """
    Comandos úteis:
    - python3 src/busca_sem_informacao.py
      Executa o grid padrão (`mini_3x3`) com as três estratégias (BFS, DFS e UCS).

    - python3 src/busca_sem_informacao.py --list-grids
      Lista os nomes dos grids disponíveis no catálogo interno.

    - python3 src/busca_sem_informacao.py --grid corredores
      Executa um grid específico do catálogo com todas as estratégias.

    - python3 src/busca_sem_informacao.py --grid bifurcacao_reflexo_planejador
      Roda o cenário de bifurcação usado para discutir agente reflexo vs planejador.

    - python3 src/busca_sem_informacao.py --grid sem_solucao
      Executa um cenário sem caminho até o objetivo (todos devem falhar).

    - python3 src/busca_sem_informacao.py --strategy bfs
      Executa apenas a estratégia escolhida (`bfs`, `dfs` ou `ucs`) no grid padrão.

    - python3 src/busca_sem_informacao.py --grid bifurcacao_reflexo_planejador --strategy bfs
      Combina escolha de grid com execução de uma única estratégia.

    - python3 src/busca_sem_informacao.py --grid-file caminho/do/grid.txt
      Carrega o grid de um arquivo texto externo (uma linha da grade por linha).

    - python3 src/busca_sem_informacao.py --grid-file caminho/do/grid.txt --strategy ucs
      Útil para testar rapidamente cenários externos com a UCS.

    - python3 src/busca_sem_informacao.py --check
      Executa checagens de corretude adicionais (BFS/UCS ótimos no grid de teste).
      
    - python3 src/busca_sem_informacao.py --grid mini_3x3 --animate --delay 0.2
      Mostra a execução passo a passo no terminal; `--delay` controla a velocidade.

    - python3 src/busca_sem_informacao.py --grid corredores --strategy dfs --animate --delay 0.1
      Exemplo combinando grid, estratégia única e animação rápida.
    """
    args = parse_args()

    if args.list_grids:
        print("Grids disponíveis:")
        for name in sorted(GRID_CATALOG.keys()):
            print(f" - {name}")
        return

    if args.grid_file is not None:
        grid = load_grid_from_file(args.grid_file)
        label = f"arquivo: {args.grid_file}"
    else:
        grid = GRID_CATALOG[args.grid]
        label = args.grid

    if args.strategy is None:
        selected_solvers = SOLVERS
    else:
        selected_solvers = [STRATEGY_TO_SOLVER[args.strategy]]

    run_searches(
        grid,
        solvers=selected_solvers,
        label=label,
        animate=args.animate,
        delay=args.delay,
    )

    if args.check:
        run_assertions(animate=args.animate, delay=args.delay)


if __name__ == "__main__":
    main()

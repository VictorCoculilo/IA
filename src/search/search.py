# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    """
    
    frontier = util.Stack() #cria a pilha   
    startNode = problem.getStartState() #pega o estado inicial
    startPath = [] #caminho inicial vazio
    frontier.push((startNode, startPath)) # (estado, caminho) #adiciona o estado inicial na pilha

    expanded = set()    #conjunto para armazenar os nós expandidos

    while not frontier.isEmpty():   
        node, path = frontier.pop()   #remove o nó do topo da pilha

        if problem.isGoalState(node):   #verifica se o nó é o estado objetivo, se for, retorna o caminho
            return path

        if node not in expanded:    #verifica se o nó já foi expandido, se não foi, expande o nó
            expanded.add(node)

            for child, action, cost in problem.expand(node):    #expande o nó, obtendo os filhos, ações e custos(não utilizado)
                if child not in expanded:   #verifica se o filho já foi expandido, se não foi, adiciona o filho na pilha
                    frontier.push((child, path + [action])) #adiciona o filho na pilha com o caminho atualizado

    return []  # Retorna uma lista vazia se não encontrar o caminho

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    
    #basicamente o mesmo código do DFS, mas com uma fila ao invés de uma pilha
    
    frontier = util.Queue()  # cria uma fila(a principal diferença)
    startNode = problem.getStartState() #pega o estado inicial
    startPath = []  #caminho inicial vazio
    frontier.push((startNode, startPath))  # (estado, caminho) #adiciona o estado inicial na pilha

    expanded = set()    #conjunto para armazenar os nós expandidos

    while not frontier.isEmpty():
        node, path = frontier.pop() #remove o nó do topo da pilha

        if problem.isGoalState(node):   #verifica se o nó é o estado objetivo, se for, retorna o caminho
            return path

        if node not in expanded:    #verifica se o nó já foi expandido, se não foi, expande o nó
            expanded.add(node)

            for child, action, cost in problem.expand(node):    #expande o nó, obtendo os filhos, ações e custos(não utilizado)
                if child not in expanded:   #verifica se o filho já foi expandido, se não foi, adiciona o filho na pilha
                    frontier.push((child, path + [action])) #adiciona o filho na pilha com o caminho atualizado
                    
    return []  # Retorna uma lista vazia se não encontrar o caminho

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    #bem parecido com os outros, mas com uma fila de prioridade
    frontier = util.PriorityQueue() # cria uma fila de prioridade(a principal diferença)
    startNode = problem.getStartState() #pega o estado inicial
    startPath = []  #caminho inicial vazio
    startCost = 0   #variavel nova que representa o custo inicial, no caso aqui é 0 
    
    #adiciona o estado inicial na fila de prioridade com o custo inicial + heurística do estado inicial
    frontier.push((startNode, startPath, startCost), startCost + heuristic(startNode, problem))

    explored = set()    #conjunto para armazenar os nós expandidos


    while not frontier.isEmpty():   
        node, path, totalCost = frontier.pop()  #remove o nó do topo da fila de prioridade, dividindo o nó, o caminho e o custo total
        if problem.isGoalState(node):   #verifica se o nó é o estado objetivo, se for, retorna o caminho
            return path

        if node not in explored:    #verifica se o nó já foi expandido, se não foi, expande o nó
            explored.add(node)

            for child, action, stepCost in problem.expand(node):    #expande o nó, obtendo os filhos, ações e o custo
                if child not in explored:   #verifica se o filho já foi expandido, se não foi, adiciona o filho na fila de prioridade
                    newCost = totalCost + stepCost  #custo total do nó atual + custo do passo
                    newPath = path + [action]   #caminho atualizado com a ação
                    priority = newCost + heuristic(child, problem)  #custo total + heurística do filho
                    frontier.push((child, newPath, newCost), priority) #adiciona o filho na fila de prioridade com o custo total + heurística do filho
                    
    return []  # Retorna uma lista vazia se não encontrar o caminho 

def iterativeDeepeningSearch(problem):

    def dls(state, depth, path, visited):   #função auxiliar para a busca em profundidade iterativa
        if problem.isGoalState(state):  #verifica se o nó é o estado objetivo, se for, retorna o caminho
            return path
        if depth == 0:  #verifica se a profundidade é 0, se for, retorna None
            return None

        visited.add(state)  #adiciona o nó atual na lista de visitados
        for child, action, stepCost in problem.expand(state):   #expande o nó, obtendo os filhos, ações e custos(não utilizado)
            if child not in visited:    #verifica se o filho já foi visitado, se não foi, chama a função recursivamente
                result = dls(child, depth - 1, path + [action], visited.copy()) #chama a função recursivamente com a profundidade - 1, o caminho atualizado e a lista de visitados
                if result is not None:  #verifica se o resultado não é None, se não for, retorna o resultado
                    return result
        return None

    depth = 0
    while True:
        visited = set() 
        #chama a função dls com o estado inicial, profundidade, caminho vazio e lista de visitados vazia
        result = dls(problem.getStartState(), depth, [], visited) 
        if result is not None:
            return result
        depth += 1  #aumenta a profundidade para a próxima iteração

# Abbreviations
ids = iterativeDeepeningSearch
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch

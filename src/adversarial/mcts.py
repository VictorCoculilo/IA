import math
import random

class MCTSNode:
    '''
        This class represents a node in the tree generated when executing the Monte Carlo Tree Search (MCTS) algorithm.
        Each node corresponds to a game state and contains information about the game,
        the moves available from that state, and the results of simulations from that state.
        The node keeps track of its parent, the move that led to it, the number of visits,
        the number of wins, and the children nodes that can be reached from it.
    '''
    def __init__(self, game, parent=None, move=None):
        '''
            Initialize the MCTSNode with the current game state, parent node, and move that led to this state.
            Also initializes the list of untried moves from this state.
        '''
        self.game = game
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.wins = 0
        self.untried_moves = game.available_moves()

    def ucb1(self, c=math.sqrt(2)):
        '''
            Upper Confidence Bound for Trees (UCB1) algorithm.
            This function calculates the UCB1 value for the node, which is used to balance exploration and exploitation.
            The formula is: UCB1 = (wins / visits) + c * sqrt(log(parent_visits) / visits)
            where c is a constant that determines the level of exploration.
        '''
        if self.visits == 0:
            return float('inf')
        return self.wins / self.visits + c * math.sqrt(math.log(self.parent.visits) / self.visits)

    def select_child(self):
        '''
            Select the child node with the highest UCB1 value.
            This function is used during the selection phase of MCTS to choose which child node to explore next.
        '''
        # If there are no children, return None
        if not self.children:
            return None
        # If there are untried moves, we can return the first child
        if self.untried_moves:
            return self.children[0]
        # Otherwise, we select the child with the highest UCB1 value
        return max(self.children, key=lambda child: child.ucb1())

    def expand(self):
        '''
            Expand the node by creating a new child node for one of the untried moves.
            This function is used during the expansion phase of MCTS to add a new node to the tree.
        '''
        # If there are no untried moves, we cannot expand
        if not self.untried_moves:
            return None
        # Select a random untried move and remove it from the list
        # This is a simple strategy; in practice, you might want to use a more sophisticated method
        # to select the move (e.g., based on heuristics or other criteria)
        move = self.untried_moves.pop()

        new_game = self.game.copy()
        new_game.make_move(move)
        child = MCTSNode(new_game, parent=self, move=move)
        self.children.append(child)
        return child

    def update(self, result):
        '''
            Update the node with the result of a simulation.
                If the result is positive, increment the number of wins
                If the result is negative, decrement the number of wins
                If the result is zero, do nothing
            This function is used during the backpropagation phase of MCTS to update the node's statistics.
        '''
        self.visits += 1
        self.wins += result

def mcts(game, iterations=200):
    root = MCTSNode(game)

    for _ in range(iterations):
        node = root
        game_sim = game.copy()

        # Selection
        while node.untried_moves == [] and node.children:
            node = node.select_child()
            game_sim.make_move(node.move)

        # Expansion
        if node.untried_moves:
            node = node.expand()
            game_sim = node.game.copy()

        # Simulation
        while not game_sim.game_over():
            move = random.choice(game_sim.available_moves())
            game_sim.make_move(move)

        # Backpropagation
        winner = game_sim.winner()
        if winner == 'X':
            result = 1
        elif winner == 'O':
            result = -1
        else:
            result = 0

        while node is not None:
            perspective = 1 if node.game.current == 'O' else -1
            node.update(perspective * result)
            node = node.parent

    best_child = max(root.children, key=lambda c: c.visits)
    return best_child.move

from puzzle import *
from queue import PriorityQueue

class Solver:
    """
    A class to implement three different search algorithms to solve an 8-puzzle
    """

    def __init__(self,alg="UCS"):
        self.puzzle = Puzzle() # Puzzle object used to calculate valid moves, cost calculations, etc.
        self.visited = [] # List of visited nodes
        self.open = PriorityQueue() # Priority queue of nodes to visit
        self.alg = alg # Specifies which of the three algorithms to use
        self.past_positions = set() # Keep track of puzzle positions that have been visited to avoid looping
        self.found_solution = False

    def solve(self,initial_position):
        """Runs the algorithm to solve the puzzle state given by initial_position string"""
        self.reset()
        self.puzzle.set_state(initial_position)
        logging.info(f"Now attempting to solve:\n{self.puzzle}")
        if self.puzzle.is_solved():
            return
        if not(self.puzzle.is_solvable()):
            raise Exception(f"The puzzle\n{self.puzzle}\ncannot be solved due to the inversion parity not matching the parity of the solved state.")
        # Add the first node
        self.create_node(0)

        while not(self.open.empty()) and not(self.found_solution):
            logging.info(f"{'~~|~~'*10}\n{self.open.qsize()} objects in queue\n")
            for i in self.open.queue[:5]:
                logging.info(f"\t{i}")
            self.expand()

        logging.info(f"<{'=---='*50}>")
        logging.info(f"Solved puzzle:\n{self.puzzle}")
        logging.info(f"Visited {len(self.visited)} nodes")

    def reset(self):
        """Resets the solver to prepare for another puzzle"""
        self.puzzle.set_state("012345678")
        self.visited = []
        self.open = PriorityQueue()
        self.past_positions = set()
        self.found_solution = False

    def expand(self):
        """Visits a given node by finding the next valid states of the puzzle"""
        _,node = self.open.get() # Pull the next node from the priority queue
        self.visited.append(node)
        next_depth = node.depth + 1 # Next nodes will have more depth
        self.puzzle.set_state(node.puzzle_state)
        logging.info(f"<{'='*30}>\nNode at depth {node.depth}:\n{self.puzzle}\n{'='*30}")
        logging.info(f"Hamming Distance: {self.puzzle.get_unsolved_pieces()}")
        logging.info(f"Manhattan Distance: {self.puzzle.total_manhattan_distance()}")
        logging.info(f"Nilsson Score: {self.puzzle.nilsson_score()}")
        logging.info(f"Inversions: {self.puzzle.count_inversions()}")
        logging.info(f"Moves:{node.move_sequence()}")
        if self.puzzle.is_solved():
            self.found_solution = True
            logging.info(f"Solution: {node.move_sequence()}")
            return
        prev_pos = self.puzzle.get_empty_position() # prev_pos of the next nodes will be the current position. This will make sure that if/when we expand those nodes, they never make a move back to the previous position.
        next_moves = self.puzzle.list_valid_moves()
        if node.prev_pos in next_moves: # Remove the previous position from the list so we don't go back to it
            next_moves.remove(node.prev_pos)
        
        logging.info(f"{len(next_moves)} available moves:")

        for move in next_moves: # Now we go through the next valid moves and create new states
            logging.info(f"\nPuzzle after moving {self.puzzle.state[move]} to the empty square:")
            self.puzzle.move(move)
            self.create_node(next_depth,prev_pos,parent=node)
            self.puzzle.move(prev_pos) # Return the puzzle to the previous position to add the next move

    def create_node(self,depth,prev_pos=-1,parent=None):
        """Calculates the total cost of the current puzzle state and creates and queues a new node with the given depth

        Args:
            depth (int): Depth of the node in the search tree
            prev_pos (int): Used to avoid repeating a previous position. -1 just means this is the starting position so there were no previous moves made before
        """
        if self.puzzle.get_state_str() in self.past_positions: # If the puzzle has been in that position before, don't bother adding a node, otherwise we end up with looping
            return
        cost = 0
        if self.alg == "UCS": # Uniform Cost Search just uses the node's depth as the cost
            cost = depth
        elif self.alg == "BFS": # Best-first Search uses the Manhattan distance of the current puzzle state
            cost = self.puzzle.total_manhattan_distance()
        elif self.alg == "A": # A* Search uses both the depth and the Nilsson's sequence to calculate the cost
            cost = depth + self.puzzle.nilsson_score()
        else: # If the Solver object does not have a specified algorithm or was initialized with an invalid algorithm, something went really wrong
            raise Exception("Something went wrong. No valid algorithm was specified.")
        
        self.past_positions.add(self.puzzle.get_state_str())
        node = Node(self.puzzle.get_state_str(),depth,prev_pos,parent)
        logging.info(f"{self.puzzle}\nCost: {cost}\nDepth: {depth}")
        self.open.put((cost,node)) # Place the node into the priority queue

class Node:
    """
    A class to implement the nodes for the search algorithms to traverse

    Attributes:
        puzzle_state (str): String representing the state of the puzzle
        depth (int): Depth of the node in the search tree
        prev_pos (int): Used by the search algorithm to avoid a previous position
    """

    def __init__(self,puzzle_state,depth,prev_pos=-1,parent=None):
        self.puzzle_state = puzzle_state
        self.depth = depth
        self.prev_pos = prev_pos
        self.parent = parent

    def move_sequence(self):
        """Traces the move sequence"""
        if self.prev_pos == -1 or self.parent.prev_pos == -1: return ''
        return self.parent.move_sequence() + str(self.prev_pos)

    def __repr__(self):
        return f"{self.puzzle_state}"
    
    def __lt__(self,other):
        return str(self) < other
    
    def __gt__(self,other):
        return str(self) > other
    
    def __eq__(self, other):
        return str(self) == other

if __name__=="__main__":
    puzz = "412367580"

    UCS = Solver()
    UCS.solve(puzz)

    logging.info(f"{'='*50}\nBest-first Search\n{'='*100}")
    BFS = Solver("BFS")
    BFS.solve(puzz)

    logging.info(f"{'='*50}\nA* Search\n{'='*100}")
    A_star = Solver("A")
    A_star.solve(puzz)
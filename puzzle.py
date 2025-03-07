import random
import logging

logging.basicConfig(filename='8-puzzle.log', level=logging.INFO, format='%(message)s')

class Puzzle:
    """
    A class representing a sliding puzzle that the algorithm will have to solve. The puzzle state is represented as a 9 element long list with each element representing the number at the given position. The indices are laid out like this:
    |1|2|3|
    |8|0|4|
    |7|6|5|
    Basically, this just makes it so the solved state is just [0,1,2,3,4,5,6,7,8] making it easier for me to debug and stuff. Maybe there's a better way of approaching this, but this is the easiest approach I can think of.

    Attributes:
        state (list): List of integers representing the numbers at each position of the puzzle.
        COORDS (list): List of pairs representing the matrix coordinates of each piece index. Due to the way I've implemented the puzzle representation, this static variable will help with calculating Manhattan distances.
    """

    COORDS = [
        (1,1),
        (0,0),
        (0,1),
        (0,2),
        (1,2),
        (2,2),
        (2,1),
        (2,0),
        (1,0)
    ]

    def __init__(self, initial_state=None):
        """Initializes a Puzzle object
        """
        self.state = [0,1,2,3,4,5,6,7,8] # Solved state
        if initial_state:
            self.set_state(initial_state)

    def set_state(self,state_string:str):
        """Sets a new state for the puzzle using a string

        Args:
            state_string (str): String representing the new puzzle position
        """
        if(len(state_string) != 9): raise Exception("state_string must be 9 long")
        try:
            int_list = [int(x) for x in state_string] # We gotta make sure all the characters are numbers
        except:
            raise Exception("All characters need to be an integer")
        
        # Next make sure all the numbers are unique and are valid pieces in the puzzle (integers 0-8). There is probably a much better way to do this, but this is what I thought of.
        if((len(int_list) != len(set(int_list))) or (set(int_list) != {0,1,2,3,4,5,6,7,8})): 
            raise Exception("Integers must be unique and within the range 0 to 8")
        
        self.state = int_list # Finally, we can set the valid state.

    def get_state_str(self) -> str:
        """Returns the puzzle state as a string that can be read by set_state()"""
        return "".join([str(x) for x in self.state])

    def is_solved(self) -> bool:
        """Returns true if puzzle is solved"""
        return self.state == [0,1,2,3,4,5,6,7,8]
    
    def get_unsolved_pieces(self) -> int:
        """Returns the number of pieces that are not in their solved position (the Hamming distance). This will be used in the heuristics for the search algorithms."""
        return sum([x!=y and y!=0 for x,y in enumerate(self.state)])
    
    def get_manhattan_distance(self,piece) -> int:
        """Returns the Manhattan distance of the given piece from its correct position
        
        Args:
            piece (int): Integer representing the value displayed on the piece. Alternatively, this can be described as the index position of the piece in the solved state.
            
        Returns:
            int: The Manhattan distance of the piece from its final position"""
        if piece==0: return 0 # The empty lot is not counted
        piece_position = self.state.index(piece) # Index position of the piece in the current state of the puzzle

        current_place = Puzzle.COORDS[piece_position] # Matrix coordinates of the piece's current position
        final_place = Puzzle.COORDS[piece] # Where the piece needs to be

        return abs(current_place[0]-final_place[0]) + abs(current_place[1]-final_place[1])
    
    def total_manhattan_distance(self) -> int:
        """Returns the sum of the Manhattan distances for all the pieces in the puzzle. This will also be used in the heuristics for the search algorithms."""
        return sum(self.get_manhattan_distance(x) for x in self.state)
    
    def nilsson_score(self) -> int:
        """Returns the Nilsson's sequence score for the current state of the puzzle. This function implements it as described in the lecture slides, so I'll include the steps in the docstring to help myself.
        1. Tile in center scores 1 (So basically if the empty lot is not in the center)
        2. For each tile around the center, if the next tile clockwise is not the correct tile, score 2
        3. Multiply the sequence by 3
        4. Add the total Manhattan distance to the score"""
        score = 0
        if self.get_empty_position() != 0: # Means there is a tile in the center
            score += 1
        
        for i in range(1,9): # Skip the center tile
            current_piece = self.state[i]
            next_piece = self.state[i%8+1]
            if current_piece != 0 and next_piece != (current_piece%8 + 1):
                score += 2

        return 3*score + self.total_manhattan_distance()

    def get_empty_position(self) ->  int:
        """Returns the position of the empty space in the puzzle"""
        return self.state.index(0)
    
    def is_solvable(self) -> bool:
        """Returns true if it is solvable"""
        return self.count_inversions()%2 != 0 # Since the solved state has odd parity, the current state needs to be odd too in order to be solvable. 
    
    def count_inversions(self) -> int:
        """Counts the number of inversions to help determine if the puzzle is solvable from the current state"""
        # Due to the way I've implemented the puzzle, finding the row-major order of the pieces is a bit unnatural, but it should work fine
        placements = [1,2,3,8,0,4,7,6,5]
        row_major_order = []
        count = 0

        for position in placements:
            if self.state[position] != 0: # Empty space isn't included
                row_major_order.append(self.state[position])

        # I could definitely have made this much neater with list comprehensions, but this makes it easier for me to compare to the example I looked at
        for i in range(len(row_major_order)):
            for j in range(i+1,len(row_major_order)):
                first_square = row_major_order[i]
                second_square = row_major_order[j]
                if first_square > second_square:
                    count += 1

        return count

    def list_valid_moves(self):
        """Provides a list of valid indices to move the current empty space to. Technically, it's the squares that can move into the empty space, but it is much easier to imagine the empty space being the one that's moving.

        Returns:
            list[int]: List of valid moves given the current position of the puzzle.
        """

        position = self.state.index(0) # Find where the empty space is

        if position == 0:
            return [2,4,6,8] # If the empty space is in the middle, any of the even numbered squares can move to it
        
        # When the empty lot is not in the center, the next and previous squares in the spiral are valid positions
        next_square = position%8 + 1
        prev_square = position - 1 if position > 1 else 8 # There is probably a better way to do this, but this was the only way I could think of making sure the position previous to 1 is always 8
        
        # Even-numbered spaces can always move to position 0, so we always include it in the valid moves. Otherwise, the only valid moves are the next and previous squares in the spiral.
        if position%2 == 0:
            return [0,prev_square,next_square]
        else:
            return [prev_square,next_square]
        
    def move(self,position:int):
        """If possible, moves whatever number is in the provided position into the empty space. More specifically, it swaps wherever 0 is in the list to the position argument as long as it is a valid move.

        Args:
            position (int): Position to swap with the empty space. Raises an error if the move is invalid.
        """
        valid_moves = self.list_valid_moves()
        empty_lot = self.state.index(0) # Position of the empty space (i.e. the element with value 0)
        if not(position in valid_moves):
            raise Exception(f"Invalid move. Square [{self.state[position]}] at position {position} cannot move into the empty space at position {empty_lot}")
        
        # Swap the values
        self.state[empty_lot],self.state[position] = self.state[position],self.state[empty_lot]

    def shuffle(self,num_moves = 31):
        """Shuffles the puzzle by doing random valid moves (originally I just had it shuffle the list, but then I remembered that some configurations are unsolvable)
        
        Args:
            num_moves (int): number of random moves to do. By default, it is 31 because I read somewhere that it takes 31 moves to solve the 8-puzzle, but I could not find the original source that explicitly states this, so I'll figure it out later.
        """
        move_count = 0
        prev_position = random.choice(self.list_valid_moves())

        while move_count < num_moves:
            valid_moves = self.list_valid_moves()
            valid_moves.remove(prev_position) # Makes sure we don't undo the previous move because there is a very good chance of that happening
            next_move = random.choice(valid_moves)
            prev_position = self.get_empty_position()
            self.move(next_move)
            move_count += 1

    def move_sequence(self,sequence):
        """Performs a sequence of moves represented as a string of integers"""
        logging.info(f"Initial position:\n{self}\nh(n): {self.get_unsolved_pieces()}\nInversions: {self.count_inversions()}\n")
        for move in sequence:
            self.move(int(move))
            logging.info(f"Position after moving {move}: {self.get_state_str()}\n{self}\nh(n): {self.get_unsolved_pieces()}\nInversions: {self.count_inversions()}")
            logging.info(f"Manhattan Distance: {self.total_manhattan_distance()}\n")

    def __str__(self):
        indices = [1,2,3,8,0,4,7,6,5] # Since the puzzle positions are in a spiral, we need to print them in a different order to make them appear correctly
        output = "="*7 + "\n"
        for real_position,index in enumerate(indices): 
            # real_position is where on the physical puzzle to display the puzzle piece. Here we're just using it to keep track of where on the physical puzzle we're printing.
            square = self.state[index] # The number to display
            if real_position in [3,6]: # Next line
                output += "|\n"
            output += f"|{square if square!=0 else ' '}"
        return output + "|\n" +"="*7 # Gotta include that last border
    
if __name__=="__main__":
    toy = Puzzle()
    print(toy)
    toy.set_state("412367580")
    print(toy)
    print(toy.count_inversions())
    toy.move_sequence("76540678065406540654065406540654065408760456780")
    print(toy)
    # toy.shuffle()
    # print(toy)
    # print(toy.count_inversions())
    # print(toy.get_unsolved_pieces())

    # toy.set_state("628345071")
    # print(toy)
    # toy.move_sequence("02180")
    # print(toy)

    # toy.set_state("081325674")
    # toy.shuffle()
    # print(toy)
    # print(f"Hamming Distance: {toy.get_unsolved_pieces()}")
    # print(f"Total Manhattan Distance: {toy.total_manhattan_distance()}")
    # print(f"Nilsson's Sequence Score: {toy.nilsson_score()}")
    # print(toy.get_manhattan_distance(2))



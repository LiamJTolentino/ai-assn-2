from puzzle import *
from Solver import *
import sys
import pandas as pd

if __name__=='__main__':
    print('hi')
    try:
        num_scrambles = sys.argv[1]
    except:
        num_scrambles = 10

    # Create each solver
    UCS = Solver()
    BFS = Solver('BFS')
    ASTAR = Solver('A')

    # Create the puzzle that will be used to generate scrambled puzzles
    Scrambler = Puzzle()
    scrambles = []
    for i in range(num_scrambles):
        Scrambler.shuffle()
        scrambles.append(Scrambler.get_state_str())

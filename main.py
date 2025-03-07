from puzzle import *
from Solver import *
import sys
import pandas as pd
from time import time_ns

def run_test(alg,scramble):
    """Solves a scramble with the given Solver object and returns the number of nodes visited and the time in nanoseconds taken to solve the puzzle"""
    start = time_ns()
    alg.solve(scramble)
    end = time_ns()
    elapsed = end - start
    return len(alg.visited),elapsed

if __name__=='__main__':
    print('hi')
    try:
        num_scrambles = int(sys.argv[1])
    except:
        num_scrambles = 10

    data = pd.DataFrame({
        "Scramble" : [],
        "Nodes UCS" : [],
        "Time UCS" : [],
        "Nodes BFS" : [],
        "Time BFS" : [],
        "Nodes A*" : [],
        "Time A*" : []
    })

    print(data)

    # Create each solver
    UCS = Solver()
    BFS = Solver('BFS')
    ASTAR = Solver('A')

    # Create the puzzle that will be used to generate scrambled puzzles
    Scrambler = Puzzle()
    scrambles = []
    print(f"Now generating {num_scrambles} unique scrambled puzzles...")
    for i in range(num_scrambles):
        Scrambler.shuffle()
        print(f"Generated the puzzle:\n{Scrambler}")
        scrambles.append(Scrambler.get_state_str())

    print("Successfully generated the scrambles")
    # Test each scramble with each algorithm and record the data
    for scramble in scrambles:
        n_UCS,t_UCS = run_test(UCS,scramble)
        n_BFS,t_BFS = run_test(BFS,scramble)
        n_A,t_A = run_test(ASTAR,scramble)

        # Create row of data
        new_row = pd.Series({
            "Scramble" : scramble,
            "Nodes UCS" : n_UCS,
            "Time UCS" : t_UCS,
            "Nodes BFS" : n_BFS,
            "Time BFS" : t_BFS,
            "Nodes A*" : n_A,
            "Time A*" : t_A
        })
        data.loc[len(data)] = new_row

    data.to_csv("Tests.csv")


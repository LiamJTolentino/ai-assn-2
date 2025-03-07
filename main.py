from puzzle import *
from Solver import *
import sys
import pandas as pd
from time import time_ns
import matplotlib.pyplot as plt

def run_test(alg,scramble):
    """Solves a scramble with the given Solver object and returns the number of nodes visited and the time in milliseconds taken to solve the puzzle"""
    start = time_ns()/1000000
    alg.solve(scramble)
    end = time_ns()/1000000
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
    print(f"Now generating {num_scrambles} unique scrambled puzzles...")
    for i in range(num_scrambles):
        Scrambler.shuffle()
        print(f"Solving the puzzle:\n{Scrambler}")

        scramble = Scrambler.get_state_str()

        n_UCS,t_UCS = run_test(UCS,scramble)
        print(f"UCS solved the puzzle in {t_UCS:.3f}ms and visited {n_UCS} nodes")
        n_BFS,t_BFS = run_test(BFS,scramble)
        print(f"BFS solved the puzzle in {t_BFS:.3f}ms and visited {n_BFS} nodes")
        n_A,t_A = run_test(ASTAR,scramble)
        print(f"A* solved the puzzle in {t_A:.3f}ms and visited {n_A} nodes")

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

    print("==================\n" + 
          "--Final Results--\n" +
          "==================")
    for alg in ["UCS","BFS","A*"]:
        node_data = data[f"Nodes {alg}"]
        time_data = data[f"Time {alg}"]
        print(f"\n{alg}:")
        print("\tNumber of Nodes visited:")
        print(f"\t\tWorst: {node_data.max()}")
        print(f"\t\tBest: {node_data.min()}")
        print(f"\t\tAverage: {node_data.mean()}")

        print("\tTime taken to solve:")
        print(f"\t\tWorst: {time_data.max():.3f}ms")
        print(f"\t\tBest: {time_data.min():.3f}ms")
        print(f"\t\tAverage: {time_data.mean():.3f}ms")
        
    data.to_csv("Tests.csv")


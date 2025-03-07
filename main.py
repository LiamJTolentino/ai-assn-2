from puzzle import *
from Solver import *
import sys
import pandas as pd
from time import time_ns
import matplotlib.pyplot as plt
import numpy as np

def run_test(alg,scramble):
    """Solves a scramble with the given Solver object and returns the number of nodes visited and the time in milliseconds taken to solve the puzzle"""
    start = time_ns()/1000000
    alg.solve(scramble)
    end = time_ns()/1000000
    elapsed = end - start
    return len(alg.visited),elapsed

# This function was mostly AI generated, but that's mainly because I suck with matplotlib
def plot_distributions(df, prefix, title,units):
    """Generates a distribution graph for a specific set of columns

    Args:
        df (DataFrame): DataFrame containing the data
        prefix (str): Prefix of the column name representing what data is stored there (Nodes or Time)
        title (str): Title displayed at the top of the graph
        units (str): Units of the column in question
    """
    # Filter columns based on prefix
    columns = [col for col in df.columns if col.startswith(prefix)]
    
    # Calculate means and standard deviations
    means = df[columns].mean()
    stds = df[columns].std()
    
    # Plot histograms and bell curves
    plt.figure(figsize=(12, 8))
    colors = ['#395c78', '#9d312f', '#f08149']  # Hex colors for each algorithm

    for i, column in enumerate(columns):
        # Plot histogram
        plt.hist(df[column], bins=30, alpha=0.5, color=colors[i], density=True, label=f'{column} Histogram')
        
        # Plot bell curve
        x = np.linspace(df[column].min(), df[column].max(), 1000)
        y = (1 / (stds[column] * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - means[column]) / stds[column])**2)
        plt.plot(x, y, color=colors[i], linestyle='dashed', linewidth=2, label=f'{column} Bell Curve')

    # Add labels and title
    plt.xlabel(f'Value ({units})')
    plt.ylabel('Density')
    plt.title(title)
    plt.legend()

    # Add a text box with means and standard deviations
    textstr = '\n'.join([f'{col.replace(prefix,"")}:\n  μ={means[col]:.2f}, σ={stds[col]:.2f}\n  Best: {df[col].min()}\n  Worst: {df[col].max()}' for col in columns])
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.text(0.05, 0.95, textstr, transform=plt.gca().transAxes, fontsize=10,
             verticalalignment='top', bbox=props)

    # Show the plot
    plt.show()

if __name__=='__main__':
    print('hi')
    random.seed(10)
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
        
    # Matplotlib stuff

    plot_distributions(data,"Nodes","Distribution of the Number of Nodes Visited by Each Algorithm","Nodes")
    plot_distributions(data,"Time","Distribution of Time Taken to solve with each algorithm","ms")
        
    data.to_csv("Tests.csv")


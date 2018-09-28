from Pathfinder import *
from MazeProblem import *
from SearchTreeNode import *

maze = ["XXXXXXX",
        "X.....X",
        "X.M.MMX",
        "X...M.X",
        "XXXXXXX"]
problem = MazeProblem(maze)
initial = (5, 1)
goals = [(5, 3), (1, 3), (1, 1)]


print(A_Star(problem, initial, goals[1]))

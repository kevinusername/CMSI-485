# Kevin Peters
"""
The Pathfinder class is responsible for finding a solution (i.e., a
sequence of actions) that takes the agent from the initial state to all
of the goals with optimal cost.

This task is done in the solve method, as parameterized
by a maze pathfinding problem, and is aided by the SearchTreeNode DS.
"""

from MazeProblem import MazeProblem
from SearchTreeNode import SearchTreeNode
import unittest
from queue import PriorityQueue
import numpy
from itertools import permutations


def generate_path(node):
    """Follows a node's parent tree to generate the path it took

    :param node: node whose parents should be looked up
    :return:Path of actions taken to reach notes state ("U","D","L","R")
    """
    solution = [node.action]

    parent_node = node.parent

    while parent_node.action is not None:
        solution.append(parent_node.action)
        parent_node = parent_node.parent

    solution.reverse()

    return solution


def h(state, goal):
    """Manhattan Distance Heuristic between 2 points

    :param state: starting state
    :param goal: ending state
    :return: score from heuristic
    """
    return abs(goal[1] - state[1]) + abs(goal[0] - state[0])


def a_star(problem, initial, goal):
    """Uses an A* search to find the optimal path between 2 points

    :param problem: maze problem
    :param initial: starting state
    :param goal: final state
    :return: (totalCost, path)
    """
    frontier = PriorityQueue(maxsize=0)
    graveyard = set()

    # Put initial state in queue
    frontier.put_nowait(SearchTreeNode(
        initial, None, None, 0, h(initial, goal)))

    while not frontier.empty():

        current = frontier.get_nowait()  # node with lowest h(n) + g(n) score
        graveyard.add(current)

        # If it satisfies the goal, return its path/solution
        if current.state == goal:
            return current.totalCost, generate_path(current)

        # Add adjacent nodes that have not already been visited to queue
        for neighbor in problem.transitions(current.state):
            if neighbor[2] not in graveyard:
                new_node = SearchTreeNode(neighbor[2], neighbor[0], current, current.totalCost + neighbor[1],
                                          h(neighbor[2], goal))

                frontier.put_nowait(new_node)

    return None


def reverse_path(path):
    """Gives the reverse of an input put. All instructions flipped and order flipped

    :param path: path to reverse
    :return: reversed path
    """
    reverse_dictionary = {"D": "U", "U": "D", "L": "R", "R": "L"}
    new_path = []

    for step in path:
        new_path.append(reverse_dictionary[step])

    new_path.reverse()

    return new_path


def solve(problem, initial, goals):
    """Uses A* to create a cost matrix that is used to evaluate a TSP like problem

    :param problem: maze
    :param initial: starting state
    :param goals: all goals to reach
    :return: optimal path
    """
    key_states = [initial] + goals
    length = len(key_states)  # Don't need to compute a bunch

    cost_matrix = numpy.zeros((length, length), object)  # Stores A* cost and path for any 2 points

    # Fill in the cost matrix with A* results
    for y in range(length - 1):
        for x in range(y + 1, length):
            if x != y:  # Ignore state traveling to itself
                cost_matrix[x][y] = a_star(problem, key_states[x], key_states[y])  # A* result between 2 points
                if cost_matrix[x][y] is None:  # If a state can't be reached, return None for the path
                    return None
                # Infer the bottom half of the matrix by reversing the path of the top half
                cost_matrix[y][x] = (cost_matrix[x][y][0], reverse_path(cost_matrix[x][y][1]))

    # All possible orders of goals, always starting at initial
    all_permutations = [perm for perm in permutations(key_states) if perm[0] == key_states[0]]

    index_dictionary = {}  # Dictionary so that the cost_matrix can be called upon using a goal as index
    for state in key_states:
        index_dictionary[state] = key_states.index(state)

    all_costs = []  # A list meant to parallel the all_permutations list, holding each perms respective cost

    # Generate the cost for each permutation and store it in all_costs
    for perm in all_permutations:
        total_cost = 0
        for s in range(length - 1):
            total_cost += cost_matrix[index_dictionary[perm[s]]][index_dictionary[perm[s + 1]]][0]
        all_costs.append(total_cost)

    optimal_perm = all_permutations[all_costs.index(min(all_costs))]  # A permutation with the lowest cost
    final_path = []

    # Compile the path for this permutation using the cost_matrix
    for s in range(length - 1):
        final_path += cost_matrix[index_dictionary[optimal_perm[s]]][index_dictionary[optimal_perm[s + 1]]][1]

    return final_path


class PathfinderTests(unittest.TestCase):

    def test_maze1(self):
        maze = ["XXXXXXX",
                "X.....X",
                "X.M.M.X",
                "X.X.X.X",
                "XXXXXXX"]
        problem = MazeProblem(maze)
        initial = (1, 3)
        goals = [(5, 3)]
        solve(problem, initial, goals)

        soln = solve(problem, initial, goals)
        (soln_cost, is_soln) = problem.soln_test(soln, initial, goals)
        self.assertTrue(is_soln)
        self.assertEqual(soln_cost, 8)

    def test_maze2(self):
        maze = ["XXXXXXX",
                "X.....X",
                "X.M.M.X",
                "X.X.X.X",
                "XXXXXXX"]
        problem = MazeProblem(maze)
        initial = (1, 3)
        goals = [(3, 3), (5, 3)]
        soln = solve(problem, initial, goals)
        (soln_cost, is_soln) = problem.soln_test(soln, initial, goals)
        self.assertTrue(is_soln)
        self.assertEqual(soln_cost, 12)

    def test_maze3(self):
        maze = ["XXXXXXX",
                "X.....X",
                "X.M.MMX",
                "X...M.X",
                "XXXXXXX"]
        problem = MazeProblem(maze)
        initial = (5, 1)
        goals = [(5, 3), (1, 3), (1, 1)]
        soln = solve(problem, initial, goals)
        (soln_cost, is_soln) = problem.soln_test(soln, initial, goals)
        self.assertTrue(is_soln)
        self.assertEqual(soln_cost, 12)

    def test_maze4(self):
        maze = ["XXXXXXX",
                "X.....X",
                "X.M.XXX",
                "X...X.X",
                "XXXXXXX"]
        problem = MazeProblem(maze)
        initial = (5, 1)
        goals = [(5, 3), (1, 3), (1, 1)]
        soln = solve(problem, initial, goals)
        self.assertTrue(soln == None)

    def test_maze5(self):
        # Big boi test. Confirms that empirically, scales exactly as O(n!) should
        maze = ["XXXXXXXXXXXXXXXXXX",
                "X****************X",
                "X****************X",
                "X****************X",
                "X****************X",
                "X****************X",
                "X****************X",
                "X****************X",
                "XXXXXXXXXXXXXXXXXX"]
        problem = MazeProblem(maze)
        initial = (3, 1)
        goals = [(1, 5), (2, 5), (5, 4), (1, 7), (5, 5), (1, 6), (2, 2), (6, 2), (5, 1), (3, 3)]
        soln = solve(problem, initial, goals)
        (soln_cost, is_soln) = problem.soln_test(soln, initial, goals)
        print(soln)
        self.assertTrue(is_soln)


if __name__ == '__main__':
    unittest.main()

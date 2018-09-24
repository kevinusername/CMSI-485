'''
The Pathfinder class is responsible for finding a solution (i.e., a
sequence of actions) that takes the agent from the initial state to all
of the goals with optimal cost.

This task is done in the solve method, as parameterized
by a maze pathfinding problem, and is aided by the SearchTreeNode DS.
'''

from MazeProblem import MazeProblem
from SearchTreeNode import SearchTreeNode
import unittest
from queue import PriorityQueue


def generate_path(node):
    solution = []
    solution.append(node.action)

    parentNode = node.parent

    while (parentNode.action != None):
        solution.append(parentNode.action)
        parentNode = parentNode.parent

    solution.reverse()

    return solution


def h(state, goal):
    return abs(goal[1] - state[1]) + abs(goal[0] - state[0])


def solve(problem, initial, goals):
    frontier = PriorityQueue(maxsize=0)
    graveyard = set()

    # Put initial state in queue
    frontier.put_nowait(
        (0, SearchTreeNode(initial, None, None, 0, h(initial, goals[0]))))

    while not frontier.empty():
        current = frontier.get_nowait()[1]

        if current.state == goals[0]:
            return generate_path(current)

        for neighbor in problem.transitions(current.state):
            new_node = SearchTreeNode(neighbor[2], neighbor[0], current, current.totalCost + neighbor[1],
                                      h(neighbor[2], goals[0]))

            if neighbor[2] not in graveyard:
                frontier.put_nowait(
                    ((new_node.totalCost + new_node.heuristicCost), new_node))


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


if __name__ == '__main__':
    unittest.main()

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


# Same code from Classwork #1
def generate_path(node):
    solution = []
    solution.append(node.action)

    parentNode = node.parent

    while (parentNode.action != None):
        solution.append(parentNode.action)
        parentNode = parentNode.parent

    solution.reverse()

    return solution


def h(state, goals):
    score = []
    for goal in goals:
        score.append(abs(goal[1] - state[1]) + abs(goal[0] - state[0]))
    return min(score)


def solve(problem, initial, goals):
    frontier = PriorityQueue(maxsize=0)
    graveyard = set()

    # Put initial state in queue
    # 3-tuple format for queue objects: (h(node)+g(node), arbitrary tie-break value, node)
    frontier.put_nowait(
        (0, 0, SearchTreeNode(initial, None, None, 0, h(initial, goals))))

    # An int to handle when multiple nodes score the same h(n) + g(n) value
    # Due to the way Python handles PriorityQueues, this is necessary to avoid
    # attempting to compare nodes, which results in an error that terminates program
    tie_breaker = 1

    while not frontier.empty():

        # node with lowest h(n) + g(n) score
        current = frontier.get_nowait()[2]
        graveyard.add(current.state)

        # If it satisfies the goal, return its path/solution
        if current.state in goals:
            graveyard.clear()
            graveyard.add(current.state)
            goals.remove(current.state)
            frontier = PriorityQueue(maxsize=0)

        if not goals:
            return generate_path(current)

        # Add adjacent nodes that have not already been visited to queue
        for neighbor in problem.transitions(current.state):
            if neighbor[2] not in graveyard:
                new_node = SearchTreeNode(neighbor[2], neighbor[0], current, current.totalCost + neighbor[1],
                                          h(neighbor[2], goals))

                frontier.put_nowait((new_node.totalCost + new_node.heuristicCost, tie_breaker, new_node))
                # Increase to ensure nodes are never compared by queue
                tie_breaker += 1

    return None


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
        print(soln)
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
        print(soln)
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

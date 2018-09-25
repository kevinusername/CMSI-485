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


# Same code from Classwork #1
# Follows a nodes parents until reaching the initial node
# Returns list of actions each node took
def generate_path(node):
    solution = [node.action]

    parent_node = node.parent

    while parent_node.action is not None:
        solution.append(parent_node.action)
        parent_node = parent_node.parent

    solution.reverse()

    return solution


# Returns Manhattan Distance heuristic score for CLOSEST goal
def h(state, goals):
    score = []
    for goal in goals:
        score.append(abs(goal[1] - state[1]) + abs(goal[0] - state[0]))
    return min(score)


def solve(problem, initial, goals):
    frontier = PriorityQueue(maxsize=0)  # queue with no maxsize that pops node with lowest h(n) + g(n) value
    graveyard = set()  # set of all visited states

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

        # when a goal is reached, reset the graveyard and frontier, remove goal from goals
        if current.state in goals:
            graveyard = {current.state}  # new graveyard with only current state
            goals.remove(current.state)
            frontier = PriorityQueue(maxsize=0)  # New empty frontier

        # If there are no more goals to search for, return the current node's path
        if not goals:
            return generate_path(current)

        # Add adjacent nodes that have not already been visited to queue
        for neighbor in problem.transitions(current.state):
            if neighbor[2] not in graveyard:
                new_node = SearchTreeNode(neighbor[2], neighbor[0], current, current.totalCost + neighbor[1],
                                          h(neighbor[2], goals))

                frontier.put_nowait((new_node.totalCost + new_node.heuristicCost, tie_breaker, new_node))
                # Increase to ensure nodes objects are never compared by queue
                tie_breaker += 1

    # If this point is reached, there is no path
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

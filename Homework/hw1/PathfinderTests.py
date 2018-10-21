import unittest
from Pathfinder import solve
from Pathfinder import a_star
from MazeProblem import MazeProblem

class PathfinderTests(unittest.TestCase):
    
    def test_maze1(self):
        maze = ["XXXXXXX",
                "X.....X",
                "X.M.M.X",
                "X.X.X.X",
                "XXXXXXX"]
        problem = MazeProblem(maze)
        initial = (1, 3)
        goals   = [(5, 3)]
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
        goals   = [(3, 3), (5, 3)]
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
        goals   = [(5, 3), (1, 3), (1, 1)]
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
        goals   = [(5, 3), (1, 3), (1, 1)]
        soln = solve(problem, initial, goals)
        self.assertTrue(soln is None)
        
    def test_maze5(self):
                #0123456789
        maze = ["XXXXXXXXXX", #0
                "X........X", #1
                "X..MMMMXXX", #2
                "X..M..M..X", #3
                "XXXM..M..X", #4
                "X..M..M..X", #5
                "XXXXXXXXXX"] #6
        problem = MazeProblem(maze)
        initial = (1, 1)
        goals   = [(8, 1), (1, 3), (8, 3), (8, 5), (1, 5)]
        soln = solve(problem, initial, goals)
        (soln_cost, is_soln) = problem.soln_test(soln, initial, goals)
        self.assertTrue(is_soln)
        self.assertEqual(soln_cost, 34)
        
    def test_maze6(self):
                #0123456789
        maze = ["XXXXXXXXXX", #0
                "X........X", #1
                "X..MMMMXXX", #2
                "X..M..M..X", #3
                "XXXM..M..X", #4
                "X..X..M..X", #5
                "XXXXXXXXXX"] #6
        problem = MazeProblem(maze)
        initial = (1, 1)
        goals   = [(8, 1), (1, 3), (8, 3), (8, 5), (1, 5)]
        soln = solve(problem, initial, goals)
        self.assertTrue(soln is None)
    
    def test_maze7(self):
                #          11111111112
                #012345678901234567890
        maze = ["XXXXXXXXXXXXXXXXXXXXX", #0
                "X..X....M....X..M.X.X", #1
                "X...X..M.M..M..MM..MX", #2
                "XMM..XMMMMM..X....X.X", #3
                "X..M..X.........M...X", #4
                "XX.......XX.XXMXXMM.X", #5
                "X.XXX.MM....X...X...X", #6
                "X...X.MM....M.XX..XXX", #7
                "XXM.X..MMMMMX..M..X.X", #8
                "X.X.........X..M....X", #9
                "XXXXXXXXXXXXXXXXXXXXX"] #10
        problem = MazeProblem(maze)
        initial = (10, 4)
        goals   = [(1, 1), (19, 1), (19, 8), (1, 9)]
        soln = solve(problem, initial, goals)
        self.assertTrue(soln is None)
    
    def test_maze8(self):
                #          11111111112
                #012345678901234567890
        maze = ["XXXXXXXXXXXXXXXXXXXXX", #0
                "X..X....M....X..M.X.X", #1
                "X...X..M.M..M..MM..MX", #2
                "XMM..XMMMMM..X....X.X", #3
                "X..M..X.........M...X", #4
                "XX.......XX.XXMXXMM.X", #5
                "X.XXX.MM....X...X...X", #6
                "X...X.MM....M.XX..XXX", #7
                "XXM.X..MMMMMX..M..X.X", #8
                "X.X.........X..M....X", #9
                "XXXXXXXXXXXXXXXXXXXXX"] #10
        problem = MazeProblem(maze)
        initial = (10, 4)
        goals   = [(1, 1), (19, 1), (19, 8), (1, 6)]
        soln = solve(problem, initial, goals)
        (soln_cost, is_soln) = problem.soln_test(soln, initial, goals)
        self.assertTrue(is_soln)
        self.assertEqual(soln_cost, 79)
        
    def test_maze9(self):
                #          11111111112
                #012345678901234567890
        maze = ["XXXXXXXXXXXXXXXXXXXXX", #0
                "X..X....M....X..M.X.X", #1
                "X...X..M.M..M..MM..MX", #2
                "XMM..XMMMMM..X....X.X", #3
                "X..M..X.........M...X", #4
                "XX.......XX.XXMXXMM.X", #5
                "X.XXX.MM....X...X...X", #6
                "X...X.MM....M.XX..XXX", #7
                "XXM.X..MMMMMX..M..X.X", #8
                "X.X.........X..M....X", #9
                "XXXXXXXXXXXXXXXXXXXXX"] #10
        problem = MazeProblem(maze)
        initial = (1, 1)
        goals   = [(8, 2), (1, 4), (4, 1), (12, 2), (18, 2), (1, 6), (6, 8), (8, 7), (13, 6), (1, 9)]
        soln = solve(problem, initial, goals)
        self.assertTrue(soln is None)
    
    def test_maze10(self):
                #          11111111112
                #012345678901234567890
        maze = ["XXXXXXXXXXXXXXXXXXXXX", #0
                "X..X....M....X..M.X.X", #1
                "X...X..M.M..M..MM..MX", #2
                "XMM..XMMMMM..X....X.X", #3
                "X..M..X.........M...X", #4
                "XX.......XX.XXMXXMM.X", #5
                "X.XXX.MM....X...X...X", #6
                "X...X.MM....M.XX..XXX", #7
                "XXM.X..MMMMMX..M..X.X", #8
                "X.X.........X..M....X", #9
                "XXXXXXXXXXXXXXXXXXXXX"] #10
        problem = MazeProblem(maze)
        initial = (1, 1)
        goals   = [(8, 2), (1, 4), (4, 1), (12, 2), (18, 2), (1, 6), (6, 8), (8, 7), (13, 6), (19, 8)]
        soln = solve(problem, initial, goals)
        (soln_cost, is_soln) = problem.soln_test(soln, initial, goals)
        self.assertTrue(is_soln)
        self.assertEqual(soln_cost, 93)
    

if __name__ == '__main__':
    unittest.main()

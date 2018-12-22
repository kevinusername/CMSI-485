# Kevin Peters & Michael Simmons
'''
ad_engine.py

CMSI 485 HW 3: Advertisement engine that selects from two
ad traits to maximize expected utility of converting a sale
for the Forney Industries Protectron 3001
'''

import itertools
import unittest
import math
import numpy as np
from pomegranate import *


class AdEngine:

    def __init__(self, data_file, structure, dec_vars, util_map):
        data = np.genfromtxt(data_file, dtype=int,
                             delimiter=',', names=True)
        self.names = data.dtype.names
        self.BN = BayesianNetwork.from_structure(
            data.view((int, len(data.dtype.names))), structure, None, 0, None, self.names)
        self.dec_vars = dec_vars
        self.dec_var_values = [list(np.unique(data[v])) for v in dec_vars]
        self.util_map = util_map
        return

    def decide(self, evidence):
        best_combo, best_util = None, -math.inf

        # I feel that this line is sinful in length for what it does
        util_location = self.names.index(list(self.util_map.keys())[0])

        possible_combos = itertools.product(*self.dec_var_values)

        for combo in possible_combos:
            util = 0
            actions = {}

            for x in range(0, len(self.dec_vars)):
                actions[self.dec_vars[x]] = combo[x]

            a_and_e = actions.copy()
            a_and_e.update(evidence)
            state_probability = self.BN.predict_proba(a_and_e)[util_location]

            for s in state_probability.parameters[0]:
                util += state_probability.parameters[0][s] * \
                    self.util_map[list(self.util_map.keys())[0]][s]

            if util > best_util:
                best_util = util
                best_combo = actions

        return best_combo


class AdEngineTests(unittest.TestCase):
    def test_defendotron_ad_engine(self):
        engine = AdEngine(
            data_file='hw3_data.csv',
            dec_vars=["Ad1", "Ad2"],
            structure=((), (), (0, 9,), (6,), (0, 1,),
                       (1, 8,), (), (2, 5,), (), ()),
            util_map={'S': {0: 0, 1: 5000, 2: 17760}}
        )
        self.assertEqual(engine.decide({"T": 1}), {"Ad1": 0, "Ad2": 1})
        self.assertIn(engine.decide({"F": 1}), [
                      {"Ad1": 1, "Ad2": 0}, {"Ad1": 1, "Ad2": 1}])
        self.assertEqual(engine.decide({"G": 1, "T": 0}), {"Ad1": 1, "Ad2": 1})

    def test_defendotron_ad_engine_t2(self):
        engine = AdEngine(
            data_file='hw3_data.csv',
            dec_vars=["Ad1"],
            structure=((), (), (0, 9,), (6,), (0, 1,),
                       (1, 8,), (), (2, 5,), (), ()),
            util_map={'S': {0: 0, 1: 5000, 2: 17760}}
        )
        self.assertEqual(engine.decide({"A": 1}), {"Ad1": 0})
        self.assertEqual(engine.decide({"P": 1, "A": 0}), {"Ad1": 1})
        self.assertIn(engine.decide({"A": 1, "G": 0, "T": 1}), [
                      {"Ad1": 0}, {"Ad1": 1}])


if __name__ == "__main__":
    unittest.main()

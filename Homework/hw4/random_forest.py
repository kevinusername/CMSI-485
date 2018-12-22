#Code written by Kevin Peters, Michael Simmons, Michael West, Nikky Rajavasireddy, Blake Crowther
import numpy as np
from sklearn.ensemble import RandomForestClassifier

from PreProcess import PreProcess


class random_forest:
    def __init__(self, data):
        self.forest = RandomForestClassifier(n_estimators=100)
        self.cutoff = data.shape[1] - 1
        self.forest.fit(data[:, 0:self.cutoff], np.asarray(
            data[:, self.cutoff], int), None)

    def test_score(self, test_data):
        return self.forest.score(test_data[:, 0:self.cutoff], test_data[:, self.cutoff], None)


data = PreProcess('income-training.csv', True).fitted_data
test_data = PreProcess('income-test.csv', False).fitted_data

forest = random_forest(data)
print(forest.test_score(test_data))

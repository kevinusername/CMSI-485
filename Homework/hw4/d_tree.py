#Code written by Kevin Peters, Michael Simmons, Michael West, Nikky Rajavasireddy, Blake Crowther
import numpy as np
from sklearn.tree import DecisionTreeClassifier

from PreProcess import PreProcess


class d_tree:
    def __init__(self, data):
        self.dtree = DecisionTreeClassifier(criterion='entropy')
        self.cutoff = data.shape[1] - 1
        self.dtree.fit(data[:, 0:self.cutoff],
                       np.asarray(data[:, self.cutoff], int))

    def test_score(self, test_data):
        return self.dtree.score(test_data[:, 0:self.cutoff], test_data[:, self.cutoff])


data = PreProcess('income-training.csv', True).fitted_data
test_data = PreProcess('income-test.csv', False).fitted_data

tree = d_tree(data)
print(tree.test_score(test_data))

#Code written by Kevin Peters, Michael Simmons, Michael West, Nikky Rajavasireddy, Blake Crowther
from PreProcess import PreProcess
from sklearn.naive_bayes import MultinomialNB
import numpy as np


class naive_bayes:
    def __init__(self, data):
        self.cutoff = data.shape[1] - 1
        self.clf = MultinomialNB()
        self.clf.fit(data[:, 0:self.cutoff],
                     np.asarray(data[:, self.cutoff], int))

    def test_score(self, test_data):
        return self.clf.score(test_data[:, 0:self.cutoff], test_data[:, self.cutoff])


data = PreProcess('income-training.csv', True).fitted_data
test_data = PreProcess('income-test.csv', False).fitted_data

nbc = naive_bayes(data)
print(nbc.test_score(test_data))

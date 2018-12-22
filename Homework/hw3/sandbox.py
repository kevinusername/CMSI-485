import numpy
from pomegranate import *
import itertools


# data = numpy.genfromtxt('hw4_data.csv', dtype=int,
#                         delimiter=',', names=True)

# print(numpy.unique(data['P']))

combos = [[0, 1], [0, 1]]

print(list(itertools.product(*combos)))


# tuple_tuple = ((), (), (0, 9,), (6,), (0, 1,),
#                (1, 8,), (), (2, 5,), (), ())

# BN = BayesianNetwork.from_structure(
#     data.view((int, len(data.dtype.names))), tuple_tuple, None, 0, None, data.dtype.names)

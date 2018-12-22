#Code written by Kevin Peters, Michael Simmons, Michael West, Nikky Rajavasireddy, Blake Crowther
import numpy as np
import pandas as desiigner
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder


class PreProcess:

    def __init__(self, dataFile, training):
        self.data = self.read_file(dataFile)
        self.bin_continous()

        if training:
            self.impute_missing()

        self.fitted_data = self.encode_data()

    def read_file(self, dataFile):
        names = ['Age', 'Work Class', 'Education', 'Education-num', 'Maritial Status', 'Occupation Code',
                 'Relationship', 'Race', 'Sex', 'Capital Gain', 'Capital Loss', 'Hours', 'Native Country', 'Income']

        dtype_map = {'Age': int, 'Work Class': str, 'Education': str, 'Education-num': int, 'Maritial Status': str, 'Occupation Code': str,
                     'Relationship': str, 'Race': str, 'Sex': str, 'Capital Gain': int, 'Capital Loss': int, 'Hours': int, 'Native Country': str, 'Income': str}

        return desiigner.read_csv(dataFile, header=None, names=names, dtype=dtype_map)

    def encode_data(self):
        est = OrdinalEncoder(dtype=int, categories='auto')
        est.fit(self.data)

        col_trans = ColumnTransformer([
            ('Age-passthrough', 'passthrough', [0]),
            ('EDU', est, [1, 2]),
            ('edu-years-passthrough', 'passthrough', [3]),
            ('mid-features', est, [4, 5, 6, 7, 8]),
            ('gain-pass', 'passthrough', [9]),
            ('loss-drop', 'drop', [10]),
            ('hours-passthrough', 'passthrough', [11]),
            ('final-features', est, [12, 13])
        ])

        return col_trans.fit_transform(self.data)

    def bin_continous(self):
        def bin_age(age):
            if age == " ?":
                return age
            elif age <= 22:
                return 0
            elif age > 22 and age <= 35:
                return 1
            elif age > 35 and age <= 65:
                return 2
            else:
                return 3

        def bin_years(years):
            if years < 9:
                return 0
            elif years == 9:
                return 1
            elif years > 9 and years <= 13:
                return 2
            else:
                return 3

        def bin_hours(hours):
            if hours < 20:
                return 0
            elif hours >= 20 and hours < 40:
                return 1
            elif hours >= 40 and hours <= 50:
                return 2
            else:
                return 3

        def bin_capital_gain(gain):
            if gain < 7000:
                return 0
            else:
                return 1


        self.data['Age'] = list(map(bin_age, self.data['Age']))
        self.data['Education-num'] = list(map(bin_years,
                                              self.data['Education-num']))
        self.data['Hours'] = list(map(bin_hours, self.data['Hours']))
        self.data['Capital Gain'] = list(
            map(bin_capital_gain, self.data['Capital Gain']))
        
    def impute_missing(self):
        imp = SimpleImputer(missing_values=" ?", strategy="most_frequent")
        self.data = imp.fit_transform(self.data)


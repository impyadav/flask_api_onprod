"""
# -*- coding: utf-8 -*-

Created on Aug 2023
@author: Prateek Yadav

"""
import numpy as np

np.random.seed(101)


class onlinePred:
    """
    Inference class moudle, Implementaion for online Prediction.
    """

    def __init__(self, ip_string):
        self.ip_string = ip_string

    def inference(self):
        """
        Takes a sentence as an input and return a numpy array of 500 random number (Generated from Gaussian Dist.
        :return:
        """
        return np.random.randn(500)

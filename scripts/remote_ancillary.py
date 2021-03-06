#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 14:56:41 2018

@author: Harshvardhan
"""
import warnings

import numpy as np
import pandas as pd
from numba import jit, prange

warnings.simplefilter("ignore")


def get_stats_to_dict(a, *b):
    df = pd.DataFrame(list(zip(*b)), columns=a)
    dict_list = df.to_dict(orient='records')

    return dict_list


def return_uniques_and_counts(df):
    """Return unique-values of the categorical variables and their counts
    """
    keys, count = dict(), dict()
    for index, row in df.iterrows():
        flat_list = [item for sublist in row for item in sublist]
        keys[index] = set(flat_list)
        count[index] = len(set(flat_list))

    return keys, count


@jit(nopython=True)
def remote_stats(MSE, varX_matrix_global, avg_beta_vector):
    my_shape = avg_beta_vector.shape
    ts = np.zeros(my_shape)

    for voxel in prange(my_shape[0]):
        var_covar_beta_global = MSE[voxel] * np.linalg.inv(varX_matrix_global)
        se_beta_global = np.sqrt(np.diag(var_covar_beta_global))
        ts[voxel, :] = avg_beta_vector[voxel, :] / se_beta_global

    return ts

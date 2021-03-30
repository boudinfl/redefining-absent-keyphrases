# -*- coding: utf-8 -*-

"""Compute statistical test on trec results."""

import sys
import re
import json
import numpy
from collections import defaultdict
from scipy import stats


def load_trec_results(input):
    keys, scores = [], []
    with open(input, 'r') as f:
        for line in f:
            line = line.strip()
            line = re.sub("\s+", " ", line)
            cols = line.split()
            if len(cols) == 3:
                keys.append(cols[1])
                scores.append(float(cols[2]))
    return (keys, scores)

scores_a = load_trec_results(sys.argv[1])
scores_b = load_trec_results(sys.argv[2])

assert(scores_a[0][:-1] == scores_b[0][:-1])

ttest = stats.ttest_rel(a=scores_a[1][:-1], b=scores_b[1][:-1])

# print('scoring for file: {}'.format(sys.argv[1]))
# print('all: {0:.4f}'.format(numpy.average(scores_a[1][:-1])))

# print('scoring for file: {}'.format(sys.argv[2]))
print('all: {0:.4f} (sign@.05: {1}, pvalue: {2:.4f})'.format(numpy.average(scores_b[1][:-1]), ttest[1] < .05, ttest[1]))

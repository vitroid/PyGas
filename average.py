#!/usr/bin/env python

import sys

import numpy as np

data = np.loadtxt(sys.stdin)
print(np.average(data[:, 2]))  # 第3カラム(圧縮因子)の平均値を表示

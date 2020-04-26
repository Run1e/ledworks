from math import ceil, floor, sqrt, log

import numpy as np

from pprint import pprint

"""
1 = 10**(x - 1) - 0.1
1.1 = 10**(x - 1)

"""

def clamp(min_val=0.0, max_val=1.0):
	def deco(func):
		def inner(val):
			if val <= min_val:
				return min_val
			if val >= max_val:
				return max_val
			else:
				return func(val)
		return inner
	return deco


# maps linear space to logarithmic space
@clamp()
def t(val):
	return pow(10, val * log(11) / log(10) - 1.0) - 0.1


# inverse of t
@clamp()
def r(val):
	return log(10 * val + 1) / log(11)


def log_filterbank(rate=44100, bins=128, n_fft=512, f_min=0, f_max=22050):
	max_rate = rate // 2

	min_frac = r(f_min / max_rate)
	max_frac = r(f_max / max_rate)
	delta_frac = (max_frac - min_frac) / bins
	pos = min_frac

	bin_pos = []

	for n in range(bins):
		bin_pos.append(t(pos))
		pos += delta_frac

	bin_pos.append(t(pos))

	fracs = np.array(bin_pos) * n_fft
	filter = np.array([np.zeros(n_fft + 1) for _ in range(bins)])

	for n in range(bins):
		low = fracs[n]
		high = fracs[n + 1]
		low_low = floor(low)
		low_high = ceil(low)
		high_low = floor(high)
		high_high = ceil(high)
		low_remainder = low % 1.0
		high_remainder = high % 1.0

		row = filter[n]
		row[low_low] = abs(low_remainder - 1.0)
		row[low_high:high_low + 1] = np.ones(high_low - low_high + 1)
		row[high_high] = high_remainder
		print(row)


	return filter

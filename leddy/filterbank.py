from math import ceil, floor, sqrt

import numpy as np


def log_map(value):
	return ((10 ** (2 * value) / 10 - 0.1)) / 10.0

# x = ((10^(2v) / 10 - 0.1)) / 10
# 10x = 10^(2v) / 10 - 0.1

# bins = number of output values in output array (which should be normalized logarithmically)
# fft_nums = number of values in the fft array
# f_min = lowest frequency to include in the output
# f_max = highest frequency to include in the output
# bleed = how much frequencies bleed into surrounding bins (in %)


def log_filterbank(rate=44100, bins=128, n_fft=512, f_min=0, f_max=22050, bleed=0.0):
	# lowest possible frequency is 0
	# the highest possible frequency is rate//2, so 10 maps to rate//2

	max_freq = rate // 2
	low_val = f_min / max_freq
	high_val = f_max / max_freq
	step = (high_val - low_val) / bins
	pos = low_val

	rates = [log_map(low_val)]
	for n in range(bins - 1):
		pos += step
		rates.append(log_map(pos))
	rates.append(log_map(high_val))

	fracs = np.array(rates) * n_fft
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
		#filter[n] = filter[n]

	return filter

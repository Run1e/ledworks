import numpy as np

from scipy.ndimage import gaussian_filter1d


class Sensitivity:
	"""Scales the values between 0.0-1.0 based on the largest value seen so far"""

	def __init__(self):
		self.max = 0.0

	def __call__(self, data):
		m = data.max()
		if m > self.max:
			self.max = m
			sens = m
		else:
			sens = self.max

		return data / sens


class Sustain:
	"""Sustain filters. Smoothing in the time dimension"""

	def __init__(self, factor, fps):
		self.factor = factor
		self.fps = fps
		self.value = None

	def __call__(self, delta, data):
		smoothing_factor = self.factor * delta * self.fps

		value = np.zeros(data.size) if self.value is None else self.value
		smoothed = smoothing_factor * data + (1.0 - smoothing_factor) * value
		self.value = np.fmax(smoothed, data)

		return self.value


# https://en.wikipedia.org/wiki/Exponential_smoothing
class Normalize:
	"""Adaptive normalization"""

	def __init__(self, fps, slowness=0.005, minimum=0.05):
		self.fps = fps
		self.sens = 0.0
		self.slowness = slowness
		self.minimum = minimum

	def __call__(self, delta, data):
		smoothing_factor = self.slowness * delta * self.fps

		current_max = data.max()

		proposed_max = smoothing_factor * current_max + (1.0 - smoothing_factor) * self.sens

		self.sens = max(proposed_max, current_max, self.minimum)

		return data * (1.0 / self.sens)


class Blur:
	"""Blurs the data along the first axis (preserving saturation but smoothing color differences)"""

	def __init__(self, sigma=2.0):
		self.sigma = sigma

	def __call__(self, delta, data):
		return gaussian_filter1d(data, sigma=self.sigma, axis=0)


class Mirror:
	"""Mirrors the input data, doubling the array size"""

	def __init__(self, n):
		self.n = n
		self.out = np.empty(n * 2, dtype=np.float32)

	def __call__(self, delta, data):
		out = self.out
		n = self.n
		out[:n] = data
		out[n:] = data[::-1]
		return out


class Logistic:
	def __init__(self, k, x_0):
		def logistic(x):
			return np.divide(1.0, 1.0 + np.power(np.e, -k * (x - x_0)))
		self.f = np.vectorize(logistic)

	def __call__(self, delta, data):
		return self.f(data)

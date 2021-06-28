import numpy as np


class Sensitivity:
	"""Scales the values between 0.0-1.0 based on the largest value found so far"""

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


from scipy.ndimage.filters import gaussian_filter


class Blur:
	def __init__(self, sigma=2.0):
		self.sigma = sigma

	def __call__(self, delta, data):
		return gaussian_filter(data, self.sigma, mode='nearest')


class Mirror:
	def __init__(self, n):
		self.n = n
		self.out = np.empty(n * 2, dtype=np.float32)

	def __call__(self, delta, data):
		out = self.out
		n = self.n
		out[:n] = data
		out[n:] = data[::-1]
		return out



import numpy as np

from .filter import Filter


# https://en.wikipedia.org/wiki/Exponential_smoothing
class SustainFilter(Filter):
	def __init__(self, factor):
		self.factor = factor
		self.value = None

	def setup(self, player):
		self.fps = player.fps

	def process(self, delta, data):
		smoothing_factor = self.factor * delta * self.fps

		value = np.zeros(data.size) if self.value is None else self.value
		smoothed = smoothing_factor * data + (1.0 - smoothing_factor) * value
		self.value = np.fmax(smoothed, data)

		return self.value

import numpy as np


class Intensity:
	def __init__(self):
		pass

	def __call__(self, delta, data):
		return np.repeat(data, 3).reshape(-1, 3)


class ColorIntensity:
	def __init__(self, colorf):
		self.colorf = colorf
		self.elapsed = 0.0

	def __call__(self, delta, data):
		new = np.empty((data.shape[0], 3), dtype=data.dtype)
		self.elapsed += delta

		for idx, v in enumerate(data):
			new[idx] = self.colorf(v * 0.5 + (self.elapsed * 0.1)) * v

		return new



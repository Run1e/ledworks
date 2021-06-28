import numpy as np


def fade(set, color=np.array([1.0, 1.0, 1.0], dtype=np.float32), duration=1.0):
	elapsed = 0

	def ticker(delta):
		nonlocal elapsed

		elapsed += delta

		if elapsed < duration:
			frac = (duration - elapsed) / duration
			set(color * frac)
		else:
			set(0, 0, 0)
			return True

	return ticker

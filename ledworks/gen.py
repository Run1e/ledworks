import numpy as np


def fade(set, color=np.array([1.0, 1.0, 1.0], dtype=np.float32), duration=1.0):
	_elapsed = 0

	def ticker(delta, elapsed):
		nonlocal _elapsed

		_elapsed += delta

		if _elapsed < duration:
			frac = (duration - _elapsed) / duration
			set(color * frac)
		else:
			set((0, 0, 0))
			return True

	return ticker

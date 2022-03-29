import numpy as np


def abrupt(set, intensity=1.0, duration=1.0):
	_elapsed = 0.0
	set(intensity)

	def ticker(delta, elapsed):
		nonlocal _elapsed

		_elapsed += delta

		if _elapsed >= duration:
			set(0.0)
			return True

	return ticker


def fade(set, intensity=1.0, duration=1.0):
	_elapsed = 0.0
	set(intensity)

	def ticker(delta, elapsed):
		nonlocal _elapsed

		_elapsed += delta

		if _elapsed < duration:
			frac = (duration - _elapsed) / duration
			set(intensity * frac)
		else:
			set(0.0)
			return True

	return ticker


def fade_color(set, color=np.array([1.0, 1.0, 1.0], dtype=np.float32), duration=1.0):
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

from .filter import Filter


# https://en.wikipedia.org/wiki/Exponential_smoothing
class NormalizeFilter(Filter):
	def __init__(self, slowness=0.005, minimum=0.05):
		self.sens = 0.0
		self.slowness = slowness
		self.minimum = minimum

		self.fps = None

	def setup(self, player):
		self.fps = player.fps

	def process(self, delta, data):
		smoothing_factor = self.slowness * delta * self.fps

		current_max = data.max()

		proposed_max = smoothing_factor * current_max + (1.0 - smoothing_factor) * self.sens

		self.sens = max(proposed_max, current_max, self.minimum)

		return data * (1.0 / self.sens)

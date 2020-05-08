from .filter import Filter


class SensitivityFilter(Filter):
	def __init__(self, sensitivity):
		self.sensitivity = sensitivity

	def process(self, delta, data):
		sens = self.sensitivity
		#sens = 1.0 / data.max()
		return data * sens

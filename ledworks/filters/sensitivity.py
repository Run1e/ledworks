from .filter import Filter


class SensitivityFilter(Filter):
	def __init__(self, sensitivity):
		self.max = 0.0

	def process(self, delta, data):
		m = data.max()
		if m > self.max:
			self.max = m
			sens = m
		else:
			sens = self.max

		return data / sens

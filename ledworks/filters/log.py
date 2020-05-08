from .filter import Filter
from ..filterbank import log_filterbank


class LogFilter(Filter):
	def __init__(self, bins, f_min=0, f_max=20000):
		self.bins = bins
		self.f_min = f_min
		self.f_max = f_max

		self.log = None

	def setup(self, player):
		self.log = log_filterbank(
			rate=player.rate,
			bins=self.bins,
			n_fft=player.chunk // 2,
			f_min=self.f_min,
			f_max=self.f_max
		)

	def process(self, delta, data):
		return self.log.dot(data)

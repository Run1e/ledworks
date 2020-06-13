import numpy as np

from .colorfilter import ColorFilter
from ..utils import hue


class StaticColorRangeFilter(ColorFilter):
	def setup(self, player):
		bins = player.bins

		a = np.zeros(3 * bins).reshape(bins, 3)

		for n in range(bins):
			pos = n / bins
			a[n] = np.array(hue(pos))

		self.mask = a

	def process(self, delta, data):
		return data * self.mask

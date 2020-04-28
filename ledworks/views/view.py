import numpy as np


class View:
	def __init__(self, strip):
		self.strip = strip

		self.data = np.zeros(strip.count * 3)
		self.data.resize(strip.count, 3)

	def updates(self):
		for index, (new_color, old_color) in enumerate(zip(self.strip.data, self.data)):
			if not np.all(new_color == old_color):
				self.data[index] = new_color
				yield index, new_color

	def draw(self):
		raise NotImplemented

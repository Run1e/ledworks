import numpy as np


class View:
	def set_data(self, data):
		self.data = data.copy()

	def changed(self, data):
		for index, (new_color, old_color) in enumerate(zip(data, self.data)):
			if not np.all(new_color == old_color):
				self.data[index] = new_color
				yield index, new_color

	def draw(self, data):
		raise NotImplemented

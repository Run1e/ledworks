import numpy as np


class ColorComponent:
	def __init__(self, offset):
		self.offset = offset

	def __get__(self, instance, owner):
		return instance.data[self.offset]

	def __set__(self, instance, value):
		instance.data[self.offset] = value


class LEDContext:
	r = ColorComponent(0)
	g = ColorComponent(1)
	b = ColorComponent(2)

	def __init__(self, index, data):
		self.index = index
		self.data = data

		self.needs_prep = True
		self.started_at = None
		self.elapsed = None
		self.delta = None

	def prep(self, now):
		self.needs_prep = False
		self.started_at = now
		self.elapsed = 0.0

	def set_delta(self, delta):
		self.delta = delta
		self.elapsed += delta

	def set(self, r, g, b):
		np.copyto(self.data, np.array([r, g, b]))

	def set_color(self, color):
		np.copyto(self.data, color)

	def off(self):
		self.set(0.0, 0.0, 0.0)

	def float(self):
		return self.data

	def int(self):
		return (self.data * 255).astype(int)

	def __repr__(self):
		return 'LEDContext({0}, {1}, {2})'.format(self.r, self.g, self.b)

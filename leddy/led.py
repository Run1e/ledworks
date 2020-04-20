class ColorComponent:
	def __init__(self, offset):
		self.offset = offset

	def __get__(self, instance, owner):
		return instance.strip_data[instance.index][self.offset]

	def __set__(self, instance, value):
		instance.strip_data[instance.index][self.offset] = value


class LEDContext:
	r = ColorComponent(0)
	g = ColorComponent(1)
	b = ColorComponent(2)

	def __init__(self, index, strip_data):
		self.index = index
		self.strip_data = strip_data

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
		array = self.strip_data[self.index]
		array[0], array[1], array[2] = r, g, b

	def off(self):
		self.set(0.0, 0.0, 0.0)

	def float(self):
		return self.strip_data[self.index]

	def int(self):
		return (self.strip_data[self.index] * 255).astype(int)

	def __repr__(self):
		return 'LEDContext({0}, {1}, {2})'.format(self.r, self.g, self.b)

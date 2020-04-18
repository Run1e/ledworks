from random import choice, randint

from .led import LEDContext


class Strip:
	def __init__(self, count):
		self.count = count
		self.data = [0.0 for _ in range(count * 3)]
		self.leds = [LEDContext(index, self.data) for index in range(count)]
		self.gens = dict()

	def random(self):
		index = randint(0, self.count - 1)
		return self.leds[index]

	def random_available(self):
		available = [led for led in self.leds if led.index not in self.gens]

		if not available:
			return None

		return choice(available)

	def assign(self, led, func, *args, **kwargs):
		self.gens[led.index] = (led, func(led, *args, **kwargs))
		led.needs_prep = True

	def assign_random(self, func, *args, **kwargs):
		led = self.random()
		self.assign(led, func, *args, **kwargs)

	def assign_available(self, func, *args, **kwargs):
		led = self.random_available()
		if led is None:
			return

		self.assign(led, func, *args, **kwargs)

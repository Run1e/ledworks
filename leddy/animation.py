from inspect import getmembers

from .timers import Timer
from .timers import call_once_every


class Animation:
	def __init__(self, strip):
		self.strip = strip

		self.time = 0.0
		self.ticks = 0

		self.timers = []

		for key, timer in getmembers(self):
			if isinstance(timer, Timer):
				timer.setup(self)
				self.timers.append(timer)

		self.setup()

	def setup(self):
		pass

	def tick(self, delta):
		self.time += delta

		# call timers, if any should be called now
		for timer in self.timers:
			timer.maybe_call(self, self.time)

		# advance generators, removing them if finished
		remove = []
		for led, gen in self.strip.gens.values():
			if led.needs_prep is True:
				led.prep(self.time)

			led.set_delta(delta)

			try:
				next(gen)
			except StopIteration:
				remove.append(led.index)

		# remove exhausted gens
		for index in reversed(remove):
			self.strip.gens.pop(index)

		self.ticks += 1

	@call_once_every(seconds=1.0)
	def fps(self, interval):
		print('TPS: {0} ON: {1}'.format(self.ticks, len(self.strip.gens)))
		self.ticks = 0

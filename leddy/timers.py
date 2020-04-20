from itertools import cycle as icycle


class Timer:
	def __init__(self, func):
		self.func = func

	def __call__(self, animation, delta):
		self.func(animation, *self.prepare(animation, delta))

	def setup(self, animation):
		pass

	def prepare(self, animation, delta):
		return ()

	def times_to_call(self, time):
		raise NotImplemented


class IntervalTimer(Timer):
	def __init__(self, func, interval):
		super().__init__(func)

		self.interval = interval
		self.iteration = 0

	def prepare(self, animation, delta):
		self.iteration += 1
		return (self.interval,)

	def times_to_call(self, time):
		return int(time / self.interval) - self.iteration  # should_be_at - currently_at


class All(IntervalTimer):
	def setup(self, animation):
		self.interval /= animation.strip.count


class Cycler(IntervalTimer):
	def __init__(self, func, seconds, reverse):
		super().__init__(func, seconds)
		self.reverse = reverse

	def setup(self, animation):
		it = reversed(animation.strip.leds) if self.reverse else animation.strip.leds
		self.generator = icycle(it)
		self.interval /= animation.strip.count

	def prepare(self, animation, delta):
		self.iteration += 1
		return self.interval, next(self.generator)


class PerTick(Timer):
	def times_to_call(self, time):
		return 1

	def prepare(self, animation, delta):
		return (delta,)


def tick():
	return lambda func: PerTick(func)


def once_every(seconds):
	return lambda func: IntervalTimer(func, seconds)


def all_every(seconds):
	return lambda func: All(func, seconds)


def cycle(seconds, reverse=False):
	return lambda func: Cycler(func, seconds, reverse)

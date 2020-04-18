from itertools import cycle as icycle


class Timer:
	def __init__(self, func, interval):
		self.func = func
		self.interval = interval

		self.iteration = 0

	def __call__(self, animation, *args, **kwargs):
		self.func(animation, self.interval, *args, **kwargs)

	def setup(self, animation):
		pass

	def maybe_call(self, animation, time):
		should_be_at = int(time / self.interval)
		while self.iteration < should_be_at:
			self.iteration += 1
			self(animation)


class CallOnce(Timer):
	pass


class CallAll(Timer):
	def setup(self, animation):
		self.interval /= animation.strip.count


class LEDCycler(Timer):
	def __init__(self, func, seconds, reverse):
		super().__init__(func, seconds)
		self.reverse = reverse

	def setup(self, animation):
		it = reversed(animation.strip.leds) if self.reverse else animation.strip.leds
		self.generator = icycle(it)
		self.interval /= animation.strip.count

	def __call__(self, animation, *args, **kwargs):
		self.func(animation, self.interval, next(self.generator))


def call_once_every(seconds):
	return lambda func: CallOnce(func, seconds)


def call_all_every(seconds):
	return lambda func: CallAll(func, seconds)


def cycle(seconds, reverse=False):
	return lambda func: LEDCycler(func, seconds, reverse)

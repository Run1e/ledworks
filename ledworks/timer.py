class Timer:
	def __init__(self, func):
		self.func = func
		self.iteration = 0
		self.animation = None

	def __call__(self):
		self.func(self.animation)
		self.iteration += 1

	def set_animation(self, animation):
		self.animation = animation

	def tick(self, delta):
		raise NotImplementedError


class IntervalTimer(Timer):
	def __init__(self, func, interval):
		super().__init__(func)

		self.interval = interval
		self._elapsed = 0.0

	def tick(self, delta):
		self._elapsed += delta
		times = int(self._elapsed / self.interval) - self.iteration  # should_be_at - currently_at

		if times > 0:
			for _ in range(times):
				self()


class PerTick(Timer):
	def tick(self, delta):
		self()


class _AllMixin:
	def set_animation(self, animation):
		super().set_animation(animation)
		self.interval /= animation.n


class _RandomMixin:
	def __call__(self):
		animation = self.animation
		self.func(animation, animation.rand())
		self.iteration += 1


class AllTimer(_AllMixin, IntervalTimer):
	pass


class RandomTimer(_RandomMixin, IntervalTimer):
	pass


class RandomAllTimer(_AllMixin, _RandomMixin, IntervalTimer):
	pass


class CycleTimer(IntervalTimer):
	def __init__(self, func, interval, reverse):
		super().__init__(func, interval)
		self._idx = 0
		self._reverse = reverse

	def __call__(self):
		animation = self.animation
		self.func(animation, self._idx)
		add = -1 if self._reverse else 1
		self._idx = (self._idx + add) % animation.n
		self.iteration += 1


class CycleAllTimer(_AllMixin, CycleTimer):
	pass


def once_per(interval):
	return lambda func: IntervalTimer(func, interval)


def every_tick():
	return lambda func: PerTick(func)


def all_per(interval):
	return lambda func: AllTimer(func, interval)


def random_once(interval):
	return lambda func: RandomTimer(func, interval)


def random_all(interval):
	return lambda func: RandomAllTimer(func, interval)


def cycle_once(interval, reverse=False):
	return lambda func: CycleTimer(func, interval, reverse)


def cycle_all(interval, reverse=False):
	return lambda func: CycleAllTimer(func, interval, reverse)

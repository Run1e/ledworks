from functools import partial
from inspect import getmembers
from random import randint

import numpy as np

from .timer import Timer, every_tick, once_per


class Animation:
	def __init__(self, n):
		self.n = n
		self.data = np.zeros((n, 3), dtype=np.float32)

	def set(self, idx, color):
		self.data[idx] = color

	def setup(self, player):
		pass

	def tick(self, delta, elapsed):
		pass

	def all(self):
		return range(self.n)

	def rand(self):
		return randint(0, self.n - 1)

	def postprocess(self, delta, elapsed):
		raise NotImplementedError('Must be subclassed')


class GeneratorAnimation(Animation):
	def __init__(self, n):
		self.__fps = 0

		self.gens = dict()
		self.timers = list()

		super().__init__(n)

		for key, timer in getmembers(self):
			if isinstance(timer, Timer):
				timer.set_animation(self)
				self.timers.append(timer)

	def _process_timers(self, delta, elapsed):
		for timer in self.timers:
			timer.tick(delta, elapsed)

	def _process_gens(self, delta, elapsed):
		remove = list()
		for idx, gen in self.gens.items():
			if gen(delta, elapsed):
				remove.append(idx)

		for idx in reversed(remove):
			self.gens.pop(idx)

	def assign(self, idx, gen, **kwargs):
		self.gens[idx] = gen(partial(self.set, idx), **kwargs)

	def tick(self, delta, elapsed):
		self._process_timers(delta, elapsed)
		self._process_gens(delta, elapsed)
		self.postprocess(delta, elapsed)

	@every_tick()
	def __count_fps(self, delta, elapsed):
		self.__fps += 1

	@once_per(1.0)
	def __print_fps(self, delta, elapsed):
		print('FPS:', self.__fps)
		self.__fps = 0

from functools import partial
from inspect import getmembers
from random import randint

import numpy as np

from .timer import Timer, every_tick, once_per


class Animation:
	def __init__(self, n):
		self.__fps = 0

		self.n = n
		self.data = np.zeros(n, dtype=np.float32)
		self.color_data = np.zeros((n, 3), dtype=np.float32)

		self.gens = dict()
		self.timers = list()
		self.elapsed = 0.0

		for key, timer in getmembers(self):
			if isinstance(timer, Timer):
				timer.set_animation(self)
				self.timers.append(timer)

	def set(self, idx, intensity):
		self.data[idx] = intensity

	def setup(self, player):
		pass

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

	def tick(self, delta, raw_audio_data):
		# track elapsed time in this animation
		self.elapsed += delta

		# process timers and generators
		self._process_timers(delta, self.elapsed)
		self._process_gens(delta, self.elapsed)

		# get final color data from postprocessing
		self.color_data = self.postprocess(
			delta,
			self.elapsed,
			self.data.copy(),
			self.process_audio(delta, self.elapsed, raw_audio_data)
		)

	def all(self):
		return range(self.n)

	def rand(self):
		return randint(0, self.n - 1)

	def postprocess(self, delta, elapsed, gen_data, audio_data):
		return np.repeat(gen_data, 3).reshape(-1, 3)

	def process_audio(self, delta, elapsed, data):
		pass

	@every_tick()
	def on_every_tick(self, delta, elapsed):
		self.__fps += 1

	@once_per(1.0)
	def on_every_second(self, delta, elapsed):
		print('FPS:', self.__fps)
		self.__fps = 0
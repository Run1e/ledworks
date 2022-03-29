from random import random

import numpy as np

import ledworks


class MyAnim(ledworks.Animation):
	def setup(self, player):
		self.elapsed = 0

	def tick(self, delta, elapsed):
		self.elapsed += delta
		for n in self.all():
			self.data[n] = ledworks.hue(self.elapsed - n / self.n)


class GenAnim(ledworks.GeneratorAnimation):
	@ledworks.cycle_all(3.0, reverse=False)
	def test(self, idx, delta, elapsed):
		self.assign(idx, ledworks.gen.fade, color=ledworks.hue(idx / self.n), duration=random())


class RandAnim(ledworks.GeneratorAnimation):
	@ledworks.random_all(3.0)
	def test(self, idx, delta, elapsed):
		self.assign(idx, ledworks.gen.fade, color=ledworks.hue(idx / self.n), duration=random() * 3)


class GossipAnim(ledworks.GeneratorAnimation):
	@ledworks.cycle_all(2.0)
	def test(self, idx, delta, elapsed):
		self.assign(idx, ledworks.gen.abrupt, duration=0.5)
		self.assign((idx + self.n // 2) % self.n, ledworks.gen.abrupt, duration=0.5)

	def postprocess(self, data, delta, elapsed):
		return np.array([ledworks.hue(p / self.n + (elapsed * 0.2)) * intensity for p, intensity in enumerate(data)])


class AudioAnim(ledworks.AudioAnimation):
	def setup(self, player):
		self.mapper = ledworks.log_filterbank(
			rate=player.rate,
			bins=self.n // 2,
			n_fft=player.chunk,
			f_min=20,
			f_max=320,
		)

		self.normalize = ledworks.filter.Normalize(player.fps)
		self.sustain = ledworks.filter.Sustain(0.15, player.fps)
		self.color = ledworks.color.ColorIntensity(ledworks.hue)
		self.blur = ledworks.filter.Blur(2.5)
		self.mirror = ledworks.filter.Mirror(self.n // 2)
		self.intensity = ledworks.color.Intensity()
		self.logistic = ledworks.filter.Logistic(k=6, x_0=0.5)

	def tick(self, delta, data):
		bins = self.mapper.dot(data)
		bins = self.normalize(delta, bins)
		# bins = self.logistic(delta, bins)
		bins = self.sustain(delta, bins)
		bins = self.blur(delta, bins)
		bins = self.mirror(delta, bins)
		self.color_data = self.color(delta, bins)


N = 64
view = ledworks.PygletView(N)

#player = ledworks.Player(N, view=view, fps=60)
#player.play(GossipAnim)
player = ledworks.AudioPlayer(N, view=view, stream=ledworks.stream.get_stream(5), fps=45)
player.play(AudioAnim)

"""
pr = cProfile.Profile()
pr.run('player.play(AudioAnim)')
stats = pstats.Stats(pr)
stats.sort_stats(pstats.SortKey.TIME)
stats.print_stats()
stats.dump_stats('profiling.prof')
"""

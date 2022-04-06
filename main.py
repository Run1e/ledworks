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


class GenAnim(ledworks.Animation):
	@ledworks.cycle_all(3.0, reverse=False)
	def test(self, idx, delta, elapsed):
		self.assign(idx, ledworks.gen.fade, color=ledworks.hue(idx / self.n), duration=random())


class RandAnim(ledworks.Animation):
	@ledworks.random_all(3.0)
	def test(self, idx, delta, elapsed):
		self.assign(idx, ledworks.gen.fade, color=ledworks.hue(idx / self.n), duration=random() * 3)


class GossipAnim(ledworks.Animation):
	@ledworks.cycle_all(2.0)
	def test(self, idx, delta, elapsed):
		self.assign(idx, ledworks.gen.abrupt, duration=0.5)
		self.assign((idx + self.n // 2) % self.n, ledworks.gen.abrupt, duration=0.5)

	def postprocess(self, delta, elapsed, gen_data, audio_data):
		return np.array([ledworks.hue(p / self.n + (elapsed * 0.2)) * intensity for p, intensity in enumerate(gen_data)])


class AudioAnim(ledworks.Animation):
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
		self.blur = ledworks.filter.Blur(2.5)
		self.mirror = ledworks.filter.Mirror(self.n // 2)
		self.color = ledworks.color.ColorIntensity(ledworks.hue)

	def process_audio(self, delta, elapsed, data):
		bins = self.mapper.dot(data)
		bins = self.normalize(delta, bins)
		bins = self.sustain(delta, bins)
		bins = self.blur(delta, bins)
		return self.mirror(delta, bins)

	def postprocess(self, delta, elapsed, led_data, audio_data):
		return self.color(delta, audio_data)

class KickReactive(ledworks.Animation):
	def setup(self, player):
		self.mapper = ledworks.log_filterbank(
			rate=player.rate,
			bins=6,
			n_fft=player.chunk,
			f_min=20,
			f_max=100,
		)

		self.normalize = ledworks.filter.Normalize(player.fps)
		self.sustain = ledworks.filter.Sustain(0.15, player.fps)

	def process_audio(self, delta, elapsed, data):
		bins = self.mapper.dot(data)
		bins = self.normalize(delta, bins)
		return np.max(self.sustain(delta, bins))

	@ledworks.cycle_all(2.0)
	def test(self, idx, delta, elapsed):
		self.assign(idx, ledworks.gen.abrupt, duration=0.5)
		self.assign((idx + self.n // 2) % self.n, ledworks.gen.abrupt, duration=0.5)

	def postprocess(self, delta, elapsed, gen_data, audio_data):
		data = gen_data * audio_data
		return np.array([ledworks.hue(p / self.n + (elapsed * 0.2)) * intensity for p, intensity in enumerate(data)])



N = 64
view = ledworks.PygletView(N)

#player = ledworks.Player(N, view=view, fps=60)
#player.play(GossipAnim)
player = ledworks.Player(N, view=view, stream=ledworks.stream.get_stream(5), fps=45)

player.play(KickReactive)

"""
pr = cProfile.Profile()
pr.run('player.play(AudioAnim)')
stats = pstats.Stats(pr)
stats.sort_stats(pstats.SortKey.TIME)
stats.print_stats()
stats.dump_stats('profiling.prof')
"""

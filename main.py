import numpy as np

import cProfile
import pstats

import ledworks

N = 64

view = ledworks.PygletView(N)
player = ledworks.Player(N, view=view, timescale=1.0)


class MyAnim(ledworks.Animation):
	def setup(self, player):
		self.elapsed = 0

	def tick(self, delta):
		self.elapsed += delta
		for n in self.all():
			self.data[n] = ledworks.hue(self.elapsed - n / self.n)


class GenAnim(ledworks.GeneratorAnimation):
	@ledworks.cycle_all(2.0, reverse=False)
	def test(self, idx):
		self.assign(idx, ledworks.gen.fade, color=ledworks.hue(idx / self.n), duration=3.0)


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
		self.blur = ledworks.filter.Blur(3.0)
		self.mirror = ledworks.filter.Mirror(self.n // 2)
		self.intensity = ledworks.color.Intensity()
		self.logistic = ledworks.filter.Logistic(k=6, x_0=0.5)

	def tick(self, delta, data):
		bins = self.mapper.dot(data)
		bins = self.normalize(delta, bins)
		#bins = self.logistic(delta, bins)
		bins = self.sustain(delta, bins)
		bins = self.blur(delta, bins)
		bins = self.mirror(delta, bins)
		self.data = self.color(delta, bins)
		#self.data = self.intensity(delta, bins)


import pyaudio

p = pyaudio.PyAudio()

stream = p.open(
	format=pyaudio.paInt16,
	channels=2,
	rate=44100,
	input=True,
	frames_per_buffer=2048,
	input_device_index=7,
	as_loopback=True,
)


#player.play(GenAnim)
player = ledworks.AudioPlayer(N, view=view, stream=stream, fps=45)
player.play(AudioAnim)


pr = cProfile.Profile()
pr.run('player.play(AudioAnim)')
stats = pstats.Stats(pr)
stats.sort_stats(pstats.SortKey.TIME)
stats.print_stats()
stats.dump_stats('profiling.prof')

from random import randint

import numpy as np
import pyaudio

import leddy


class RandomLinear(leddy.Animation):
	@leddy.once_every(seconds=0.1)
	def test(self, interval):
		self.strip.assign_random(leddy.rate.linear, duration=3.0)


class HueSpin(leddy.Animation):
	@leddy.cycle(seconds=1.0, reverse=True)
	def loop(self, interval, led):
		self.strip.assign(led, leddy.rate.fade, color=leddy.utils.hue(self.time * 2.0), duration=0.4)


class Visualizer(leddy.Animation):
	def setup(self):
		self.chunk = 1024
		p = pyaudio.PyAudio()

		self.stream = p.open(
			format=pyaudio.paInt24,
			channels=2,
			rate=44100,
			input=True,
			frames_per_buffer=self.chunk,
			input_device_index=3,
			as_loopback=True
		)

	@leddy.tick()
	def tick(self, delta):
		data = np.frombuffer(self.stream.read(self.chunk, exception_on_overflow=False), dtype=np.int16)


class HueComet(leddy.Animation):
	@leddy.cycle(seconds=4.0, reverse=False)
	def cycle(self, interval, led):
		self.strip.assign(
			led, leddy.rate.fade,
			color=leddy.utils.hue(self.time * 1.61), duration=randint(self.strip.count // 30, self.strip.count // 3) * interval
		)


if __name__ == '__main__':
	strip = leddy.Strip(128)
	player = leddy.PygletPlayer(strip, fps=None, timescale=1.0, width=960, height=960)
	player.play(HueComet)
# player.play_cycle(HueSpin(strip), HueComet(strip))

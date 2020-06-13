from random import randint

import numpy as np

import ledworks


class HueSpin(ledworks.Animation):
	@ledworks.cycle(seconds=3.0, reverse=True)
	def loop(self, interval, led):
		self.strip.assign(led, ledworks.rate.fade(color=ledworks.utils.hue(self.time * 2.0), duration=2.6))


class HueComet(ledworks.Animation):
	@ledworks.cycle(seconds=4.0, reverse=False)
	def cycle(self, interval, led):
		color = ledworks.utils.hue(self.time * 1.61)
		duration = randint(self.strip.count // 30, self.strip.count // 3) * interval

		self.strip.assign(
			led, ledworks.rate.fade(color=color, duration=duration)
		)

	def on_data(self, data):
		pass  # print(data)


class TameImpala(ledworks.Animation):
	@ledworks.cycle(seconds=3.0)
	def cycle(self, interval, led):
		duration = interval * self.strip.count / 4
		self.strip.assign(led, ledworks.rate.rotating_hue_full(start=self.time, duration=duration, rate=0.5))
		self.strip.assign(self.strip.get_opposite(led.index), ledworks.rate.rotating_hue_full(start=self.time, duration=duration, rate=0.5))


class Visualizer(ledworks.Animation):
	def on_data(self, data):
		size = self.strip.count
		half_size = size // 2

		fin = np.zeros(size * 3).reshape(-1, 3)
		fin[:half_size] = data
		fin[half_size:] = data[::-1]

		np.copyto(self.strip.data, fin)


if __name__ == '__main__':
	import pyaudio

	p = pyaudio.PyAudio()

	print(p.get_default_input_device_info())

	stream = p.open(
		format=pyaudio.paInt16,
		channels=2,
		rate=44100,
		input=True,
		frames_per_buffer=2048,
		input_device_index=4,
		as_loopback=True
	)

	strip = ledworks.Strip(128)

	player = ledworks.AudioPlayer(
		strip=strip,
		view=ledworks.PygletView(strip, width=720, height=720),
		fps=60,
		stream=stream,
		mapper=ledworks.LogMapper(bins=strip.count // 2, f_min=20, f_max=320),
	)

	player.add_filter(ledworks.NormalizeFilter())
	player.add_filter(ledworks.SustainFilter(0.12))  # 0.32

	player.add_filter(ledworks.StaticColorRangeFilter())

	player.play(Visualizer)

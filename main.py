from random import randint

import numpy as np
import pyaudio

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
		pass #print(data)


class TameImpala(ledworks.Animation):
	@ledworks.cycle(seconds=3.0)
	def cycle(self, interval, led):
		duration = interval * self.strip.count / 4
		self.strip.assign(led, ledworks.rate.rotating_hue_full(start=self.time, duration=duration, rate=0.5))
		self.strip.assign(self.strip.get_opposite(led.index), ledworks.rate.rotating_hue_full(start=self.time, duration=duration, rate=0.5))


class Visualizer(ledworks.Animation):
	def setup(self, player):
		self.sens = 8.0

		# self.mel = librosa.filters.mel(sr=self.rate, n_fft=self.chunk, n_mels=self.strip.count, fmin=0, fmax=8000)
		self.log = ledworks.log_filterbank(
			player.rate,
			self.strip.count // 2,
			player.chunk // 2,
			f_min=0,
			f_max=500
		)


	@ledworks.cycle(seconds=4.0, reverse=False)
	def cycle(self, interval, led):
		return
		color = ledworks.utils.hue(self.time * 1.61)
		duration = randint(self.strip.count // 30, self.strip.count // 3) * interval

		self.strip.assign(
			led, ledworks.rate.fade(color=color, duration=duration)
		)

	def on_data(self, data):
		data = self.log.dot(data) * self.sens

		fin = np.zeros(self.strip.count)
		fin[:self.strip.count // 2] = data
		fin[self.strip.count // 2:] = data[::-1]

		# color = ledworks.utils.hue(self.time)

		# [1, 2, 3] -> [(1, 1, 1), (2, 2, 2), (3, 3, 3)]
		out = np.repeat(fin, 3).reshape(-1, 3)

		np.copyto(self.strip.data, out)


if __name__ == '__main__':
	import pyaudio

	p = pyaudio.PyAudio()

	stream = p.open(
		format=pyaudio.paInt16,
		channels=2,
		rate=44100,
		input=True,
		frames_per_buffer=2048,
		input_device_index=4,
		as_loopback=True
	)

	strip = ledworks.Strip(60)

	player = ledworks.AudioPlayer(
		strip=strip,
		view=ledworks.PygletView(strip, width=720, height=720),
		fps=60,
		stream=stream,
	)

	player.play(Visualizer)

"""
	@ledworks.tick()
	def tick(self, delta, data):
		# get raw dual channel PCM data from sound card
		# as this is 16-bit, it ranges from -2**15 to 2**15-1
		raw_data = self.stream.read(self.chunk, exception_on_overflow=False)

		# because of that, dividing it by 2**15 gives us the range of -1.0 to 1.0
		stereo = np.frombuffer(raw_data, dtype=np.int16) / 2 ** 15

		# TODO: figure out how to combine N channels
		mono = stereo[1::2]

		# mono is now CHUNK in length

		# perform fast fourier transform (real) on mono data
		fft_complex = np.fft.rfft(mono)

		# get absolute values from complex data and normalize between 0.0 - 1.0 (hopefully? needs to be double checked)
		fft_data = np.abs(fft_complex) / (self.chunk / 2)

		# fft_data is CHUNK+1 in length

		# mel_data = self.mel.dot(fft_data) * self.strip.count
		data = self.log.dot(fft_data) * self.sens

		fin = np.zeros(self.strip.count)
		fin[:self.strip.count // 2] = data
		fin[self.strip.count // 2:] = data[::-1]

		# color = ledworks.utils.hue(self.time)

		# [1, 2, 3] -> [(1, 1, 1), (2, 2, 2), (3, 3, 3)]
		out = np.repeat(fin, 3).reshape(-1, 3)

		np.copyto(self.strip.data, out)

"""
from random import randint

import numpy as np
import pyaudio

import leddy


class HueSpin(leddy.Animation):
	@leddy.cycle(seconds=3.0, reverse=False)
	def loop(self, interval, led):
		self.strip.assign(led, leddy.rate.fade, color=leddy.utils.hue(self.time * 2.0), duration=2.6)


class HueComet(leddy.Animation):
	@leddy.cycle(seconds=4.0, reverse=False)
	def cycle(self, interval, led):
		self.strip.assign(
			led, leddy.rate.fade(color=leddy.utils.hue(self.time * 1.61), duration=randint(self.strip.count // 30, self.strip.count // 3) * interval)
		)


class TameImpala(leddy.Animation):
	@leddy.cycle(seconds=3.0)
	def cycle(self, interval, led):
		duration = interval * self.strip.count / 4
		self.strip.assign(led, leddy.rate.rotating_hue_full(start=self.time, duration=duration, rate=0.5))
		self.strip.assign(self.strip.get_opposite(led.index), leddy.rate.rotating_hue_full(start=self.time, duration=duration, rate=0.5))


def hertz_to_mel(freq):
	return 2595.0 * np.log10(1 + (freq / 700.0))


class Visualizer(leddy.Animation):
	def setup(self):
		self.sens = 1.0

		self.channels = 2
		self.rate = 44100
		self.sample_size = 16
		self.chunk = 256
		self.real_chunk = self.chunk // self.channels

		self.timestep = 1.0 / self.rate

		p = pyaudio.PyAudio()

		# for n in range(p.get_device_count()):
		print(p.get_device_info_by_index(4))

		self.stream = p.open(
			format=pyaudio.paInt16,
			channels=self.channels,
			rate=self.rate,
			input=True,
			frames_per_buffer=self.chunk,
			input_device_index=4,
			as_loopback=True
		)

		# self.mel = librosa.filters.mel(sr=self.rate, n_fft=self.chunk, n_mels=self.strip.count, fmin=0, fmax=8000)
		self.log = leddy.log_filterbank(self.rate, self.strip.count, self.chunk // 2)

	@leddy.tick()
	def tick(self, delta):
		# get raw dual channel PCM data from sound card
		raw_data = self.stream.read(self.chunk, exception_on_overflow=False)

		# read into numpy array as 16 bit integers
		stereo = np.frombuffer(raw_data, dtype=np.int16) / 2 ** 15

		# TODO: figure out how to combine N channels
		mono = stereo[::2]

		# perform fast fourier transform (real) on mono data
		fft_complex = np.fft.rfft(mono)

		# normalize between
		fft_data = np.abs(fft_complex) * self.channels / self.chunk

		# mel_data = self.mel.dot(fft_data) * self.strip.count
		data = self.log.dot(fft_data) * self.sens

		# [1, 2, 3] -> [(1, 1, 1), (2, 2, 2), (3, 3, 3)]
		out = np.repeat(data, 3).reshape(-1, 3)

		self.strip.data = out


if __name__ == '__main__':
	strip = leddy.Strip(128)
	player = leddy.PygletPlayer(strip, fps=None, timescale=1.0, width=1000, height=1000)
	player.play(Visualizer)

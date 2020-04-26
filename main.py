from random import randint

import numpy as np
import pyaudio

import ledworks


class HueSpin(ledworks.Animation):
	@ledworks.cycle(seconds=3.0, reverse=False)
	def loop(self, interval, led):
		self.strip.assign(led, ledworks.rate.fade, color=ledworks.utils.hue(self.time * 2.0), duration=2.6)


class HueComet(ledworks.Animation):
	@ledworks.cycle(seconds=4.0, reverse=False)
	def cycle(self, interval, led):

		color = ledworks.utils.hue(self.time * 1.61)
		duration = randint(self.strip.count // 30, self.strip.count // 3) * interval

		self.strip.assign(
			led, ledworks.rate.fade(color=color, duration=duration)
		)


class TameImpala(ledworks.Animation):
	@ledworks.cycle(seconds=3.0)
	def cycle(self, interval, led):
		duration = interval * self.strip.count / 4
		self.strip.assign(led, ledworks.rate.rotating_hue_full(start=self.time, duration=duration, rate=0.5))
		self.strip.assign(self.strip.get_opposite(led.index), ledworks.rate.rotating_hue_full(start=self.time, duration=duration, rate=0.5))


def hertz_to_mel(freq):
	return 2595.0 * np.log10(1 + (freq / 700.0))


class Visualizer(ledworks.Animation):
	def setup(self):
		self.sens = 2.0

		self.channels = 2
		self.rate = 44100
		self.sample_size = 16
		self.chunk = 720
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
		self.log = ledworks.log_filterbank(self.rate, self.strip.count // 2, self.chunk // 2, f_min=0, f_max=1000)

	@ledworks.tick()
	def tick(self, delta):
		# get raw dual channel PCM data from sound card
		raw_data = self.stream.read(self.chunk, exception_on_overflow=False)

		# read into numpy array as 16 bit integers
		stereo = np.frombuffer(raw_data, dtype=np.int16) / 2 ** 15

		# TODO: figure out how to combine N channels
		mono = stereo[::2]

		# perform fast fourier transform (real) on mono data
		fft_complex = np.fft.rfft(mono)

		# get absolute values from complex data and normalize between 0.0 - 1.0 (hopefully? needs to be double checked)
		fft_data = np.abs(fft_complex) * self.channels / self.chunk

		# mel_data = self.mel.dot(fft_data) * self.strip.count
		data = self.log.dot(fft_data) * self.sens

		fin = np.zeros(self.strip.count)
		fin[:self.strip.count // 2] = data
		fin[self.strip.count // 2:] = data[::-1]

		#color = ledworks.utils.hue(self.time)

		# [1, 2, 3] -> [(1, 1, 1), (2, 2, 2), (3, 3, 3)]
		out = np.repeat(fin, 3).reshape(-1, 3)

		np.copyto(self.strip.data, out)


if __name__ == '__main__':
	strip = ledworks.Strip(96)
	player = ledworks.PygletPlayer(strip, fps=None, timescale=1.0, width=480, height=480)
	player.play(HueComet)

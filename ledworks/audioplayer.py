from time import perf_counter

import numpy as np

from .audioanimation import AudioAnimation
from .player import Player

WINDOW_SIZE = 2


class AudioPlayer(Player):
	def __init__(self, n, view, stream, fps=None):
		super().__init__(n, view, fps=fps, timescale=1.0)

		self.stream = stream

		# sampling rate (44100)
		self.rate = stream._rate

		# channel count (2)
		self.channels = stream._channels

		# how many bits in each sample (16)
		self.sample_size = {2: 32, 4: 24, 8: 16, 16: 8}[stream._format]

		# which numpy data type to use for that sample
		self.dtype = {8: np.int8, 16: np.int16, 24: np.int32, 32: np.int32}[self.sample_size]

		# number of frames to read
		# one frame is one sample for each channel (so 2*16=32 bits)
		self.chunk = (self.rate // self.fps) ^ 1

		# scalar used to fit a 16-bit value into 0.0-1.0
		self.scalar = 2 ** (self.sample_size - 1)

		# rolling window for data
		self.roll = np.zeros(self.chunk * WINDOW_SIZE).reshape(WINDOW_SIZE, self.chunk)

	def fft(self):
		# get raw PCM data from soundcard
		# fps is controlled here, as this blocks until the buffer is filled
		# and since chunk is sizes to only fill when
		# 1/fps of a second has passed, it works okay
		raw_data = self.stream.read(self.chunk, exception_on_overflow=False)

		# read it into a numpy buffer using this soundcards sample_size as type
		# divide by 2 ** (sample_size - 1) in order to normalize values between
		# -1.0 and 1.0
		data = np.frombuffer(raw_data, dtype=self.dtype) / self.scalar

		# TODO: combining channels. do I have to do a transform for each channel?
		# this solution probably works but I hate it
		if self.channels > 1:
			data = data[::self.channels]

		roll = self.roll
		roll[:-1] = roll[1:]
		roll[-1:] = data.copy()

		rolled = np.concatenate(roll)

		# perform FFT (from real numbers)
		fft_complex = np.fft.rfft(rolled)

		# print(fft_complex.shape)

		# get the absolute values of the complex numbers
		# and again, normalize between 0.0 and 1.0
		# I hope that's what this does anyway
		return 2 * np.abs(fft_complex) / self.chunk

	def play(self, animation):
		animation: AudioAnimation = animation(self.n)
		animation.setup(self)

		self.view.set_data(animation.color_data)

		now = perf_counter()

		while True:
			now, prev = perf_counter(), now
			delta = (now - prev) * self.timescale

			animation.tick(delta, self.fft())

			# if self.fps is None or self.time_since_last_frame > self.frame_interval:
			self.view.draw(animation.color_data)

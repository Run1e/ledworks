from time import perf_counter

import numpy as np

from .animation import Animation

TEMPORAL_WINDOW = 0.04


"""
each tick we will read rate/fps frames
previously we concatenated two of these chunks,
meaning each tick had 2/45th of a seconds worth of audio data

meaning, each tick should have rate / (2/45) frames

"""


class Player:
	def __init__(self, n, view, stream=None, fps=None, timescale=1.0):
		self.n = n
		self.view = view
		self.fps = fps
		self.timescale = timescale

		self._interval = None if fps is None else 1.0 / fps

		if stream is not None:
			self.setup_stream(stream)

	def setup_stream(self, stream):
		self.stream = stream

		# sampling rate (44100)
		self.rate = stream._rate

		# channel count (2)
		self.channels = stream._channels

		# how many bits in each sample (16)
		self.sample_size = {2: 32, 4: 24, 8: 16, 16: 8}[stream._format]

		# which numpy data type to use for that sample
		self.dtype = {8: np.int8, 16: np.int16, 24: np.int32, 32: np.int32}[self.sample_size]

		# number of frames to read per tick
		# one frame is one sample for each channel (so 2*16=32 bits)
		self.chunk = self.rate // self.fps // self.channels

		# size of our rolling window
		self.window_size = int(self.rate * TEMPORAL_WINDOW)

		# scalar used to fit an n-bit value into -1.0 - 1.0
		self.scalar = 2 ** (self.sample_size - 1)

		# rolling window for data
		self.window = np.zeros(self.window_size, dtype=np.float64)

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

		window = self.window

		chunk = self.chunk
		window_size = self.window_size
		src = window[0:window_size - chunk]
		dst = window[chunk:]

		np.copyto(dst, src)

		np.copyto(window[:chunk], data)

		# perform FFT (from real numbers)
		fft_complex = np.fft.rfft(window)

		# get the absolute values of the complex numbers
		# and again, normalize between 0.0 and 1.0
		# I hope that's what this does anyway
		out = 2 * np.abs(fft_complex) / self.chunk
		return out

	def play(self, animation):
		animation: Animation = animation(self.n)
		animation.setup(self)

		self.view.set_data(animation.color_data)

		now = perf_counter()

		while True:
			now, prev = perf_counter(), now
			delta = (now - prev) * self.timescale
			self.fft()
			animation.tick(delta, self.fft() if self.stream else None)

			# if self.fps is None or self.time_since_last_frame > self.frame_interval:
			self.view.draw(animation.color_data)


	def slideshow(self, animations):
		animations = [animation(self.n) for animation in animations]

		anims = list()
		for animation in animations:
			anim = animation(self.n)
			anim.setup(self)
			anims.append(anim)



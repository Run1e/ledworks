import numpy as np
from time import perf_counter

from .player import Player


class AudioPlayer(Player):
	def __init__(self, strip, view, fps, stream):
		if not isinstance(fps, (int, float)):
			raise TypeError('fps has to be set for AudioPlayers.')

		super().__init__(strip, view, fps)

		self.stream = stream
		self.rate = stream._rate
		self.channels = stream._channels
		self.sample_size = {2: 32, 4: 24, 8: 16, 16: 8}[stream._format]
		self.dtype = {8: np.int8, 16: np.int16, 24: np.int32, 32: np.int32}[self.sample_size]
		self.chunk = (self.rate // self.fps) ^ 1

		self.scaler = 2 ** (self.sample_size - 1)

		self.filters = []

	def add_filter(self, filter):
		filter.setup(self)
		self.filters.append(filter)

	def fft(self):
		# get raw PCM data from soundcard
		raw_data = self.stream.read(self.chunk, exception_on_overflow=False)

		# read it into a numpy buffer using this soundcards sample_size as type
		# divide by 2 ** (sample_size - 1) in order to normalize values between
		# -1.0 and 1.0
		stereo = np.frombuffer(raw_data, dtype=self.dtype) / self.scaler

		# TODO: combining channels. do I have to do a transform for each channel?
		mono = stereo[::2]

		# perform FFT (from real numbers)
		fft_complex = np.fft.rfft(mono)

		# get the absolute values of the complex numbers
		# and again, normalize between 0.0 and 1.0
		# I sure do hope that's what dividing by chunk / 2 does
		return np.abs(fft_complex) / (self.chunk / 2)

	def play(self, animation):
		animation = animation(self.strip)
		animation.setup(self)

		on_data = getattr(animation, 'on_data', None)

		now = perf_counter()

		while True:
			# time calculations
			now, prev = perf_counter(), now
			delta = (now - prev) * self.timescale
			self.time += delta

			# get fft data
			fft = self.fft()

			# run through processing filters
			for filter in self.filters:
				fft = filter.process(delta, fft)

			# give data to data event handler
			if on_data is not None:
				on_data(fft)

			# tick animation
			animation._tick(delta)

			# draw
			self.view.draw()

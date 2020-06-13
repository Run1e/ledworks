import numpy as np
from time import perf_counter

from .player import Player
from .filters.filter import Filter
from .filters.colorfilter import ColorFilter


WINDOW_SIZE = 2


class AudioPlayer(Player):
	def __init__(self, strip, view, fps, stream, mapper):
		if not isinstance(fps, (int, float)):
			raise TypeError('fps has to be set for AudioPlayers.')

		super().__init__(strip, view, fps)

		self.stream = stream
		self.mapper = mapper
		self.bins = mapper.bins

		self.rate = stream._rate
		self.channels = stream._channels
		self.sample_size = {2: 32, 4: 24, 8: 16, 16: 8}[stream._format]
		self.dtype = {8: np.int8, 16: np.int16, 24: np.int32, 32: np.int32}[self.sample_size]
		self.chunk = (self.rate // self.fps) ^ 1

		self.scaler = 2 ** (self.sample_size - 1)
		self.roll = np.zeros(self.chunk * WINDOW_SIZE).reshape(WINDOW_SIZE, self.chunk)

		self.amplitude_filters = []
		self.color_filters = []

		self.mapper.setup(self)

	def add_filter(self, filter):
		filter.setup(self)

		if isinstance(filter, ColorFilter):
			self.color_filters.append(filter)
		elif isinstance(filter, Filter):
			self.amplitude_filters.append(filter)
		else:
			raise TypeError('Filter has to be of type Filter or ColorFilter.')

	def fft(self):
		# get raw PCM data from soundcard
		raw_data = self.stream.read(self.chunk, exception_on_overflow=False)

		# read it into a numpy buffer using this soundcards sample_size as type
		# divide by 2 ** (sample_size - 1) in order to normalize values between
		# -1.0 and 1.0
		data = np.frombuffer(raw_data, dtype=self.dtype) / self.scaler

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

		#print(fft_complex.shape)

		# get the absolute values of the complex numbers
		# and again, normalize between 0.0 and 1.0
		# I hope that's what this does anyway
		return 2 * np.abs(fft_complex) / self.chunk

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
			data = self.fft()
			data = self.mapper.map(data)

			# run through processing filters
			for filter in self.amplitude_filters:
				data = filter.process(delta, data)

			# [1, 2, 3] -> [(1, 1, 1), (2, 2, 2), (3, 3, 3)]
			data = np.repeat(data, 3).reshape(-1, 3)

			for filter in self.color_filters:
				data = filter.process(delta, data)

			# give data to data event handler
			if on_data is not None:
				on_data(data)

			# tick animation
			animation._tick(delta)

			# draw
			self.view.draw()

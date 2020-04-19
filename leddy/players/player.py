from time import perf_counter
from itertools import cycle


class Player:
	def __init__(self, strip, fps=None, timescale=1.0):
		self.strip = strip
		self.fps = fps
		self.timescale = timescale

		self.time = 0.0
		self.frame_interval = None if fps is None else timescale / fps
		self.time_since_last_frame = float('inf')

	def draw(self):
		raise NotImplemented

	def time(self):
		return perf_counter()

	def play(self, *animations, stop_after=float('inf')):
		animations = [animation(self.strip) for animation in animations]

		stop_at = self.time + stop_after

		now = perf_counter()
		while True:
			now, prev = perf_counter(), now
			delta = (now - prev) * self.timescale
			self.time += delta

			self.time_since_last_frame += delta

			for animation in animations:
				animation._tick(delta)

			if self.fps is None or self.time_since_last_frame > self.frame_interval:
				self.draw()
				self.time_since_last_frame = 0.0

			if self.time >= stop_at:
				return

	def play_cycle(self, *animations, duration=1.0):
		for animation in cycle(animations):
			self.play(animation, duration)

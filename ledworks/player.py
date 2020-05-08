from time import perf_counter


class Player:
	def __init__(self, strip, view, fps=None):
		self.strip = strip
		self.view = view
		self.fps = fps

		self.timescale = 1.0

		self.time = 0.0
		self.frame_interval = None if fps is None else 1.0 / fps
		self.time_since_last_frame = float('inf')

	def play(self, animation):
		animation = animation(self.strip)
		animation.setup(self)

		now = perf_counter()

		while True:
			now, prev = perf_counter(), now
			delta = (now - prev) * self.timescale

			self.time += delta
			self.time_since_last_frame += delta

			animation._tick(delta)

			if self.fps is None or self.time_since_last_frame > self.frame_interval:
				self.view.draw()
				self.time_since_last_frame = 0.0

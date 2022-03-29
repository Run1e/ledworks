from time import perf_counter

from .animation import Animation


class Player:
	def __init__(self, n, view, fps=60, timescale=1.0):
		self.n = n
		self.view = view
		self.fps = fps
		self.timescale = timescale

		self._interval = None if fps is None else 1.0 / fps

	def play(self, animation):
		animation: Animation = animation(self.n)
		animation.setup(self)

		self.view.set_data(animation.color_data)

		now = perf_counter()
		elapsed = 0.0

		while True:
			now, prev = perf_counter(), now
			delta = (now - prev) * self.timescale
			elapsed += delta

			animation.tick(delta, elapsed)

			# if self.fps is None or self.time_since_last_frame > self.frame_interval:
			self.view.draw(animation.color_data)

from math import cos, pi, sin

from pyglet.window import Window
from pyglet.gl import *

from ..player import Player

VERTICES = 5
STEP = 1.0 / VERTICES
TWO_PI = pi * 2.0


class PygletPlayer(Player):
	def __init__(self, strip, fps=None, timescale=1.0, width=640, height=640):
		super().__init__(strip, fps, timescale)

		self.width = width
		self.height = height

		self.window = Window(
			width, height,
			config=Config(sample_buffers=1, samples=4, double_buffer=True)
		)

		self.window.set_vsync(False)
		self.window.set_location(10, 40)

		self.vertex_lists = []

		# radius of outer "ring"
		outer_radius = (min(width, height) * 0.95) // 2

		circle_num = strip.count
		circle_step = 1.0 / circle_num

		angle = sin(pi / circle_num)
		inner_radius = int(outer_radius / (angle + 1))

		# radius of inner ring which all led circle's origin goes through
		circle_radius = int(0.9 * inner_radius * angle)

		center_x = width // 2
		center_y = height // 2

		for n in range(circle_num):
			s, c = sin(n * circle_step * TWO_PI), cos(n * circle_step * TWO_PI)
			x, y = center_x + int(s * inner_radius), center_y + int(c * inner_radius)

			verts = [(x, y)]
			for v in range(VERTICES + 1):
				verts.append((x + int(sin(STEP * v * TWO_PI) * circle_radius), y + int(cos(STEP * v * TWO_PI) * circle_radius)))

			self.vertex_lists.append(tuple(verts))

	def draw(self):
		self.window.dispatch_events()

		#glClear(GL_COLOR_BUFFER_BIT)
		for index, (r, g, b) in self.updates():
			vl = self.vertex_lists[index]

			glBegin(GL_TRIANGLE_FAN)
			glColor3f(r, g, b)

			for x, y in vl:
				glVertex2f(x, y)

			glEnd()

		glFlush()

		self.window.flip()

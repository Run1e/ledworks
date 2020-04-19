from math import cos, pi, sin

import pyglet

from .player import Player

VERTICES = 5
STEP = 1.0 / VERTICES
TWO_PI = pi * 2.0


class PygletPlayer(Player):
	def __init__(self, strip, fps=None, timescale=1.0, width=640, height=640):
		super().__init__(strip, fps, timescale)

		self.width = width
		self.height = height

		self.window = pyglet.window.Window(width, height)

		self.vtx = pyglet.graphics.vertex_list(3 * VERTICES, 'v2i/stream', 'c3B/stream')

		# radius of outer "ring"
		outer_radius = (min(width, height) * 0.95) // 2

		circle_num = strip.count
		circle_step = 1.0 / circle_num

		angle = sin(pi / circle_num)
		inner_radius = int(outer_radius / (angle + 1))

		# radius of inner ring which all led circle's origin goes through
		self.circle_radius = int(0.9 * inner_radius * angle)

		self.led_pos = []
		center_x = width // 2
		center_y = height // 2

		for n in range(circle_num):
			s, c = sin(n * circle_step * TWO_PI), cos(n * circle_step * TWO_PI)
			self.led_pos.append((center_x + int(s * inner_radius), center_y + int(c * inner_radius)))

	def draw(self):
		self.window.dispatch_events()

		for index, ctx in enumerate(self.strip.leds):
			x_pos, y_pos = self.led_pos[index]
			verts = []

			# for each triangle
			for vert in range(VERTICES):
				verts += [
					x_pos, y_pos,
					x_pos + int(sin(STEP * vert * TWO_PI) * self.circle_radius), y_pos + int(cos(STEP * vert * TWO_PI) * self.circle_radius),
					x_pos + int(sin(STEP * (vert + 1) * TWO_PI) * self.circle_radius), y_pos + int(cos(STEP * (vert + 1) * TWO_PI) * self.circle_radius)
				]

			self.vtx.vertices = verts
			self.vtx.colors = ctx.tuple() * 3 * VERTICES
			self.vtx.draw(pyglet.gl.GL_TRIANGLES)

		self.window.flip()

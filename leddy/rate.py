def fade(led, color, duration=1.0):
	def ticker():
		r, g, b = color
		while led.elapsed < duration:
			frac = (duration - led.elapsed) / duration
			led.set(r * frac, g * frac, b * frac)
			yield

		led.off()

	return ticker()


def blink(led, color=(1.0, 1.0, 1.0), duration=1.0, attack=0.2):
	def ticker():
		inverse = 1.0 - attack
		while led.elapsed < duration:
			through = led.elapsed / duration
			frac = through / attack if through < attack else abs(((through - attack) / inverse) - 1.0)
			led.set(color[0] * frac, color[1] * frac, color[2] * frac)
			yield

		led.off()

	return ticker()


def linear(led, duration=1.0):
	def ticker():
		while led.elapsed < duration:
			frac = (duration - led.elapsed) / duration
			led.r, led.g, led.b = frac, frac, frac
			yield

		led.off()

	return ticker()

from .utils import hue


def full(color=(1.0, 1.0, 1.0), duration=1.0):
	def ticker(led):
		r, g, b = color
		while led.elapsed < duration:
			led.set(r, g, b)
			yield

		led.off()

	return ticker


def fade(color=(1.0, 1.0, 1.0), duration=1.0):
	def ticker(led):
		r, g, b = color
		while led.elapsed < duration:
			frac = (duration - led.elapsed) / duration
			led.set(r * frac, g * frac, b * frac)
			yield

		led.off()

	return ticker


def blink(color=(1.0, 1.0, 1.0), duration=1.0, attack=0.2):
	def ticker(led):
		inverse = 1.0 - attack
		r, g, b = color
		while led.elapsed < duration:
			through = led.elapsed / duration
			frac = through / attack if through < attack else abs(((through - attack) / inverse) - 1.0)
			led.set(r * frac, g * frac, b * frac)
			yield

		led.off()

	return ticker


def linear(duration=1.0):
	def ticker(led):
		while led.elapsed < duration:
			frac = (duration - led.elapsed) / duration
			led.set(frac, frac, frac)
			yield

		led.off()

	return ticker


def rotating_hue_full(start, duration=1.0, rate=1.0):
	def ticker(led):
		while led.elapsed < duration:
			color = hue(start + led.elapsed * rate)
			led.set(*color)
			yield

		led.off()

	return ticker
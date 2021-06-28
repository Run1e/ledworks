def fade(set, color=(1.0, 1.0, 1.0), duration=1.0):
	elapsed = 0

	def ticker(delta):
		nonlocal elapsed

		elapsed += delta

		if elapsed > duration:
			set(0, 0, 0)
			return True
		else:
			r, g, b = color
			frac = (duration - elapsed) / duration
			set(r * frac, g * frac, b * frac)

	return ticker

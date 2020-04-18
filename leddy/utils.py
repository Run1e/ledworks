def __hue(val):
	if val > 4.0:
		return 0.0
	elif val > 3.0:
		return abs(val - 4.0) # - 3.0 - 1.0
	elif val > 1.0:
		return 1.0
	else:
		return val


def hue(angle: float):
	angle = (angle % 1.0) * 6
	r = __hue((angle + 2.0) % 6.0)
	g = __hue(angle)
	b = __hue((angle + 4.0) % 6.0)
	return r, g, b
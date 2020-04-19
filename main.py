from random import randint

import leddy


class RandomLinear(leddy.Animation):
	@leddy.call_once_every(seconds=0.1)
	def test(self, interval):
		self.strip.assign_random(leddy.rate.linear, duration=3.0)


class HueComet(leddy.Animation):
	@leddy.cycle(seconds=1.0)
	def cycle(self, interval, led):
		self.strip.assign(led, leddy.rate.fade, color=leddy.utils.hue(self.time * 0.2), duration=randint(1, 3) / 10)

	@leddy.tick()
	def tick(self, delta):
		pass


class HueSpin(leddy.Animation):
	@leddy.cycle(seconds=1.0, reverse=True)
	def loop(self, interval, led):
		self.strip.assign(led, leddy.rate.fade, color=leddy.utils.hue(self.time * 0.82), duration=0.4)


if __name__ == '__main__':
	strip = leddy.Strip(128)
	player = leddy.PygletPlayer(strip, fps=None, timescale=1.0, width=640, height=640)
	player.play(HueComet)
# player.play_cycle(HueSpin(strip), HueComet(strip))

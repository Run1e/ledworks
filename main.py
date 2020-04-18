from random import randint

import leddy


class RandomLinear(leddy.Animation):
	@leddy.call_once_every(seconds=0.1)
	def test(self, now):
		self.strip.assign_random(leddy.rate.linear, duration=3.0)


class HueComet(leddy.Animation):
	@leddy.cycle(seconds=1.0)
	def loop(self, interval, led):
		self.strip.assign(led, leddy.rate.fade, color=leddy.utils.hue(self.time * 0.2), duration=randint(1, 3) / 10)


class HueSpin(leddy.Animation):
	@leddy.cycle(seconds=1.0)
	def loop(self, interval, led):
		self.strip.assign(led, leddy.rate.fade, color=leddy.utils.hue(self.time * 0.82), duration=0.4)


if __name__ == '__main__':
	strip = leddy.Strip(128)
	player = leddy.PygletPlayer(strip, fps=60, timescale=1.0)
	player.play(HueComet(strip))
	#player.play_cycle(HueSpin(strip), HueComet(strip))

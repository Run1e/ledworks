# ledworks

ledworks is a Python library for creating LED strip animations.


Example animation class:
```python
class HueComet(ledworks.Animation):
    @ledworks.cycle(seconds=4.0, reverse=False)
    def cycle(self, interval: float, led: ledworks.LEDContext):

        color = ledworks.utils.hue(self.time * 1.61)
        duration = randint(self.strip.count // 30, self.strip.count // 3) * interval
        
        self.strip.assign(
            led, ledworks.rate.fade(color=color, duration=duration)
        )
```

And its output on the PygletPlayer:

![HueComet](https://i.imgur.com/6G4gTey.gifv)

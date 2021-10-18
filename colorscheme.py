
class ColorScheme:
    pass

class AbsoluteVelocity(ColorScheme):
    def __init__(self, max=5):
        self.max = max

    def getHSB(self, v):
        av = abs(v)
        hue = av / self.max
        sat = (self.max-av) / (self.max / 3)
        bri = av / (self.max / 9)
        if hue > 1:
            hue = 1.0
        if sat > 1.0:
            sat = 1.0
        elif sat < 0:
            sat = 0.0
        if bri > 1.0:
            bri = 1.0
        return hue, sat, bri

import time
import pycom

pycom.heartbeat(False)

def hsv_to_rgb(h, s, v):
    if s == 0.0:
        return v, v, v
    i = int(h*6.0) # XXX assume int() truncates!
    f = (h*6.0) - i
    p = v*(1.0 - s)
    q = v*(1.0 - s*f)
    t = v*(1.0 - s*(1.0-f))
    i = i%6
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q

def rgb_to_hex(rgb):
    r,g,b = rgb
    return (int(r*255) << 16) + (int(g*255)<<8) + (int(b*255))

hue = 0
while True:
    col = rgb_to_hex(hsv_to_rgb(hue, .5, .1))
    pycom.rgbled(col)
    hue = (hue + .0001) % 1

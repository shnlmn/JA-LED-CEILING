import time
from noise import pnoise3
import neopixel

led_vars = {
    "mag": 5,
    "octaves": 2,
    "timing": 0.003,
    "min_bright": 0,
    "max_bright": 1.0,
    "x_drift": 0,
    "y_drift": 0,
    "blue_offset": 1000,
    "red_offset": 4000,
    "green_offset": 100,
    "red_bright": 255,
    "blue_bright": 255,
    "green_bright": 255
}

H = 12
W = 16

def interp(val, smin=0.0, smax=1.0, tmin=0.0, tmax=255.0):
    return ((abs(val) - smin) * (tmax - tmin) / (smax - smin)) + tmin

async def display_img(strip, count, **cfg):
    span = W * H
    z_shift = count * cfg["timing"]
    for i in range(W):
        for j in range(H):
            led_index = (W * H) - 1 - (i * H + j)
            if i % 2 == 0:
                j = (H - 1) - j
            y_dir = i * cfg["mag"] + (count * cfg["y_drift"])
            x_dir = j * cfg["mag"] + (count * cfg["x_drift"])
            b = interp(pnoise3((y_dir + cfg["blue_offset"]) / span,
                               (x_dir + cfg["blue_offset"]) / span,
                               z_shift, octaves=cfg["octaves"]),
                       0, 1, cfg["min_bright"] * 255,
                              cfg["blue_bright"] * cfg["max_bright"])
            r = interp(pnoise3((y_dir + cfg["red_offset"]) / span,
                               (x_dir + cfg["red_offset"]) / span,
                               z_shift, octaves=cfg["octaves"]),
                       0, 1, cfg["min_bright"] * 255,
                              cfg["red_bright"] * cfg["max_bright"])
            g = interp(pnoise3((y_dir + cfg["green_offset"]) / span,
                               (x_dir + cfg["green_offset"]) / span,
                               z_shift, octaves=cfg["octaves"]),
                       0, 1, cfg["min_bright"] * 255,
                              cfg["green_bright"] * cfg["max_bright"])
            strip[led_index] = (int(r), int(g), int(b))
    strip.show()

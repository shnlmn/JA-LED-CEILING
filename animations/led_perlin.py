import time
from noise import pnoise3
import neopixel
from config import LED_WIDTH, LED_HEIGHT

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

def interp(val, smin=0.0, smax=1.0, tmin=0.0, tmax=255.0):
    return ((abs(val) - smin) * (tmax - tmin) / (smax - smin)) + tmin

async def display_img(strip, count, **cfg):
    span = LED_WIDTH * LED_HEIGHT
    z_shift = count * cfg["timing"]
    for i in range(LED_WIDTH):
        for j in range(LED_HEIGHT):
            led_index = (LED_WIDTH * LED_HEIGHT) - 1 - (i * LED_HEIGHT + j)
            if i % 2 == 0:
                j = (LED_HEIGHT - 1) - j
            y_dir = i * cfg["mag"] + (count * cfg["y_drift"])
            x_dir = j * cfg["mag"] + (count * cfg["x_drift"])
            cfg["octaves"] = int(cfg["octaves"])
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

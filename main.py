import sys
#!/usr/bin/env python3
import time
import signal
import asyncio
import websockets
import board
import neopixel
from animations.led_perlin import led_vars as perlin_vars, display_img as perlin_img
from animations.led_fire import led_vars as fire_vars, display_img as fire_img

# LED strip configuration
LED_COUNT = 192        # Number of LED pixels
LED_PIN = board.D18    # GPIO pin connected to the pixels (must support PWM or be a hardware SPI pin)
LED_BRIGHTNESS = 1.0   # Brightness of the LEDs (0.0 to 1.0)
LED_AUTO_WRITE = False # Disable auto-show to manually control updates
PIXEL_ORDER = neopixel.GRB  # Pixel color order

# Animation registry
animations = {
    'perlin': (perlin_vars, perlin_img),
    'fire': (fire_vars, fire_img),
}
current_anim = 'perlin'

strip = None

def signal_handler(sig, frame):
    color_wipe(strip, (0, 0, 0))  # Turn off all LEDs
    sys.exit(0)

def color_wipe(strip, color):
    """Wipe color across display a pixel at a time."""
    for i in range(len(strip)):
        strip[i] = color
    strip.show()

async def listen(websocket, path):
    """
    Receives commands of format "key:value"
    e.g. "animation:fire" or "mag:5.0"
    """
    message = await websocket.recv()
    key, val = message.split(':', 1)

    if key == 'animation' and val in animations:
        global current_anim
        current_anim = val
        print(f"Switched animation to {val}")
    else:
        # Update led_vars of the active animation
        anim_vars, _ = animations[current_anim]
        try:
            anim_vars[key] = float(val)
            print(f"Updated {key} to {val} in {current_anim}")
        except ValueError:
            print(f"Invalid value for {key}: {val}")

async def run_animation():
    count = 0
    while True:
        anim_vars, anim_func = animations[current_anim]
        await anim_func(strip, count, **anim_vars)
        count += 1

if __name__ == '__main__':
    # Handle Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Initialize LED strip
    strip = neopixel.NeoPixel(
        LED_PIN, LED_COUNT,
        brightness=LED_BRIGHTNESS,
        auto_write=LED_AUTO_WRITE,
        pixel_order=PIXEL_ORDER
    )

    # Start WebSocket server on port 5555
    start_server = websockets.serve(listen, '0.0.0.0', 5555)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(start_server, run_animation()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    loop.close()


import sys
#!/usr/bin/env python3
import time
import signal
import asyncio
import websockets
import board
import neopixel
import json
from config import LED_WIDTH, LED_HEIGHT
from settings import ACTIVE_ANIMATIONS

current_anim = "perlin"

# LED strip configuration
LED_COUNT = LED_WIDTH*LED_HEIGHT        # Number of LED pixels
LED_PIN = board.D18    # GPIO pin connected to the pixels (must support PWM or be a hardware SPI pin)
LED_BRIGHTNESS = 1.0   # Brightness of the LEDs (0.0 to 1.0)
LED_AUTO_WRITE = False # Disable auto-show to manually control updates
PIXEL_ORDER = neopixel.GRB  # Pixel color order

strip = None

# Graceful shutdown signal handler
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
    Handles inbound messages, for example:
    "animation:perlin"
    "mag:4.2"
    "request_ui_schema:1"
    """
    async for message in websocket:
        
        global current_anim
        anim_dict = ACTIVE_ANIMATIONS[current_anim]
        print(current_anim)
        
        try:
            key, val = message.split(':', 1)
            print(f"Received: {message}")
            if key == 'animation' and val in ACTIVE_ANIMATIONS:
                current_anim = val
                anim_dict = ACTIVE_ANIMATIONS[val]
                print(f"Switched animation to {val}")
                ui_schema = anim_dict["ui_controls"]
                current_values = anim_dict["vars"]
                response = {
                    "ui_schema": ui_schema,
                    "current_values": current_values,
                }
                await websocket.send(json.dumps(response))
            elif key == 'request_ui_schema':
                #Return the UI schema for the current animation
                ui_schema = anim_dict["ui_controls"]
                current_values = anim_dict["vars"]
                response = {
                    "ui_schema": ui_schema,
                    "current_values": current_values,
                }
                await websocket.send(json.dumps(response))
            else:
                # Update led_vars of the active animation
                if key in anim_dict["vars"]:
                    try:
                        anim_dict["vars"][key] = float(val)
                        print(f"Updated {key} to {val} in {current_anim}")
                    except ValueError:
                        print(f"Invalid value for {key}: {val}")

        except Exception as e:
            print(f"Error processing message: {e}")

async def run_animation():
    count = 0
    while True:
        anim_vars = ACTIVE_ANIMATIONS[current_anim]["vars"]
        anim_func = ACTIVE_ANIMATIONS[current_anim]["func"]
        await anim_func(strip, count, **anim_vars)
        count += 1
        await asyncio.sleep(0)  # Allow other tasks to run

async def main():
    global strip

    # Initialize LED strip
    strip = neopixel.NeoPixel(
        LED_PIN, LED_COUNT,
        brightness=LED_BRIGHTNESS,
        auto_write=LED_AUTO_WRITE,
        pixel_order=PIXEL_ORDER
    )

    # Start WebSocket server
    server = await websockets.serve(listen, '0.0.0.0', 5555)
    print("WebSocket server started on ws://0.0.0.0:5555")

    # Run animation loop concurrently
    await asyncio.gather(server.wait_closed(), run_animation())

if __name__ == '__main__':
    # Handle Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Run the main event loop
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        color_wipe(strip, (0, 0, 0))  # Turn off all LEDs
        print("Program terminated.")



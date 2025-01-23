import random
import neopixel
from config import LED_WIDTH, LED_HEIGHT

led_vars = {
    "spark_chance": 0.05,
    "cooling": 5,
    "sparking": 50,
    "max_bright": 255
}

def clamp(value, min_value=0, max_value=255):
    """Clamp a value between min_value and max_value."""
    return max(min_value, min(value, max_value))

async def display_img(strip, count, **cfg):
    """Update LED matrix with random spark effect."""
    for i in range(LED_WIDTH):
        for j in range(LED_HEIGHT):
            # Random spark chance
            if random.random() < cfg["spark_chance"]:
                brightness = random.randint(cfg["max_bright"] // 2, cfg["max_bright"])
            else:
                brightness = random.randint(0, cfg["max_bright"] // 4)

            # Cooling effect
            brightness -= cfg["cooling"]
            brightness = clamp(brightness, 0, cfg["max_bright"])

            # Calculate LED index for serpentine layout
            led_index = (LED_WIDTH * LED_HEIGHT) - 1 - (i * LED_HEIGHT + j)
            # if i % 2 == 0:
            #     led_index = (i * LED_HEIGHT) + j

            # Set pixel color (red channel only for demonstration)
            strip[led_index] = (brightness, 0, 0)
    # Update LED strip
    strip.show()

from animations import led_perlin, led_fire
from config import LED_WIDTH, LED_HEIGHT


ACTIVE_ANIMATIONS = {
    "perlin": {
        "vars" :led_perlin.led_vars,
        "func": led_perlin.display_img,
        "ui_controls": {
            "mag": {
                "type": "range",
                "label": "Magnitude",
                "max": 10,
                "step": 1,
                
            },
            "octaves": {
                "type": "number",
                "label": "Octaves",
                "min": 1,
                "max": 8
            },
            # "timing": {
            #     "type": "range",
            #     "label": "Timing",
            #     "step": 1,
            # },
            "x_drift": {
                "type": "range",
                "label": "X Drift",
                "min": 0,
                "max": 10,
                "step": 0.1,
            },
            "y_drift": {
                "type": "range",
                "label": "Y Drift",
                "min": 0,
                "max": 10,
                "step": 0.1,
            },
        }
    },
    "fire": {
        "vars" :led_fire.led_vars,
        "func": led_fire.display_img,
        "ui_controls": {
            "spark_chance": {
                "type": "range",
                "label": "Spark Probability",
                "min": 0.0,
                "max": 1.00,
                "step": 0.01,
            },
            "cooling": {
                "type": "range",
                "label": "Cooling",
                "min": 0,
                "max": 100,
            },
            # "sparking": {
            #     "type": "range",
            #     "label": "Sparking",
            #     "min": 0,
            #     "max": 100,
            # },
        }
    }
}

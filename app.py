import sys
print(sys.platform)
if sys.platform == 'linux' in sys.platform:
    from fake_rpi.RPi import GPIO 
else:
    import RPi.GPIO as GPIO

from flask import Flask, render_template, request
import os

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

LED_PIN = 18
GPIO.setup(LED_PIN, GPIO.OUT)

pwm_led = GPIO.PWM(LED_PIN, 1000)
pwm_led.start(0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_brightness', methods=['POST'])
def set_brightness():
    brightness_str = request.form.get('brightness', '0')
    try:
        brightness = float(brightness_str)
    except ValueError:
        brightness = 0
    brightness = max(0, min(brightness, 100))
    pwm_led.ChangeDutyCycle(brightness)
    return "OK", 200

@app.route('/cleanup')
def cleanup():
    pwm_led.stop()
    GPIO.cleanup()
    return 'GPIO cleaned up'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

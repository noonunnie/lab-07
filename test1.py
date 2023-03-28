# lab 7
# using chatGPT

import time
import spidev
import RPi.GPIO as GPIO

# LED setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
led_pin = 17
GPIO.setup(led_pin, GPIO.OUT)

# MCP3008 setup
spi = spidev.SpiDev()
spi.open(0, 0)

# Grove light sensor setup
light_pin = 0  # connect to CH0 on MCP3008
threshold = 300  # experimentally determined threshold for light/dark

# Grove sound sensor setup
sound_pin = 1  # connect to CH1 on MCP3008
tap_threshold = 400  # experimentally determined threshold for tap detection

# Blink LED 5 times with on/off intervals of 500ms
for i in range(5):
    GPIO.output(led_pin, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(led_pin, GPIO.LOW)
    time.sleep(0.5)

# Read Grove light sensor for 5 seconds with intervals of 100ms
start_time = time.time()
while (time.time() - start_time) < 5:
    # read raw value from MCP3008
    light_value = spi.xfer2([1, (8 + light_pin) << 4, 0])
    light_raw = ((light_value[1] & 3) << 8) + light_value[2]

    # determine light/dark and print value
    if light_raw < threshold:
        print(f"{light_raw} - dark")
    else:
        print(f"{light_raw} - bright")
    
    time.sleep(0.1)

# Blink LED 4 times with on/off intervals of 200ms
for i in range(4):
    GPIO.output(led_pin, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(led_pin, GPIO.LOW)
    time.sleep(0.2)

# Read Grove sound sensor for 5 seconds with intervals of 100ms
start_time = time.time()
while (time.time() - start_time) < 5:
    # read raw value from MCP3008
    sound_value = spi.xfer2([1, (8 + sound_pin) << 4, 0])
    sound_raw = ((sound_value[1] & 3) << 8) + sound_value[2]

    # print raw value
    print(sound_raw)
    
    # check for tap
    if sound_raw > tap_threshold:
        print("Tap detected!")
    
    time.sleep(0.1)

# cleanup GPIO and SPI
GPIO.cleanup()
spi.close()

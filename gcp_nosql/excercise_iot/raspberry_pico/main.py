import machine
import utime
import random
import json  # Import JSON to format properly

# Setup ADC for temperature sensor
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / 65535  # Convert ADC value to voltage

# Detect if using Raspberry Pi Pico or Pico W
try:
    led = machine.Pin(25, machine.Pin.OUT)  # For Pico
except:
    led = machine.Pin("LED", machine.Pin.OUT)  # For Pico W

while True:
    # Read temperature
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706) / 0.001721  # Convert to Celsius
    random_on = random.uniform(1, 3)

    # Determine LED state
    led_on_off = 1 if random_on > 2 else 0
    led.value(led_on_off) 

    # Send properly formatted JSON
    data = {"temperature": round(temperature, 2), "led": led_on_off, "id": "raspberry_mac"}
    print(json.dumps(data))  

    # Wait before next reading
    utime.sleep(1)

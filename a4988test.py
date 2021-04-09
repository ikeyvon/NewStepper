from hx711 import HX711
import RPi.GPIO as GPIO
import time
from RpiMotorLib import RpiMotorLib


low_pressure_threshold=-1000###########################
high_pressure_threshold=36000###########################3

sensor_pins = [27,17] # [out,sck]##########################33

FORWARD_BUTTON_GPIO = 16##########################
BACKWARD_BUTTON_GPIO = 12##########################


#define GPIO pins
GPIO_pins = (14, 15, 18) # Microstep Resolution MS1-MS3 -> GPIO Pin
direction= 24       # Direction -> GPIO Pin
step = 23      # Step -> GPIO Pin


motor = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")


class pressure_sensor:
        def __init__(self,SensorPins):
            self.SensorPins = SensorPins                
            # HOW TO CALCULATE THE REFFERENCE UNIT
            # To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
            # In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
            # and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
            # If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
            #hx.set_reference_unit(113)
            referenceUnit = 100
            out = SensorPins[0]
            sck = SensorPins[1]
            self.hx = HX711(out, sck)
            self.hx.set_reading_format("MSB", "MSB")
            self.hx.set_reference_unit(referenceUnit)
            self.hx.reset()
            self.hx.tare()
#             while True:
#                 self.pressure = self.read_sensor_test()
#                 print(self.pressure)
#                 time.sleep(0.001)

        def read_sensor_test(self):
            val = self.hx.get_weight(5)
            self.hx.power_down()
            self.hx.power_up()
            return int(val)

sensor = pressure_sensor(sensor_pins)

GPIO.setmode(GPIO.BCM)

GPIO.setup(FORWARD_BUTTON_GPIO, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(BACKWARD_BUTTON_GPIO, GPIO.IN, pull_up_down = GPIO.PUD_UP)


motor.motor_go(clockwise=False, steptype="Full", steps=250, stepdelay=.005, verbose=False, initdelay=.05)

pressure = 1

while True:
#     print('HERE')
#     pressure = sensor.read_sensor_test()
#     
    if GPIO.input(FORWARD_BUTTON_GPIO) == True:
        print(1234567890)

    if GPIO.input(FORWARD_BUTTON_GPIO) == True  and pressure<=high_pressure_threshold:
        print('for')
        motor.motor_go(clockwise=False, steptype="Full", steps=100, stepdelay=.005, verbose=False, initdelay=.05)
        

    elif GPIO.input(BACKWARD_BUTTON_GPIO) == True  and pressure>=low_pressure_threshold:
        motor.motor_go(clockwise=True, steptype="Full", steps=100, stepdelay=.005, verbose=False, initdelay=.05)
        print('back')
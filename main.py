import Adafruit_DHT
from gpiozero import Button, LED
import RPi.GPIO as GPIO
from subprocess import check_call
import time

GPIO.setmode(GPIO.BCM)

sensor = Adafruit_DHT.DHT11
pin_sensor_hum = 18
pin_apagar_raspi = 27
pin_leds = 22
red = LED(23)
GPIO.setup(pin_leds, GPIO.IN, pull_up_down=GPIO.PUD_UP)


class SistemaCultivo:
    def __init__(self):
        self.boton_apagar_rap = Button(pin_apagar_raspi, hold_time=3)
        self.boton_apagar_rap.when_held = self.apagar_rap
        GPIO.add_event_detect(pin_leds, GPIO.BOTH, callback=self.boton_leds_apagar_y_prender, bouncetime=200)

    def sensor_humytemp(self):
        hum, temp = Adafruit_DHT.read_retry(sensor, pin_sensor_hum)
        return hum, temp

    def boton_leds_apagar_y_prender(self, channel):
        # Lógica para apagar o prender los LEDs
        if GPIO.input(pin_leds):
            red.on()
        else:
            red.off()

    def apagar_rap(self):
        # Lógica para apagar la Raspberry Pi
        check_call(['sudo', 'poweroff'])

    def ejecutar(self):
        while True:
            hum, temp = self.sensor_humytemp()
            print('temp={0:0.1f}C hum={1:0.1f}%'.format(temp, hum))
            time.sleep(0.1)


sistema_cultivo = SistemaCultivo()
sistema_cultivo.ejecutar()
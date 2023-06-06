# -*- coding: utf-8 -*-
import Adafruit_DHT
from gpiozero import Button, LED
import RPi.GPIO as GPIO
from subprocess import check_call
import time


class Humificador:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def encender(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def apagar(self):
        GPIO.output(self.pin, GPIO.LOW)


class TiraLED:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def encender(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def apagar(self):
        GPIO.output(self.pin, GPIO.LOW)


class SistemaCultivo:
    def __init__(self, pin_shutdown, btn_leds, sensor, pin_sensor_hum):
        self.btn_shutdown = Button(pin_shutdown, hold_time=3)
        self.btn_shutdown.when_held = self.apagar_rap
        GPIO.add_event_detect(
            btn_leds, GPIO.BOTH, callback=self.switch_tira_leds, bouncetime=200)  # bounce time para evitar rebotes
        self.sensor = sensor
        self.pin_sensor_hum = pin_sensor_hum

    def sensor_humytemp(self):
        hum, temp = Adafruit_DHT.read_retry(self.sensor, self.pin_sensor_hum)
        return hum, temp

    def switch_tira_leds(self, channel):
        # Lógica para apagar o prender los LEDs
        if GPIO.input(btn_leds):
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


GPIO.setmode(GPIO.BCM)
sensor = Adafruit_DHT.DHT11
pin_sensor_hum = 18
pin_shutdown = 27
btn_leds = 22
red = LED(23)
GPIO.setup(btn_leds, GPIO.IN, pull_up_down=GPIO.PUD_UP)

sistema_cultivo = SistemaCultivo(pin_shutdown, btn_leds, sensor, pin_sensor_hum)
sistema_cultivo.ejecutar()

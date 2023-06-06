import Adafruit_DHT
from gpiozero import Button,LED
import RPi.GPIO as GPIO
from subprocess import check_call
import time

GPIO.setmode(GPIO.BCM)

sensor = Adafruit_DHT.DHT11
pin_sensor_hum = 18
pin_apagar_raspi=27
pin_leds = 22
red = LED(23)
GPIO.setup(pin_leds, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def sensor_humytemp():
    hum, temp = Adafruit_DHT.read_retry(sensor,pin_sensor_hum)
    return hum, temp

def boton_huminificador(channel): # Función que se ejecuta cuando se presiona el botón
    pass

def boton_leds_apagar_y_prender(channel):
    # Lógica para apagar los LEDs
    if GPIO.input(pin_leds):     # if port 18 == 1
        red.on()
    else:                  # if port 18 != 1
        red.off()

def apagar_rap():
    # Lógica para apagar la Raspberry Pi
    check_call(['sudo', 'poweroff'])


def main():
    boton_apagar_rap = Button(pin_apagar_raspi, hold_time=3)
    boton_apagar_rap.when_held = apagar_rap
    GPIO.add_event_detect(pin_leds,GPIO.BOTH,callback=boton_leds_apagar_y_prender,bouncetime=200)
    while True:
        hum, temp = sensor_humytemp()
        print('temp={0:0.1f}C hum={1:0.1f}%'.format(temp, hum))
        time.sleep(0.1)

if __name__ == "__main__":
    main()
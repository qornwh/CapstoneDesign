import RPi.GPIO as GPIO
import time

def setting_gpio():
    GPIO.setmode(GPIO.BOARD)

def cleaning():
    GPIO.cleanup()
    

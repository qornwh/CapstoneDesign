import test_gpio

pin_servo = 32
servo = None

def setting():
    global servo
    test_gpio.GPIO.setup(pin_servo, test_gpio.GPIO.OUT)
    servo = test_gpio.GPIO.PWM(pin_servo, 50)
    servo.start(0)

def setMoterControl(speed):
    global servo
    servo.ChangeDutyCycle(speed)
    test_gpio.time.sleep(2)

def on():
    global servo
    servo.start(0)

def off():
    global servo
    servo.stop()
    
if __name__ == '__main__':
    import sys
    test_gpio.setting_gpio()
    setting()
    try:
        #7아래, 1우
        setMoterControl(1)
        off()
    except KeyboardInterrupt:
        test_gpio.cleaning()
        sys.exit() #종료

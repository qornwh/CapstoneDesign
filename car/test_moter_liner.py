import test_gpio

'''
A
24  in1
26  in2
22  speed
'''
pin_moter_A1 = 24
pin_moter_A2 = 26
pin_moter_AS = 22

moter_speed = 100
pwm_A = None

def setting():
    global pwm_A
    
    test_gpio.GPIO.setup(pin_moter_A1, test_gpio.GPIO.OUT)
    test_gpio.GPIO.setup(pin_moter_A2, test_gpio.GPIO.OUT)
    test_gpio.GPIO.setup(pin_moter_AS, test_gpio.GPIO.OUT)
    pwm_A = test_gpio.GPIO.PWM(pin_moter_AS, 200)

    pwm_A.start(0)
    
def liner_start():
    pwm_A.start(0)
    
    
def liner_stop():
    pwm_A.stop()

def setMoterControl(speed, stat):
    
    #foward
    if(stat == 1):
        test_gpio.GPIO.output(pin_moter_A1, test_gpio.GPIO.LOW)
        test_gpio.GPIO.output(pin_moter_A2, test_gpio.GPIO.HIGH)
        pwm_A.ChangeDutyCycle(speed) 

    #back
    elif(stat == 2):
        test_gpio.GPIO.output(pin_moter_A1, test_gpio.GPIO.HIGH)
        test_gpio.GPIO.output(pin_moter_A2, test_gpio.GPIO.LOW) 
        pwm_A.ChangeDutyCycle(speed) 

    #stop
    elif(stat == 5):
        pwm_A.ChangeDutyCycle(0) 
    
    test_gpio.time.sleep(2)

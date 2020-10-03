import test_gpio

'''
A
36  in1
38  in2
40  speed

B
33  speed
35  in3
37  in4
'''
pin_moter_A1 = 38
pin_moter_A2 = 36
pin_moter_AS = 40

pin_moter_B3 = 35
pin_moter_B4 = 37
pin_moter_BS = 33

moter_speed = 0

pwm_A = None
pwm_B = None

def setting():
    global pwm_A
    global pwm_B
    
    test_gpio.GPIO.setup(pin_moter_A1, test_gpio.GPIO.OUT)
    test_gpio.GPIO.setup(pin_moter_A2, test_gpio.GPIO.OUT)
    test_gpio.GPIO.setup(pin_moter_AS, test_gpio.GPIO.OUT)
    pwm_A = test_gpio.GPIO.PWM(pin_moter_AS, 100)
    
    test_gpio.GPIO.setup(pin_moter_B3, test_gpio.GPIO.OUT)
    test_gpio.GPIO.setup(pin_moter_B4, test_gpio.GPIO.OUT)
    test_gpio.GPIO.setup(pin_moter_BS, test_gpio.GPIO.OUT)
    pwm_B = test_gpio.GPIO.PWM(pin_moter_BS, 100)
    
    pwm_A.start(moter_speed)
    pwm_B.start(moter_speed)

def setMoterControl(speed, stat):
    #foward 1/6
    if(stat == 1):
        test_gpio.GPIO.output(pin_moter_A1, test_gpio.GPIO.HIGH)
        test_gpio.GPIO.output(pin_moter_A2, test_gpio.GPIO.LOW)
        
        test_gpio.GPIO.output(pin_moter_B3, test_gpio.GPIO.HIGH)
        test_gpio.GPIO.output(pin_moter_B4, test_gpio.GPIO.LOW)
        
        '''
        pwm_A.ChangeDutyCycle(speed+10) 
        pwm_B.ChangeDutyCycle(speed-30)
        test_gpio.time.sleep(0.2)
        '''
        pwm_A.ChangeDutyCycle(speed+5) 
        pwm_B.ChangeDutyCycle(speed-10)
        
        
    #back
    elif(stat == 2):
        test_gpio.GPIO.output(pin_moter_A1, test_gpio.GPIO.LOW)
        test_gpio.GPIO.output(pin_moter_A2, test_gpio.GPIO.HIGH) 
        
        test_gpio.GPIO.output(pin_moter_B3, test_gpio.GPIO.LOW)
        test_gpio.GPIO.output(pin_moter_B4, test_gpio.GPIO.HIGH)
        
        '''
        pwm_A.ChangeDutyCycle(speed+10) 
        pwm_B.ChangeDutyCycle(speed-30)
        '''
        pwm_A.ChangeDutyCycle(speed+15-10) 
        pwm_B.ChangeDutyCycle(speed-10)
        test_gpio.time.sleep(0.2)

    #right B
    elif(stat == 3):
        test_gpio.GPIO.output(pin_moter_B3, test_gpio.GPIO.HIGH)
        test_gpio.GPIO.output(pin_moter_B4, test_gpio.GPIO.LOW)

        pwm_A.ChangeDutyCycle(0) 
        pwm_B.ChangeDutyCycle(95)

    #left A
    elif(stat == 4):
        test_gpio.GPIO.output(pin_moter_A1, test_gpio.GPIO.HIGH)
        test_gpio.GPIO.output(pin_moter_A2, test_gpio.GPIO.LOW)

        pwm_A.ChangeDutyCycle(95) 
        pwm_B.ChangeDutyCycle(0)

    #back right B
    elif(stat == 6):
        test_gpio.GPIO.output(pin_moter_B3, test_gpio.GPIO.LOW)
        test_gpio.GPIO.output(pin_moter_B4, test_gpio.GPIO.HIGH)
        
        pwm_A.ChangeDutyCycle(0) 
        pwm_B.ChangeDutyCycle(95)

    #back left A
    elif(stat == 8):
        test_gpio.GPIO.output(pin_moter_A1, test_gpio.GPIO.LOW)
        test_gpio.GPIO.output(pin_moter_A2, test_gpio.GPIO.HIGH)
        
        pwm_A.ChangeDutyCycle(95) 
        pwm_B.ChangeDutyCycle(0)

    #stop
    elif(stat == 5):
        pwm_A.ChangeDutyCycle(0) 
        pwm_B.ChangeDutyCycle(0)
        test_gpio.time.sleep(0.1)
        return

    test_gpio.time.sleep(0.15)

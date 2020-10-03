import test_gpio as gp

clk_1 = 40
dir_1 = 38
#clk_2 = 36
#dir_2 = 32

front = 1
back  = 0

moter_speed = 0

pwm_1 = None
#pwm_2 = None

def setting_act():
    global pwm_1
    #global pwm_2
    gp.GPIO.setup(clk_1, gp.GPIO.OUT)
    gp.GPIO.setup(dir_1, gp.GPIO.OUT)
    #gp.GPIO.setup(clk_2, gp.GPIO.OUT)
    #gp.GPIO.setup(dir_2, gp.GPIO.OUT)
    
    gp.GPIO.output(dir_1, front)
    #gp.GPIO.output(dir_2, front)
    
    pwm_1 = gp.GPIO.PWM(clk_1, 1200)
    #pwm_2 = gp.GPIO.PWM(clk_2, 255)
    
    pwm_1.start(moter_speed)
    #pwm_2.start(moter_speed)
    
def setActControl(speed, stat):
    global pwm_1
    #global pwm_2
    #foward
    if(stat == 1):
        gp.GPIO.output(dir_1, front)
        #gp.GPIO.output(dir_2, front)
    
        pwm_1.ChangeDutyCycle(speed)
        #pwm_2.ChangeDutyCycle(speed)
    #back
    elif(stat == 2):
        gp.GPIO.output(dir_1, back)
        #gp.GPIO.output(dir_2, back)
    
        pwm_1.ChangeDutyCycle(speed)
        #pwm_2.ChangeDutyCycle(speed)
    #stop
    elif(stat == 3):
        pwm_1.ChangeDutyCycle(0)
        #pwm_2.ChangeDutyCycle(0)
        
import test_gpio as gp

aph = (3,5,7,11,13,15)

data_inerrupt = 0

def setting_approach():
    for i in aph:
        gp.GPIO.setup(i, gp.GPIO.IN, pull_up_down = gp.GPIO.PUD_UP)
    
def setting_interrupt():
    for i in aph:
        gp.GPIO.add_event_detect(i, gp.GPIO.FALLING, callback=app_inerrupt)

def remove_interrput():
    for i in aph:
        gp.GPIO.remove_event_detect(i)
    
def read_approach():
    data = []
    for i in aph:
        data = data +[gp.GPIO.input(i)]
    return data

def app_inerrupt(app_pin):
    global data_inerrupt
    #print(app_pin)
    #print(':번')
    data_inerrupt = app_pin
    
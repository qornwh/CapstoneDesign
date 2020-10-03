import test_gpio as gp
'''
app_1_2 = 22
app_2_2 = 24
app_3_2 = 26
app_4_2 = 32
'''
aph2 = [22]

data_inerrupt = 0

def setting_approach():
    for i in aph2:
        gp.GPIO.setup(i, gp.GPIO.IN, pull_up_down = gp.GPIO.PUD_UP)
    
def setting_interrupt():
    for i in aph2:
        gp.GPIO.add_event_detect(i, gp.GPIO.FALLING, callback=app_inerrupt)

def remove_interrput():
    for i in aph2:
        gp.GPIO.remove_event_detect(i)
    print('remove interrupt app2')
    
def read_approach():
    data = 0
    for i in aph2:
        data = data +[gp.GPIO.input(i)]
    return data

def app_inerrupt(app_pin):
    global data_inerrupt
    data_inerrupt = app_pin
    '''print(app_pin, ':번')'''
    
if __name__ == '__main__':
    import time 
    gp.setting_gpio()
    time.sleep(0.5)
    setting_approach()
    time.sleep(0.5)
    setting_interrupt()
    time.sleep(0.5)
    remove_interrput()
    time.sleep(0.5)
    setting_interrupt()
    time.sleep(0.5)
    remove_interrput()
    time.sleep(0.5)
    setting_interrupt()
    time.sleep(0.5)
    remove_interrput()
    time.sleep(0.5)
    setting_interrupt()
    time.sleep(0.5)
    remove_interrput()
    time.sleep(0.5)
    setting_interrupt()
    time.sleep(0.5)
    remove_interrput()
    
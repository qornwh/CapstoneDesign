import test_gpio as gp
import test_act as act
'''
limit_11 = 37
limit_13 = 35
limit_21 = 33
limit_23 = 31
limit_31 = 29
limit_33 = 23
limit_41 = 21
limit_43 = 19
'''
limit = [37,35,33,31,29,23,21,19]
data_inerrupt = 0

def setting_limit():
    for i in limit:
        gp.GPIO.setup(i, gp.GPIO.IN, pull_up_down = gp.GPIO.PUD_UP)

def setting_interrupt():
    for i in limit:
        gp.GPIO.add_event_detect(i, gp.GPIO.FALLING, callback=limit_inerrupt)

def remove_interrput():
    for i in limit:
        gp.GPIO.remove_event_detect(i)
    print('limit interrput remove')

def limit_inerrupt(limit_pin):
    global data_inerrupt
    #print(limit_pin, ':번')
    data_inerrupt = limit_pin
    
def read_limit():
    data = []
    for i in limit:
        data = data +[gp.GPIO.input(i)]
    return data

if __name__ == '__main__':
    gp.setting_gpio()
    setting_limit()
    setting_interrupt()
    
    while(True):
        i =1
    
    
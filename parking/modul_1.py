import test_gpio  as gp
import test_act   as act

gp.setting_gpio()
act.setting_act()

'''limit = [37,35,33,31,29,23,21,19, 22, 32]'''
limit = [21,23]
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

def limit_inerrupt(limit_pin):
    global data_inerrupt
    print(limit_pin, ':번')
    data_inerrupt = limit_pin
    
def read_limit():
    data = []
    for i in limit:
        data = data +[gp.GPIO.input(i)]
    return data

try:
    setting_limit()
    setting_interrupt()
    while(True):
        i = 1
        act.setActControl(90,2)
        if(data_inerrupt != 0):
            act.setActControl(0, 3)
            remove_interrput()
            break
        gp.time.sleep(0.2)

except KeyboardInterrupt:
    print('종료')
    
gp.cleaning()

'''
try:
    while(True):
        i =1
    
except KeyboardInterrupt:
    print('종료')
'''
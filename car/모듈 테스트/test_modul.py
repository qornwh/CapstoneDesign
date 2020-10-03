import test_gpio  as gpio
import test_line  as line
import test_jodo
import test_moter as moter
import threading
import test_servo
import test_moter_liner

gpio.setting_gpio()
line.setting()
test_jodo.setting()
moter.setting()
test_moter_liner.setting()
test_servo.setting()

gpio.time.sleep(3)

speed = 65
df = 2

def handler(channel):
    l,c,r = line.line_data()
    gpio.time.sleep(0.5)
    if(c == 0 and l == 0 and r == 0):
        moter.setMoterControl(0, 5)
        
while(True):
    l,c,r = line.line_data()

    #forward
    if(l == 1 and c == 0 and r == 1):
        #print("go1")
        moter.setMoterControl(speed, df)

    #right
    elif(l == 1 and r == 0):
        #print("go2")
        moter.setMoterControl(speed, 3)

    #left
    elif(l == 0 and r == 1):
        #print("go3")
        moter.setMoterControl(speed, 4)
        
    moter.setMoterControl(0, 5)
             
    if(l == 0 and c == 0 and r == 0):
        print("go4")
        break
    


gpio.cleaning()

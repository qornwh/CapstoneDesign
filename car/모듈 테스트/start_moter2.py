import test_gpio as gpio
import test_moter as moter
import test_line as line
import test_socket as client
import time
import sys

state = 0
speed = 40
name = 'car01'
runNum = 1
interrupData = False
'''
#  1num   |   2num
#         |
#  ----------------
#  3num   |   4num
#         |
#  ----------------
'''

def handler(channel):
    if(runNum == 1):
        l,c,r = line.line_data()
        if(c == 0 and l == 0 and r == 0):
            moter.setMoterControl(0, 5)
            print('interrup!!!!!!!')
        
def setting():
    gpio.setting_gpio()
    moter.setting()
    line.setting()
    #client.setting()

def ending():
    gpio.cleaning()

def openM():
    global state
    while(True):
        data = client.sendNrecv(name+' : open')
        if(int(data) > 0):
            state = state + 1
            break
        time.sleep(0.5)

def onM():
    global state
    while(True):
        data = client.sendNrecv(name+' : on')
        if(int(data) > 0):
            state = state + 1
            break
        time.sleep(0.5)

def checkM():
    global state
    while(True):
        data = client.sendNrecv(name+' : check')
        if(data.find('Ischecking') < 0):
            state = state + 1
            break
        time.sleep(0.5)

def runM():
    global state
    try:
        print("license number on")
        gpio.time.sleep(2);
        print("license number ok")

        print("send server : car on")
        gpio.time.sleep(1);
        print("recv server : go 4num")

        print("start parking~~")
        #interrup
        gpio.GPIO.add_event_detect(line.pin_otc, gpio.GPIO.FALLING, callback = handler)
        gpio.GPIO.add_event_detect(line.pin_otl, gpio.GPIO.FALLING, callback = handler)
        gpio.GPIO.add_event_detect(line.pin_otr, gpio.GPIO.FALLING, callback = handler)
        
        while(True):
            l,c,r = line.line_data()
            moter.setMoterControl(0, 5)
            #전부다 들어왔을떄
            if(c == 0 and l == 0 and r == 0):
                global interrupData
                gpio.GPIO.remove_event_detect(line.pin_otc)
                gpio.GPIO.remove_event_detect(line.pin_otl)
                gpio.GPIO.remove_event_detect(line.pin_otr)
                
                #지정 주차에 따라 오른쪽 왼쪽 앞쪽 판단 interrupt
                if(runNum%2 == 1 and runNum == interrupData):
                    print('번호 : ',runNum, '  rignt')
                    gpio.GPIO.add_event_detect(line.pin_otc, gpio.GPIO.FALLING, callback = handler)
                    while(True):
                        moter.setMoterControl(speed, 4)
                        moter.setMoterControl(0, 5)
                        l,c,r = line.line_data()
                        if(l == 1 and c == 0 and r == 1):
                            gpio.GPIO.remove_event_detect(line.pin_otc)
                            break
                elif(runNum%2 == 0 and runNum == interrupData):
                    print('번호 : ',runNum, '  left')
                    gpio.GPIO.add_event_detect(line.pin_otc, gpio.GPIO.FALLING, callback = handler)
                    while(True):
                        moter.setMoterControl(speed, 3)
                        moter.setMoterControl(0, 5)
                        l,c,r = line.line_data()
                        if(l == 1 and c == 0 and r == 1):
                            gpio.GPIO.remove_event_detect(line.pin_otc)
                            break
                else:
                    print('번호 : ',runNum, '  else')
                    gpio.GPIO.add_event_detect(line.pin_otl, gpio.GPIO.RISING, callback = handler)
                    gpio.GPIO.add_event_detect(line.pin_otr, gpio.GPIO.RISING, callback = handler)
                    while(True):
                        moter.setMoterControl(speed, 1)
                        moter.setMoterControl(0, 5)
                        l,c,r = line.line_data()
                        if(l == 1 and r == 1):
                            gpio.GPIO.remove_event_detect(line.pin_otl)
                            gpio.GPIO.remove_event_detect(line.pin_otr)
                            interrupData = interrupData + 2
                            break
                    
            #forward
            elif(l == 1 and c == 0 and r == 1):
                moter.setMoterControl(speed, 1)

            #right
            elif(l == 1 and r == 0):
                moter.setMoterControl(speed, 4)

            #left
            elif(l == 0 and r == 1):
                moter.setMoterControl(speed, 3)

            elif(l == 1 and c == 1 and r== 1):
                data = client.sendNrecv(name+' : arrive='+str(runNum))
                state = state + 1
                break
                
    except KeyboardInterrupt:
        ending()
        sys.exit()

def runT():
    print("start Deparking~~")
    #interrup
    gpio.GPIO.add_event_detect(line.pin_otc, gpio.GPIO.FALLING, callback = handler)
    gpio.GPIO.add_event_detect(line.pin_otl, gpio.GPIO.FALLING, callback = handler)
    gpio.GPIO.add_event_detect(line.pin_otr, gpio.GPIO.FALLING, callback = handler)

    while(True):
        l,c,r = line.line_data()
        moter.setMoterControl(0, 5)

        if(c+r+l != 0):
            moter.setMoterControl(speed, 2)
        else:
            break
    
        
if __name__ == '__main__':
    '''
    print('setting~~')
    setting()
    print('setting complate')
    
    try:
        while(True):
            if(state == 0):
                print('open')
                openM()

            elif(state == 1):
                print('on')
                onM()

            elif(state == 2):
                print('check')
                checkM()

            elif(state == 3):
                if(runNum % 2 == 1):
                    interrupData = runNum % 2
                else:
                    interrupData = 2
                print('main')
                runM()
                moter.setMoterControl(0, 5)

            else:
                time.sleep(4)
                print('end')
            
    except KeyboardInterrupt:
        ending()
        sys.exit()
    '''
    setting()
    runT()
    print('stop')
    


    




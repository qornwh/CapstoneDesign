import test_gpio     as gp
import test_limit    as limit
import test_act      as act
import test_approach as app
import test_approach2 as app2
import test_socket   as client
from park_state import pState, pEnum
import threading
import time

global sing, myPark
myPark = pState()
#up 0 down 1
sing = 0

def setting():
    gp.setting_gpio()
    limit.setting_limit()
    act.setting_act()
    app.setting_approach()
    app.setting_interrupt()
    app2.setting_approach()
    app2.setting_interrupt()
    limit.setting_interrupt()
    client.setting()
    
def ending():
    limit.remove_interrput()
    app2.remove_interrput()
    gp.cleaning()
    
def openM():
    global myPark
    while(True):
        data = client.sendNrecv(myPark.name()+' : open')
        if(int(data) > 0):
            myPark.setState(pEnum.open)
            break
        time.sleep(0.5)
        
def onM():
    global myPark
    data = app.read_approach()
    data = client.sendNrecv(myPark.name()+' : on='+str(data[0])+','+str(data[1])+','+str(data[2])+','+str(data[3])+','+str(data[4])+','+str(data[5]))
    if(data != ''):
        myPark.setState(pEnum.on)
        #time.sleep(0.5)
        
def onRun():
    #올라가는지 확인
    #올라가면 다시 내려갈떄 까지 대기
    #내려가라는 신호 받으면 내려감
    global myPark, sing
    if(sing == 0):
        data = client.sendNrecv(myPark.name()+' : run :'+'up')
        if(int(data) > 200):
            arg1 = int(data) - 200
            t = threading.Thread(target=onUp, args={arg1})
            t.start()
            return
    elif(sing == 1):
        data2 = client.sendNrecv(myPark.name()+' : run : '+'down')
        if(int(data2) > 0):
            arg1 = int(data2)
            t = threading.Thread(target=onDown, args={int(data2)})
            t.start()
            return
            
def onUp(data):
    global myPark, sing
    sing = -1
    myPark.setState(pEnum.up)
    #limit.setting_interrupt()
    #app2.setting_interrupt()
    limit.data_inerrupt = 0
    app2.data_inerrupt = 0
    if(data != 1):
        while(True):
            act.setActControl(95, 1)
            #time.sleep(0.2)
            delay_time(0.2)
            if(data == 2):
                if(app2.data_inerrupt == 22 ):
                    print(app2.data_inerrupt, 'ars')
                    act.setActControl(0, 3)
                    #time.sleep(0.5)
                    delay_time(0.5)
                    app2.data_inerrupt = 0
                    myPark.setFloor(2)
                    break
                        
            elif(data == 3):
                if(limit.data_inerrupt == 19 or limit.data_inerrupt == 23 or limit.data_inerrupt == 33 or limit.data_inerrupt == 37):
                    act.setActControl(0, 3)
                    #time.sleep(0.5)
                    delay_time(0.5)
                    limit.data_inerrupt  = 0
                    myPark.setFloor(3)
                    break
    else:
        myPark.setFloor(1)
    data = client.sendNrecv(myPark.name()+' : run,'+'stop')
    if(int(data) > 0):
        print('onUp 종료')
        #limit.remove_interrput()
        delay_time(0.5)
        #app2.remove_interrput()
        sing = 1
        
def onDown(data):
    global myPark, sing
    sing = -1
    myPark.setState(pEnum.down)
    #limit.setting_interrupt()
    #app2.setting_interrupt()
    limit.data_inerrupt = 0
    #app2.data_inerrupt = 0
    if(myPark.floor() != 1):
        while(True):
            act.setActControl(95, 2)
            #time.sleep(0.2)
            delay_time(0.2)
            if(limit.data_inerrupt == 31 or limit.data_inerrupt == 35 or limit.data_inerrupt == 29 or limit.data_inerrupt == 21):
                print(limit.data_inerrupt, 'is');
                act.setActControl(0, 3)
                #time.sleep(0.5)
                delay_time(0.5)
                myPark.setFloor(1)
                break
    else:
        myPark.setFloor(1)
    data = client.sendNrecv(myPark.name()+' : run,'+'stop')
    if(int(data) > 0):            
        print('onDown 종료')
        #limit.remove_interrput()      
        #app2.remove_interrput()      
        sing = 0
        delay_time(0.5)      
        
def delay_time(timeData):
    start_t = time.time()
    while(True):
        end_t = time.time()
        if((end_t-start_t)>=timeData):
            break
    #print('dalay time ',timeData)
        
        
if __name__ == '__main__':
    setting()
    openM()
    print('park')
    try:
        while(True):
            onM()
            onRun()
            #time.sleep(1)
            delay_time(1)
    except KeyboardInterrupt:
        print('keyboardInterrupt')
    except Exception as e:
        print('Error : ',e)
    ending()
    
    
    
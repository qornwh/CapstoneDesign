import test_gpio   as gpio
import test_moter  as moter
import test_line   as line
import test_socket as client
import test_jodo   as jodo
import test_servo  as servo
import test_moter_liner as liner
from state import pState as State
import sys

handle_data = 0

def handler(channel):
    l,c,r = line.line_data()
    gpio.time.sleep(0.5)
    if(c == 0 and l == 0 and r == 0):
        moter.setMoterControl(0, 5)

def handler2(channel):
    l,c,r = line.line_data()
    gpio.time.sleep(0.5)
    if(c == 0 and l == 0 and r == 0):
        moter.setMoterControl(0, 5)
        
def setting():
    gpio.setting_gpio()
    moter.setting()
    line.setting()
    client.setting()
    jodo.setting()
    servo.setting()
    liner.setting()

def ending():
    gpio.cleaning()
    client.sockClosing()

def arinit():
    servo.setMoterControl(7)
    gpio.time.sleep(1)

def goM():
    #주차할 경우, 빼내올 경우
    finsh = False
    try:
        while(True):
            #대기 주차장이 올라갈때 까지 #여기서 오류가 뜨는데..
            data1 = client.sendNrecv(State.name()+' : up')
            if(int(data1) > 0):
                _data = State.park_number()%10
                print(_data,'층 입니다')
                break
            gpio.time.sleep(1)

        liner.liner_start()
        while(True):
            #리니어 모터가 끝까지 나아갈 떄까지 2초 간격
            liner.setMoterControl(99,1)
            gpio.time.sleep(12)
            data2 = client.sendNrecv(State.name()+' : set')
            if(int(data2) > 0):
                liner.setMoterControl(0,5)
                break

        while(True):
            #서보 모터 아래로
            servo.setMoterControl(7)
            break

        i = 0 #변수 : 줄어들 시간
        while(True):
            #리니어 모터가 줄어들 떄까지 2초 간격
            liner.setMoterControl(99,2)
            if(i>5):
                print(data2,'자동차 주차 완료')
                break
            i = i +1
        liner.liner_stop()
            
        active('in')
        while(True):
            #대기 주차장이 내려갈떄 까지
            data3 = client.sendNrecv(State.name()+' : down')
            if(int(data3) > 0):
                print('주차 과정 완료')
                gpio.time.sleep(0.5)
                break
            gpio.time.sleep(1)
            
        finsh = True
    except Exception as e:
        print('예외가 발생했습니다.', e)
    
    return finsh

def backM():
    #주차할 경우, 빼내올 경우
    finsh = False
    try:
        while(True):
            #대기 주차장이 올라갈때 까지
            data1 = client.sendNrecv(State.name()+' : up')
            if(int(data1) > 0):
                print((State.park_number()%10),'층 입니다')
                gpio.time.sleep(1)
                break
            gpio.time.sleep(1)

        liner.liner_start()
        while(True):
            #리니어 모터가 끝까지 나아갈 떄까지 2초 간격
            liner.setMoterControl(99,1)
            gpio.time.sleep(12)
            data2 = client.sendNrecv(State.name()+' : set')
            if(int(data2) > 0):
                liner.setMoterControl(0,5)
                gpio.time.sleep(1)
                break

        while(True):
            #서보 모터 위로
            servo.setMoterControl(1)
            break

        i = 0 #변수 : 줄어들 시간
        while(True):
            #리니어 모터가 줄어들 떄까지 2초 간격
            liner.setMoterControl(99,2)
            if(i>5):
                print(data2,'자동차 빼기 완료')
                break
            i = i +1

        liner.liner_stop()
        active('out')
        while(True):
            #대기 주차장이 내려갈떄 까지
            data3 = client.sendNrecv(State.name()+' : down')
            if(int(data3) > 0):
                print('주차 빼기 과정 완료')
                gpio.time.sleep(0.5)
                break
            gpio.time.sleep(1)
            
        finsh = True
    except Exception as e:
        print('예외가 발생했습니다.', e)
    
    return finsh

def openM():
    while(True):
        data = client.sendNrecv(State.name()+' : open')
        if(int(data) > 0):
            State.stateChange()
            break
        gpio.time.sleep(0.5)

def onM():
    _type = False
    arinit()
    while(True):
        data = client.sendNrecv(State.name()+' : getOsend')

        if(int(data) > 0):
            State.setCarType(1)
            break
        else:
            jodo_data = jodo.jodo_data_d0()
            if(jodo_data == 1):
                print('자동차 탑재 완료')
                servo.setMoterControl(1)
                gpio.time.sleep(2)
                break

        gpio.time.sleep(1)

        
    if(State.car_type() == 0):
        while(True):
            data = client.sendNrecv(State.name()+' : on1')
            if(int(data) > 0):
                State.stateChange()
                break
            gpio.time.sleep(0.5)
            
    elif(State.car_type() == 1):
        while(True):
            data = client.sendNrecv(State.name()+' : on2')
            if(data.find('IsOn') < 0):
                State.stateChange(2)
                State.setCarNumber(data)
                print("자동차 뺴기")
                break
            else:
                break   

def checkM():
    while(True):
        data = client.sendNrecv(State.name()+' : check')
        if(data.find('Ischecking') < 0):
            State.setCarNumber(data)
            State.stateChange()
            break
        gpio.time.sleep(0.5)

def runM():
    global handle_data
    try:
        if(State.car_type() == 0):
            while(True):
                data = client.sendNrecv(State.name()+' : run')
                if(int(data) > 0):
                    State.setParkNumber(int(data))
                    break
                gpio.time.sleep(0.5)
        else:
            State.setParkNumber(int(State.car_number())) 
            
        #interrup
        gpio.GPIO.add_event_detect(line.pin_otl, gpio.GPIO.FALLING, callback = handler)
        gpio.GPIO.add_event_detect(line.pin_otr, gpio.GPIO.FALLING, callback = handler)
        print("start parking~~")
        
        while(True):
            l,c,r = line.line_data()

            #forward
            if(l == 1 and c == 0 and r == 1):
                #print("go1")
                moter.setMoterControl(State.speed(), 1)

            #right
            elif(l == 1 and r == 0):
                #print("go2")
                moter.setMoterControl(State.speed(), 4)

            #left
            elif(l == 0 and r == 1):
                #print("go3")
                moter.setMoterControl(State.speed(), 3)
                
            moter.setMoterControl(0, 5)
                
            if(l == 0 and c == 0 and r == 0):
                print("go4")
                #park_number에 10을 나누어 1번 주차장인지 2번 주차장인지 판단
                _park_number = int(State.park_number()/10)-1
                if(_park_number > handle_data):
                    handle_data = handle_data +1
                    moter.setMoterControl(State.speed(), 1)
                    gpio.time.sleep(0.6)
                    print(_park_number,"번 라인")
                else:
                    moter.setMoterControl(0, 5)
                    gpio.GPIO.remove_event_detect(line.pin_otl)
                    gpio.GPIO.remove_event_detect(line.pin_otr)
                    gpio.time.sleep(2)
                    print('인터럽트 해제 완료')
                    #빼내오는차 넣는차 검출
                    break

        _data = True
        if(State.car_type() == 0):
            arrive(str(State.park_number()), 'in')
            _data = goM()
        elif(State.car_type() == 1):
            arrive(str(State.park_number()), 'out')
            _data = backM()
        State.stateChange()
        State.setCarType(0)
                
    except KeyboardInterrupt:
        ending()
        sys.exit()

def arrive(number, value):
    while(True):
        data = client.sendNrecv(State.name()+' : arrive '+value+' = '+number)
        if(int(data) > 0):
            break
        gpio.time.sleep(0.5)

def active(value):
    while(True):
        data = client.sendNrecv(State.name()+' : active = '+value)
        if(int(data) > 0):
            break
        gpio.time.sleep(0.5)

def reset():
    #통신이 끊겼을때
    #제자리로 돌아간다
    #서보 모터 아래로
    gpio.time.sleep(0.5)
    servo.setMoterControl(7)
    gpio.time.sleep(2)

    gpio.GPIO.add_event_detect(line.pin_otl, gpio.GPIO.FALLING, callback = handler)
    gpio.GPIO.add_event_detect(line.pin_otr, gpio.GPIO.FALLING, callback = handler)
    try:   
        while(True):
            l,c,r = line.line_data()
            moter.setMoterControl(0, 5)

            #back
            if(l == 1 and c == 0 and r == 1):
                moter.setMoterControl(State.speed(), 2)

            #back right
            elif(l == 1 and r == 0):
                moter.setMoterControl(State.speed(), 6)

            #back left
            elif(l == 0 and r == 1):
                moter.setMoterControl(State.speed(), 8)

            #여기는 도착한 센서값 캐치후 on상태로 복귀
            if(l == 0 and c == 0 and r == 0):
                gpio.GPIO.remove_event_detect(line.pin_otl)
                gpio.GPIO.remove_event_detect(line.pin_otr)
                moter.setMoterControl(0, 5)
                State.setState(1)
                break

    except KeyboardInterrupt:
        ending()
        sys.exit()

def restart():
    global handle_data
    gpio.GPIO.add_event_detect(line.pin_otl, gpio.GPIO.FALLING, callback = handler2)
    gpio.GPIO.add_event_detect(line.pin_otr, gpio.GPIO.FALLING, callback = handler2)
    try:   
        while(True):
            l,c,r = line.line_data()

            #back
            if(l == 1 and c == 0 and r == 1):
                moter.setMoterControl(State.speed(), 2)

            #back right
            elif(l == 1 and r == 0):
                moter.setMoterControl(State.speed(), 6)

            #back left
            elif(l == 0 and r == 1):
                moter.setMoterControl(State.speed(), 8)
                
            moter.setMoterControl(0, 5)

            #여기는 도착한 센서값 캐치후 on상태로 복귀
            if(l == 0 and c == 0 and r == 0):
                print("restart handle : ",int(handle_data))
                if(handle_data != 0):
                    handle_data = handle_data - 1
                    moter.setMoterControl(State.speed(), 2)
                    gpio.time.sleep(0.6)
                    moter.setMoterControl(0, 5)
                elif(handle_data == 0):
                    gpio.GPIO.remove_event_detect(line.pin_otl)
                    gpio.GPIO.remove_event_detect(line.pin_otr)
                    gpio.time.sleep(0.5)
                    State.setState(10)
                    break

    except KeyboardInterrupt:
        ending()
        sys.exit()

def end():
    try:
        while(True):
            jodo_data = jodo.jodo_data_d0()
            if(jodo_data == 1):
                print('자동차를 빼세요')
                gpio.time.sleep(1)
            else:
                print('자동차 운반 완료')
                State.setState(1)
                break
                
    except KeyboardInterrupt:
        ending()
        sys.exit()
        
    #모든 과정 완료 5초 딜레이
    gpio.time.sleep(5)

if __name__ == '__main__':
    print('setting~~')
    setting()
    print('setting complate')
    
    try:
        while(True):
            if(State.state() == 0):
                print('open')
                openM()

            elif(State.state() == 1):
                print('on')
                onM()

            elif(State.state() == 2):
                print('check')
                checkM()

            elif(State.state() == 3):
                print('run_go')
                runM()

            elif(State.state() == 4):
                print('출발선으로')
                restart()

            elif(State.state() == 9):
                print('run_reset')
                reset()

            elif(State.state() == 10):
                print('run_end')
                end()
            
            else:
                gpio.time.sleep(4)
                print('close')
                
    except KeyboardInterrupt:
        ending()
        sys.exit()
    


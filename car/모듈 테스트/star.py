import test_gpio   as gpio
import test_moter  as moter
import test_line   as line
import test_socket as client
import test_jodo   as jodo
import test_servo  as servo
import test_moter_liner as liner
import state
import time
import sys

#자동차 상태
state = 0
#자동차 스피드
speed = 40
#자동차 이름
name = 'car01'
#자동차 위치 
park_number = 0
#자동차 번호판
car_number = ''
#인터럽트 출발선 1, 1번주차장 2, 2번 주차장 3
handle_data = 0
#빼낼 자동차, 넣을 자동차 판단 변수
car_type = 0

def handler(channel):
    global handle_data
    l,c,r = line.line_data()
    if(c == 0 and l == 0 and r == 0):
        moter.setMoterControl(0, 5)
        handle_data = handle_data + 1
        print('handle',handle_data)

def handler2(channel):
    global handle_data
    l,c,r = line.line_data()
    if(c == 0 and l == 0 and r == 0):
        moter.setMoterControl(0, 5)
        handle_data = handle_data - 1
        print('handle',handle_data)
        
def setting():
    gpio.setting_gpio()
    moter.setting()
    line.setting()
    client.setting()
    jodo.setting()
    servo.setting()
    liner.setting()
    arinit()

def ending():
    gpio.cleaning()

def arinit():
    servo.setMoterControl(12.5)
    time.sleep(2)

def goM():
    global car_type
    #주차할 경우, 빼내올 경우
    finsh = False
    try:
        while(True):
            #대기 주차장이 올라갈때 까지
            data1 = client.sendNrecv(name+' : up')
            if(int(data1) > 0):
                print((park_number%10),'층 입니다')
                break

        while(True):
            #리니어 모터가 끝까지 나아갈 떄까지 2초 간격
            liner.setMoterControl(99,1)
            time.sleep(12)
            data2 = client.sendNrecv(name+' : set')
            if(int(data2) > 0):
                liner.setMoterControl(0,5)
                break

        while(True):
            #서보 모터 아래로
            gpio.time.sleep(0.5)
            servo.setMoterControl(12.5)
            gpio.time.sleep(2)
            break

        i = 0 #변수 : 줄어들 시간
        while(True):
            #리니어 모터가 줄어들 떄까지 2초 간격
            liner.setMoterControl(99,2)
            if(i>5):
                print(data2,'자동차 주차 완료')
                break
            i = i +1

        while(True):
            #대기 주차장이 내려갈떄 까지
            data3 = client.sendNrecv(name+' : down')
            if(int(data3) > 0):
                print('주차 과정 완료')
                break
            
        finsh = True
    except Exception as e:
        print('예외가 발생했습니다.', e)
    
    return finsh

def backM():
    global car_type
    #주차할 경우, 빼내올 경우
    finsh = False
    try:
        while(True):
            #대기 주차장이 올라갈때 까지
            data1 = client.sendNrecv(name+' : up')
            if(int(data1) > 0):
                print((park_number%10),'층 입니다')
                time.sleep(1)
                break

        while(True):
            #리니어 모터가 끝까지 나아갈 떄까지 2초 간격
            liner.setMoterControl(99,1)
            time.sleep(12)
            data2 = client.sendNrecv(name+' : set')
            if(int(data2) > 0):
                liner.setMoterControl(0,5)
                time.sleep(1)
                break

        while(True):
            #서보 모터 위로
            gpio.time.sleep(0.5)
            servo.setMoterControl(1)
            gpio.time.sleep(2)
            break

        i = 0 #변수 : 줄어들 시간
        while(True):
            #리니어 모터가 줄어들 떄까지 2초 간격
            liner.setMoterControl(99,2)
            if(i>5):
                print(data2,'자동차 빼기 완료')
                break
            i = i +1

        while(True):
            #대기 주차장이 내려갈떄 까지
            data3 = client.sendNrecv(name+' : down')
            if(int(data3) > 0):
                print('주차 빼기 완료')
                break
            
        finsh = True
    except Exception as e:
        print('예외가 발생했습니다.', e)
    
    return finsh

def reset_stat():
    park_number = 0
    car_number = ''
    handle_data = 0
    car_type = 0

def openM():
    global state
    while(True):
        data = client.sendNrecv(name+' : open')
        if(int(data) > 0):
            state. = state + 1
            break
        time.sleep(0.5)

def onM():
    global state, car_type, car_number
    _type = False
    while(True):
        data = client.sendNrecv(name+' : getOsend')

        if(int(data) > 0):
            car_type = 1
            break
        else:
            jodo_data = gpio.GPIO.input(jodo.pin_jodo)
            if(jodo_data == 1):
                print('자동차 탑재 완료')
                servo.setMoterControl(1)
                time.sleep(2)
                break

        time.sleep(1)

        
    if(car_type == 0):
        while(True):
            data = client.sendNrecv(name+' : on1')
            if(int(data) > 0):
                state = state + 1
                break
            time.sleep(0.5)
            
    elif(car_type == 1):
        while(True):
            data = client.sendNrecv(name+' : on2')
            if(data.find('IsOn') < 0):
                state = state + 2
                car_number = data
                print("자동차 뺴기")
                break

def checkM():
    global state
    while(True):
        data = client.sendNrecv(name+' : check')
        if(data.find('Ischecking') < 0):
            car_number = data
            state = state + 1
            break
        time.sleep(0.5)

def runM():
    global state, park_number, car_type, handle_data
    try:
        #interrup
        gpio.GPIO.add_event_detect(line.pin_otl, gpio.GPIO.FALLING, callback = handler)
        gpio.GPIO.add_event_detect(line.pin_otr, gpio.GPIO.FALLING, callback = handler)
        print("start parking~~")
        
        while(True):
            l,c,r = line.line_data()
            moter.setMoterControl(0, 5)

            #forward
            if(l == 1 and c == 0 and r == 1):
                print("go1")
                moter.setMoterControl(speed, 1)

            #right
            elif(l == 1 and r == 0):
                print("go2")
                moter.setMoterControl(speed, 4)

            #left
            elif(l == 0 and r == 1):
                print("go3")
                moter.setMoterControl(speed, 3)
                
            if(l == 0 and c == 0 and r == 0):
                print("go4")
                moter.setMoterControl(0, 5)
                #park_number에 10을 나누어 1번 주차장인지 2번 주차장인지 판단
                _park_number = int(park_number/10)+1
                if(_park_number != handle_data):
                    moter.setMoterControl(speed, 1)
                    time.sleep(0.5)
                else:
                    gpio.GPIO.remove_event_detect(line.pin_otl)
                    gpio.GPIO.remove_event_detect(line.pin_otr)
                    #빼내오는차 넣는차 검출
                    _data = True
                    if(car_type == 0):
                        _data = goM()
                    elif(car_type == 1):
                        _data = backM()
                    if(_data == True):
                        #제자리로
                        print('남은 주차 확인')
                        state = state + 1
                        car_type = 0
                    else:
                        #초기화 , 종료 
                        print('초기화')
                    moter.setMoterControl(0, 5)
                    break
                
    except KeyboardInterrupt:
        ending()
        sys.exit()

def reset():
    #통신이 끊겼을때
    #제자리로 돌아간다
    #서보 모터 아래로
    gpio.time.sleep(0.5)
    servo.setMoterControl(12.5)
    gpio.time.sleep(2)

    global state
    gpio.GPIO.add_event_detect(line.pin_otl, gpio.GPIO.FALLING, callback = handler)
    gpio.GPIO.add_event_detect(line.pin_otr, gpio.GPIO.FALLING, callback = handler)
    try:   
        while(True):
            l,c,r = line.line_data()
            moter.setMoterControl(0, 5)

            #back
            if(l == 1 and c == 0 and r == 1):
                moter.setMoterControl(speed, 2)

            #back right
            elif(l == 1 and r == 0):
                moter.setMoterControl(speed, 6)

            #back left
            elif(l == 0 and r == 1):
                moter.setMoterControl(speed, 8)

            #여기는 도착한 센서값 캐치후 on상태로 복귀
            if(l == 0 and c == 0 and r == 0):
                gpio.GPIO.remove_event_detect(line.pin_otl)
                gpio.GPIO.remove_event_detect(line.pin_otr)
                moter.setMoterControl(0, 5)
                state = 1
                break

    except KeyboardInterrupt:
        ending()
        sys.exit()

def restart():
    global state
    gpio.GPIO.add_event_detect(line.pin_otl, gpio.GPIO.FALLING, callback = handler2)
    gpio.GPIO.add_event_detect(line.pin_otr, gpio.GPIO.FALLING, callback = handler2)
    try:   
        while(True):
            l,c,r = line.line_data()
            moter.setMoterControl(0, 5)

            #back
            if(l == 1 and c == 0 and r == 1):
                moter.setMoterControl(speed, 2)

            #back right
            elif(l == 1 and r == 0):
                moter.setMoterControl(speed, 6)

            #back left
            elif(l == 0 and r == 1):
                moter.setMoterControl(speed, 8)

            #여기는 도착한 센서값 캐치후 on상태로 복귀
            if(l == 0 and c == 0 and r == 0):
                moter.setMoterControl(0, 5)
                if(handle_data != 0):
                    moter.setMoterControl(speed, 1)
                    time.sleep(0.5)
                elif(handle_data == 0):
                    gpio.GPIO.remove_event_detect(line.pin_otl)
                    gpio.GPIO.remove_event_detect(line.pin_otr)
                    state = 10
                    break

    except KeyboardInterrupt:
        ending()
        sys.exit()

def end():
    global state
    reset_stat()
    try:
        while(True):
            jodo_data = gpio.GPIO.input(jodo.pin_jodo)
            if(jodo_data == 1):
                print('자동차를 빼세요')
            else:
                print('자동차 운반 완료')
                state = 1
                break
                
    except KeyboardInterrupt:
        ending()
        sys.exit()
        
    #모든 과정 완료 5초 딜레이
    time.sleep(5)

if __name__ == '__main__':
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
                print('run_go')
                runM()

            elif(state == 4):
                print('출발선으로')
                restart()

            elif(state == 9):
                print('run_reset')
                reset()

            elif(state == 10):
                print('run_end')
                end()
            
            else:
                time.sleep(4)
                print('close')
                
    except KeyboardInterrupt:
        ending()
        sys.exit()
    

import select
import socket
import sys
import threading
import numbering as number
import multi
import time
from mongo import box as DB

#ex)
#'ip' 'c1=msg'
#ip: name
clientMap = {}
#ip:'번호판'
licenseMap = {'car01': ''}
#''자리':번호판'
licensePark = {11: '', 12: '', 13: '', 21: '', 22: '', 23: ''}
# 주차장자리: 상태(비었음, 주차중, 나오는중, 있음) 1 2 3 4
parkingMap = {11: 1, 12: 1, 13: 1, 21: 1, 22: 1, 23: 1}
#db
db = DB()

class Server():
    def __init__(self):
        self.ip = self.ipcheck()
        self.port = 55555
        self.size = 1024

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(False)
        self.server.bind((self.ip, self.port))
        self.server.listen()
        self.input_list = [self.server]

        self.asi = dataAsi()

    def ipcheck(self):
        return socket.gethostbyname(socket.getfqdn())

    def run(self):
        while True:
            input_ready, write_ready, except_ready = select.select(self.input_list, [], [])
            for ir in input_ready:
                if ir == sys.stdin:
                    junk = sys.stdin.readline()
                    print(junk, flush=True)

                elif(ir == self.server):
                    client, address = self.server.accept()
                    print(address, 'is connected', flush=True)
                    self.input_list.append(client)
                else:
                    data = ir.recv(self.size)
                    if data:
                        _data = data.decode()
                        print(ir.getpeername(), 'recv :', _data, flush=True)
                        code = self.asi.ParseMsg(ir.getpeername(), _data)
                        ###
                        if(code > 100 and code < 130):
                            ir.send(str(code-100).encode())
                        elif(code == -1):
                            print('error')
                            ir.send('error'.encode())
                        elif(code == -12):
                            ir.send('Ischecking'.encode())
                        elif(code == 12):
                            _number = licenseMap.get(_data[:5])
                            ir.send(str(_number).encode())
                            print(_number, " ", _data[:5])
                        elif(code == 31 or code == 32):
                            ir.send(self.__dicToString().encode())
                        elif(code > 300 and code < 330):
                            _number = code - 300
                            ir.send(str(_number).encode())
                        elif(code == -35):
                            ir.send(str('이미 나오기 준비 or 나오는 중입니다').encode())
                        else:
                            ir.send(str(code).encode())
                        ###
                    else:
                        global clientMap
                        key = self.__findKey(ir.getpeername())
                        clientMap[key] = ''
                        print(key,' : ',ir.getpeername(), 'close', flush=True)
                        ir.close()
                        if(str(key).find('park') > -1):
                            self.asi.park_setting()
                        self.input_list.remove(ir)

    def __findKey(self, value):
        global clientMap
        result = ''
        for name, ip in clientMap.items():
            if(ip == value):
                result = name
                break
            else:
                result = -1
                break
        return result

    def __findSocket(self, ip):
        for body in self.input_list.__iter__():
            print("body : ",body)
            __str = str(body)
            if(__str.find(str(ip))>0):
                body.send('ok'.encode())

    def __dicToString(self):
        global parkingMap
        _data = '{'
        for key, val in parkingMap.items():
            _data += str(key)+':'+str(val)+','
        _data = _data[:-1]
        _data += '}'
        return _data

    def __del__(self):
        self.server.close()
        print('server stop')

class dataAsi():
    def __init__(self):
        super()
        self.num = number.License()
        self.multi = multi.multi()
        #car 부분에서쓰는 임시적으로 위치 저장 변수
        self._bup = -1
        #엘리베이터 층수를 임시적으로 저장 변수
        self._elevator = -1
        #주차후 엘리베이터를 움직이기 위한 if용도 변수
        self._onoffelevator = False
        #up 1, down 2, stop 3
        self._updown = -1
        #엘리베이터가 내려오고 주차장 주차장 dic 변수값이 바뀔때 사용하는 변수
        self._appelv = 0

    def park_setting(self):
        self._onoffelevator = False
        self._updown = -1
        self._elevator = -1
        self._appelv = 0

    def car_setting(self):
        self._bup = -1

    #주차공간 찾는 함수
    def __findParkingCar(self):
        global parkingMap
        for key, val in parkingMap.items():
            if(key == 1):
                return val
        return -1

    def ParseMsg(self, ip, msg):
        global clientMap, parkingMap, licensePark
        if(msg.find('car') > -1):
            if(msg.find('open') > -1):
                self.car_setting()
                clientMap[msg[:5]] = ip
                print(msg[:5], ' : ', clientMap.get(msg[:5]), flush=True)
                print('자동차 등록 완료')
                return 10
            elif(msg.find('getOsend') > -1):
                if(self.multi.consum() > 0):
                    return 15
                else:
                    return -15
            elif(msg.find('on1') > -1):
                #스레드 실행, 촬영 시작, 번호판 인식 시작, -1 이미지 처리 끝내지 못함 다시 요청하게 만듬
                _thread = threading.Thread(target=self.num.imgProcessing, args={'samples/LicensePlate/test003.jpg'})
                _thread.start()
                return 11
            elif (msg.find('on2') > -1):
                #빼내야할 번호 전송
                _testdata = self.multi.getVal()
                if(parkingMap[_testdata] < 4):
                    return 0
                self._bup = _testdata
                #가야할 층수
                self._elevator = _testdata%10
                print('test',_testdata)
                if(_testdata != 0):
                    print('test',_testdata)
                    DB.db_add(db, msg[:5], time.strftime('%x', time.localtime(time.time())), licensePark[self._bup]+' out')
                    licensePark[self._bup] = ''
                    #나오는중 상태변경
                    parkingMap[self._bup] = 3
                    return 100+_testdata
                else:
                    return 0
            elif(msg.find('check') > -1):
                if(self.num.number != "-1"):
                    licenseMap[msg[:5]] = self.num.number
                    print('번호판 등록 완료', self.num.number)
                    #db 추가
                    DB.db_add(db, msg[:5], time.strftime('%x', time.localtime(time.time())), self.num.number+' in')
                    return 12
                else:
                    #번호판 인식중
                    print('번호판 인식중')
                    return -12
            elif (msg.find('up') > -1):
                #주차 위치 찾기, 엘리베이터에게 데이터를 보내 전부 올라갈떄 까지 기다라기
                #층수 찾기
                #층수 리턴 ex) 호수+층수
                #엘리베이터가 일정 층수에 맞는 곳에 도착하면 16 / 아니면 -100
                if(self._updown == 3):
                    return 16
                else:
                    return -16
            elif (msg.find('down') > -1):
                #엘리베이터가 1층에 도착하면 17 / 아니면 -100
                #엘리베이터 변수 초기화
                if(self._updown == 3):
                    if(self._bup == 3):
                        parkingMap[self._bup] = 1
                        licensePark[self._bup] = ''
                    elif(self._bup == 2):
                        parkingMap[self._bup] = 4
                    self._elevator = -1
                    self._bup = -1
                    self._appelv = 1
                    return 17
                else:
                    return -17
            elif (msg.find('set') > -1):
                #주차위치의 주차장의 근접센서 값이 변하면 18 / 아니면 -100
                return 18
            elif(msg.find('run') > -1):
                # 11으로 가라,12으로 가라, 13으로 가라, 21으로 가라, 22으로 가라, 23으로 가라
                _testdata = -1
                print('run')
                for key, val in parkingMap.items():
                    if(key == 11):
                        key = 12
                        val = parkingMap[key]
                    elif(key == 12):
                        key = 13
                        val = parkingMap[key]
                    elif(key == 13):
                        key = 11
                        val = parkingMap[key]
                    elif(key == 21):
                        key = 22
                        val = parkingMap[key]
                    elif(key == 22):
                        key = 23
                        val = parkingMap[key]
                    elif(key == 23):
                        key = 21
                        val = parkingMap[key]
                    if(val == 1):
                        _testdata = key
                        if(self.num.number != '-1'):
                            licensePark[key] = self.num.number
                            self.num.number = '-1'
                            #주차중 상태변경
                            parkingMap[_testdata] = 2
                            print("licensePark",key," :: ",licensePark[key])
                            break
                if(_testdata != -1):
                    self._bup = _testdata
                    self._elevator = _testdata%10
                    return 100+_testdata
                else:
                    return -13
            elif(msg.find('arrive') > -1):
                _msg = msg.split('=')
                if (_msg[1] != None and _msg[0].find('in') > -1):
                    #어떤자리에 도착했는지 수신
                    parkingMap[int(_msg[1])] = 2
                    _data = _msg[1]
                    self._onoffelevator = True
                elif(_msg[1] != None and _msg[0].find('out') > -1):
                    # 어떤자리에 도착했는지 수신
                    parkingMap[int(_msg[1])] = 3
                    _data = _msg[1]
                    self._onoffelevator = True
                else:
                    return -14
                # self._updown 초기화
                self._updown = -1
                print(msg[:5],' : 도착')
                return 14
            elif (msg.find('active') > -1):
                _msg = msg.split('=')
                if (_msg[1].find('in') > -1):
                    if(self._bup != 1):
                        self._onoffelevator = True
                elif (_msg[1].find('out') > -1):
                    if(self._bup != 1):
                        self._onoffelevator = True
                else:
                    return -14
                #self._updown 초기화
                self._updown = -1
                print(msg[:5], ' : 도착')
                return 14

            elif(msg.find('wait') > -1):
                print(msg[:5],' : 대기중')
                return 14
            else:
                return -1

        elif(msg.find('park') > -1):
            if (msg.find('open') > -1):
                self.park_setting()
                clientMap[msg[:4]] = ip
                print('주차장 등록 완료')
                return 20
            elif(msg.find('on') > -1):
                #주차장은 1초 간격으로 갱신된 빈자리 값을 보내준다
                _msg = msg.split('=')
                if(_msg[1] != ''):
                    __msg = _msg[1].split(',')
                    #print('__msg',__msg,' len = ', len(__msg))
                    i = 0
                    if(self._appelv == 1):
                        for parking, val in parkingMap.items():
                            if (val == 5):
                                if (int(__msg[i]) == 1):
                                    __msg[i] = '1'
                                    parkingMap[parking] = int(__msg[i])
                            else:
                                if (int(__msg[i]) == 0):
                                    __msg[i] = '4'
                                parkingMap[parking] = int(__msg[i])
                            i = i + 1
                            self._appelv = 0
                        return 21

                    for parking, val in parkingMap.items():
                        if(val == 2):
                            if (int(__msg[i]) == 0):
                                __msg[i] = '4'
                                parkingMap[parking] = int(__msg[i])
                        elif(val == 3):
                            if (int(__msg[i]) == 1):
                                __msg[i] = '1'
                                parkingMap[parking] = int(__msg[i])
                        elif(val == 5):
                            if (int(__msg[i]) == 1):
                                __msg[i] = '1'
                                parkingMap[parking] = int(__msg[i])
                        else:
                            if (int(__msg[i]) == 0):
                                __msg[i] = '4'
                            parkingMap[parking] = int(__msg[i])
                        i = i + 1
                    return 21
                else:
                    print('변한값 없음')
                    return -21
            elif(msg.find('run') > -1):
                if(msg.find('up') > -1):
                    if(self._elevator >= 1 and self._onoffelevator == True):
                        print('엘리베이터 up 작동')
                        print('updown',self._updown,'ele',self._elevator)
                        _data = self._elevator
                        self._updown = 1
                        self._elevator = 1
                        self._onoffelevator = False
                        return  200+_data
                    else:
                        return -25
                elif(msg.find('down') > -1):
                    if(self._elevator == 1 and self._onoffelevator == True):
                        print('엘리베이터 down 작동')
                        print('updown',self._updown,'ele',self._elevator)
                        self._updown = 2
                        self._onoffelevator = False
                        return 24
                    else:
                        return -24
                elif(msg.find('stop') > -1):
                    print('ele stop')
                    self._updown = 3
                    return 23
                return -1
            elif(msg.find('led') > -1):
                _msg = msg.split('=')
                __msg = _msg.split(',')
                print(__msg[0]+'번 켜짐')
                return 22
            else:
                return -1

        elif (msg.find('gui') > -1):
            if (msg.find('open') > -1):
                clientMap[msg[:3]] = ip
                print('터치 패널 등록 완료')
                return 30
            elif (msg.find('on') > -1):
                # 터치 패널이 세팅이 완료되고 주차장 정보를 요청하는 메시지
                return 31
            elif (msg.find('tick') > -1):
                # 터치 패널이 주기적으로 주차장 정보를 요청하는 메시지
                return 32
            elif (msg.find('find') > -1):
                _msg = msg.split('=')
                if (len(_msg) > 1):
                    #여기서 dict에서 찾아서 리턴으로 보낸다
                    _str = int(_msg[1])
                    _number = -1
                    for key, val in licensePark.items():
                        if(val == _str or key == _str):
                            _number = key
                            if (parkingMap[_number] != 4):
                                return -33
                            print('12')
                    return 300+_number
                return -33
            elif (msg.find('out') > -1):
                _msg = msg.split('=')
                if (len(_msg) > 1):
                    _str = str(_msg[1]).strip()
                    _number = -1

                    if(msg.find('master') > -1):
                        _str = int(_msg[1][-2:])
                        print('master ',_str)
                        for key, val in licensePark.items():
                            if (key == _str):
                                _number = key
                                if (parkingMap[_number] == 5):
                                    print('이미 빼내기 준비중 입니다')
                                    return -35
                                if (parkingMap[_number] != 4):
                                    return -34
                                self.multi.produce(_number)
                                parkingMap[_number] = 5
                                print(self.multi.q.qsize())
                    else:
                        for key, val in licensePark.items():
                            if (val == _str):
                                _number = key
                                if (parkingMap[_number] == 5):
                                    print('이미 빼내기 준비중 입니다')
                                    return -35
                                if (parkingMap[_number] != 4):
                                    return -34
                                self.multi.produce(_number)
                                parkingMap[_number] = 5
                                print(self.multi.q.qsize())
                    return 300 + _number
                return -34
            else:
                return -1

        elif (msg.find('phone') > -1):
            if (msg.find('open') > -1):
                clientMap[msg[:5]] = ip
                print('phone 등록 완료')
                return 40
            elif (msg.find('out') > -1):
                _msg = msg.split('=')
                if (len(_msg) > 1):
                    _str = str(_msg[1]).strip()
                    _number = -1

                    if(msg.find('master') > -1):
                        _str = int(_msg[1])
                        print('master')
                        for key, val in licensePark.items():
                            if (key == _str):
                                _number = key
                                if (parkingMap[_number] == 5):
                                    print('이미 빼내기 준비중 입니다')
                                    return -35
                                if (parkingMap[_number] != 4):
                                    return -34
                                self.multi.produce(_number)
                                parkingMap[_number] = 5
                                print(self.multi.q.qsize())
                    else:
                        for key, val in licensePark.items():
                            if (val == _str):
                                _number = key
                                if (parkingMap[_number] == 5):
                                    print('이미 빼내기 준비중 입니다')
                                    return -35
                                if (parkingMap[_number] != 4):
                                    return -34
                                self.multi.produce(_number)
                                parkingMap[_number] = 5
                                print(self.multi.q.qsize())
                    return 300 + _number
                return -34
            else:
                return -1
        else:
            return -1

    def __del__(self):
        print('dataAsi class del')

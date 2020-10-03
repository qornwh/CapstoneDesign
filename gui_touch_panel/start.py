from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QLineEdit
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QImage
import urllib.request as req, sys, time
from mainWindow import Ui_mainWindow
import cv2
import ast
import my_camera as mycamera
import my_socket as mysock
import Loading as myload
import fireDB
import os

'''
1                      2                               3                            4                   5
회색 : 자동차 없음  ||  노란색 : 주차중(들어오는중)  ||  파란색 : 자동차 나오는 중  ||  빨간색 : 주차됨  || 녹색 : 자동차 나오기 대기중
---------------------------------------------------------------------------------------------------------------------------------
딕셔너리 
ex {1:(14마1234,2), 2:('',1), 3:('',1), 4:('',1)}
'''

class testW(QWidget ,Ui_mainWindow):
    camera_slot_start = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #주차 위치 데이터 딕셔너리
        self.park_dic = {11:1, 12:1, 13:1, 21:1, 22:1, 23:1}
        mysock.setting()
        self.firepy = fireDB.Firepy()
        _data = mysock.sendNrecv('gui : open')
        self.setting()
        #이 타이머는 1초 간격으로 서버로 주차위치 데이터 수신
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.onQ)
        self.timer.start()
        #카메리 시작, 종료 확인 변수
        self.runnig_camera = False
        #self.show()

    def setting(self):
        _data = mysock.sendNrecv('gui : on')
        self.setParkDic()
        #self.lineEdit.setEchoMode(QLineEdit.Password)
        #카메라 로딩 이미지 출력
        self._mycamera = mycamera.camera(self)
        _qPixmap = QPixmap("known/load.png")
        # self.lb_camera.resize(_qPixmap.width(), _qPixmap.height())
        _qPixmap =_qPixmap.scaled(self.lb_camera.width(), self.lb_camera.height())
        self.lb_camera.setAlignment(Qt.AlignCenter)
        self.lb_camera.setPixmap(_qPixmap)

        self.ledt_phone.setDisabled(True);
        self.lb_num_phone.setText("      ");

        self.user_name = {"Unknown" : 0, "배준수" : 0, "박인제" : 0, "박명우" : 0}
        try:
            _files = self.firepy.load_list_firestore()
            # for file in _files:
            #     print(file.name)
            #     _filename = str(file.name).split("/")[1].lower()
            #     try:
            #         print(_filename)
            #         self.firepy.load_storge(file.name, "./known/" + _filename)
            #         self.user_name[_filename[:3]] = 0
            #     except:
            #         print('Download Failed')
        except Exception as e:
            print(str(e))

    @pyqtSlot()
    def camera_view(self):
        self.img = cv2.cvtColor(mycamera.frame_buf, cv2.COLOR_BGR2RGB)
        _format = QImage(self.img,
                         self.img.shape[1],
                         self.img.shape[0],
                         QImage.Format_RGB888)
        _pixmap = QPixmap(_format)
        self.lb_camera.setPixmap(_pixmap)
        self.lb_camera.update()

    @pyqtSlot()
    def camera_off(self):
        print(str(self.lb_camera.width())+"  "+str(self.lb_camera.height()))
        self._myload = myload.Load(self)
        self._myload.load.connect(self.loading_end)
        self._myload.start()
        #무기록, Unknown, 이름 파싱 필요, 그후 이름과 자동차 번호가 매칭 확인
        _val = self.parsering(self._mycamera.face_dectection.face_names)
        self._mycamera.face_dectection.face_names = []
        _number = _val[3:]
        print("result name : ",_val)
        #그후 송신 하자
        if(_val == "" or _val == "Unknown" or _val != self.ledt_name.text()):
            msgbox = QMessageBox()
            msgbox.about(self, '인식 불가', '해당하는 사람이 없습니다.')
        else:
            print("이름", _val, "자동차 번호 ", self.ledt_car.text());
            _data = mysock.sendNrecv('gui : out ='+ self.ledt_car.text())
            msgbox = QMessageBox()
            print("data  ",int(_data))
            if (int(_data) < 0 or int(_data) > 100):
                msgbox.about(self, '주차 위치', '해당하는 자동차가 없습니다.')
            else:
                msgbox.about(self, '주차 위치', _data + '번호 자동차가 곧 나옵니다.')

        self.camera_slot_start.disconnect()
        self._mycamera.tic.disconnect()
        self._mycamera.off.disconnect()
        self.ledt_name.setText("")
        self.ledt_phone.setText("")
        self.ledt_car.setText("")

    def parsering(self, data_list):
        # print(data_list)
        if(len(data_list) == 0):
            _data = ""
            return _data
        else:
            _data = "Unknown"
            # _data_dic = {"Unknown" : 0}
            _data_dic = self.user_name
            for val in data_list:
                _data_dic[val] = _data_dic[val] + 1
            _sdata_dic = sorted(_data_dic.items(), reverse=True, key = lambda item: item[1])
            print(_sdata_dic)
            _data, _not = _sdata_dic[0]
            if(_not < 1):
                return "Unknown"
            return _data

    @pyqtSlot()
    def loading_end(self):
        _qPixmap = QPixmap("known/load.png")
        self.lb_camera.resize(_qPixmap.width(), _qPixmap.height())
        self.lb_camera.setPixmap(_qPixmap)
        self.runnig_camera = False

    def onQ(self):
        _data = mysock.sendNrecv('gui : tick')
        self.park_dic = ast.literal_eval(_data)
        self.setParkDic()

    def setParkDic(self):
        self.setParkColor(self.lb_1_1,self.park_dic[11])
        self.setParkColor(self.lb_1_2,self.park_dic[12])
        self.setParkColor(self.lb_1_3,self.park_dic[13])
        self.setParkColor(self.lb_2_1,self.park_dic[21])
        self.setParkColor(self.lb_2_2,self.park_dic[22])
        self.setParkColor(self.lb_2_3,self.park_dic[23])

    def setParkColor(self, lb, val):
        if(val == 1):
            lb.setStyleSheet("background-color: rgb(222, 222, 222);")
        elif(val == 2):
            lb.setStyleSheet("background-color: yellow;")
        elif(val == 3):
            lb.setStyleSheet("background-color: blue;")
        elif(val == 4):
            lb.setStyleSheet("background-color: red;")
        elif(val == 5):
            lb.setStyleSheet("background-color: green;")

    def changeLayout1(self):
        self.stkwdg.setCurrentIndex(0)

    def changeLayout2(self):
        self.stkwdg.setCurrentIndex(1)

    def changeLayout3(self):
        self.stkwdg.setCurrentIndex(2)

    def searchcle(self):
        str = self.ledt_search.text()
        if(not str.isdecimal()):
            msgbox = QMessageBox()
            msgbox.about(self, '에러', '번호를 입력해주세요')
            return
        else:
            _data = mysock.sendNrecv('gui : find = ' + str)
            msgbox = QMessageBox()
            if (int(_data) < 0 or int(_data) > 100):
                msgbox.about(self, '주차 위치', '해당하는 자동차가 없습니다')
            else:
                msgbox.about(self, '주차 위치', _data + '번 위치 해 있습니다')

    def findcle(self):
        '''
        str = self.ledt_out.text()
        if(not str.isdecimal()):
            msgbox = QMessageBox()
            msgbox.about(self, '에러', '번호를 입력해주세요')
            return
        else:
            _data = mysock.sendNrecv('gui : out =' + str)
            msgbox = QMessageBox()
            if (int(_data) < 0):
                msgbox.about(self, '주차 위치', '해당하는 자동차가 없습니다.')
            else:
                msgbox.about(self, '주차 위치', _data + '번호 자동차가 곧 나옵니다.')
        '''
        car = self.ledt_car.text()
        phone = self.ledt_phone.text()
        name = self.ledt_name.text()
        if(len(car) == 2):
            _data = mysock.sendNrecv('gui : out =(master)' + car)
            msgbox = QMessageBox()
            if (int(_data) < 0  or int(_data) > 100):
                msgbox.about(self, '주차 위치', '해당하는 자동차가 없습니다.')
            else:
                msgbox.about(self, '주차 위치', _data + '번호 자동차가 곧 나옵니다.')
        else:
            if (not self.runnig_camera):
                if(len(name) < 1 or len(car) < 1):
                    msgbox = QMessageBox()
                    msgbox.about(self, '에러 확인', '이름, phone, 자동차번호를 다시 입력해주세요')
                    return
                else:
                    try:
                        _data = self.firepy.load_firestore(name,car)
                        print("_data name phone : ", _data)
                        _img = _data['img']+'.JPG'
                        _file_list = os.listdir('./known')
                        if(self.file_serch(_img, _file_list)):
                            _path = self.firepy.load_storge(_img)
                            self._mycamera.face_dectection.add_face(_img)
                        self._mycamera.tic.connect(self.camera_view)
                        self._mycamera.off.connect(self.camera_off)
                        self.camera_slot_start.connect(self._mycamera.name_slot)
                        self._mycamera.start()
                        self.runnig_camera = True
                        self.camera_slot_start.emit(self.ledt_name.text())
                    except KeyError as key:
                        print("error : "+str(key))
                        msgbox = QMessageBox()
                        msgbox.about(self, '에러 확인', str(key))
                    except Exception as e:
                        print("error : ",str(e))
                        msgbox = QMessageBox()
                        msgbox.about(self, '에러 확인', str(e))
            else:
                msgbox = QMessageBox()
                msgbox.about(self, '에러 확인', '현재 카메라가 구동중입니다.')
                return

    def file_serch(self, name, _file_list):
        _data = False
        for file in _file_list:
            if(str(file) == str(name)):
                _data = True
        return _data

    def __del__(self):
        mysock.sockClosing()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = QWidget()
    test = testW()
    test.show()
    sys.exit(app.exec_())
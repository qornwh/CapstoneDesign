import face_recognition
import cv2
import dlib
import os
import numpy as np
import time
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PIL import ImageFont, ImageDraw, Image

global frame_buf
global name_buf

class camera(QThread):
    tic = pyqtSignal()
    off = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.frame = None
        self.rat = None
        self.key = 27
        self.face_dectection = face_detect()
        self.isOpend = True

    def run(self):
        global frame_buf
        if(self.cap.isOpened()):
            self.width = self.cap.get(3)
            self.height = self.cap.get(4)

        else:
            print("VideoCamera is not opened")
            return

        start = time.time()
        while(True):
            if(time.time() - start > 5):
                #시그널을 하나 더 만든다, 그후 실행된 emit함수에서 2초간 대기후 이미지 변경
                #찾은 이름들을 튜플로 만들어서 emit함수에서 처리 및 전송
                self.off.emit()
                break
                
            if(self.isOpend):
                self.rat, self.frame = self.cap.read()
                frame_buf = self.face_dectection.encoding(self.frame) #여기 에러
                self.tic.emit()
            else:
                break

    @pyqtSlot(str)
    def name_slot(self, name):
        self.face_dectection.this_name = name
        print("my_camera_slot : ",name)

    def __del__(self):
        self.isOpend = False
        del self.face_dectection

class face_detect:
    def __init__(self):
        '''
        __test_image = face_recognition.load_image_file("known/bill.jpg")
        __test1_face_encoding = face_recognition.face_encodings(__test1_image)[0]

        __test2_image = face_recognition.load_image_file("known/Obama.jpg")
        __test2_face_encoding = face_recognition.face_encodings(__test2_image)[0]

        self.known_face_encodings = [
            self.__test1_face_encoding,
            self.__test2_face_encoding
        ]
        self.known_face_names = [
            "bill",
            "obama"
        ]
        '''
        self.known_face_encodings = []
        self.known_face_names = []
        _file_list = os.listdir('known')

        for file in _file_list:
            if(file.endswith('.jpg')):
                __test1_image = face_recognition.load_image_file("./known/"+file)
                __test1_face_encoding = face_recognition.face_encodings(__test1_image)[0]
                self.known_face_encodings.append(__test1_face_encoding)
                self.known_face_names.append(file[0:3])

        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True
        self.this_name = ""

    def add_face(self, file):
        __test1_image = face_recognition.load_image_file("known/" + file)
        __test1_face_encoding = face_recognition.face_encodings(__test1_image)[0]
        self.known_face_encodings.append(__test1_face_encoding)
        self.known_face_names.append(file[0:3])

    def encoding(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small_frame = small_frame[:, :, ::-1]
        _match = False

        if self.process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances) #여기서 에러

                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                    _match = True
                    print("match : ", name)

                self.face_names.append(name)

        for (top, right, bottom, left), name in zip(face_locations, self.face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (40, 40, 40), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            # Draw a label with a name below the face
            if(_match):
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, "Matched", (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            else:
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame,"Unknown", (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        return frame

    def __del__(self):
        self.process_this_frame = False


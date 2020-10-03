# CapstoneDesign

## 주제 : 얼굴인식을 통한 자동 주차 시스템
- 주차하면서 발생되는 문제 5가지(주차 정체, 빈 주차공간, 주차사고, 사람들의 성향, 주차하는 시간)는 사람이 주차를 하면서 생기는 문제이므로 자동으로 주차를 해주는 시스템과 편의성을
위해 안드로이드 앱으로 얼굴인식하여 자동차를 꺼내오는 기능을 프로젝트 입니다.

### 파일구성
- 노트북
```
server : 자동주차 타워 서버, 번호판 인식 기능
gui_touch_panel : 주차장 주차여부, 자동차 위치, 자동차 꺼내기 기능
```
- 라즈베리파이
```
car : 차랑 운반 rc카
park : 주차타워 
```
- 안드로이드 스마트폰
```
face_recognation_android : 얼굴인식, 사용자 등록, 수정 및 자동차 꺼내기 
```

### 환경
- 네트워크 : 노트북 윈도우 10 pro 핫스팟 이용
- os : 노트북 - 윈도우10, 라즈베리파이 - 라즈비안
- pyqt5 : 5.15
- python : 3.7
- android studio : 4.0

### 사진
- 자동차 번호판 인식
![dryt](https://user-images.githubusercontent.com/46042936/94984682-854ce680-0589-11eb-8196-943ee3afab72.PNG)
- gui_touch_panel : face-recognition-python 얼굴인식 
![gui1](https://user-images.githubusercontent.com/46042936/94984683-88e06d80-0589-11eb-8b0a-1ec145ba3e22.jpg)
- face_recognation_android : 얼굴인식
![안드로이드2](https://user-images.githubusercontent.com/46042936/94984685-8b42c780-0589-11eb-8dbe-40baa6d47f01.jpg)
- rc카1
![자동차 앞](https://user-images.githubusercontent.com/46042936/94984687-8d0c8b00-0589-11eb-94f1-fa68f1b433c5.png)
- rc카2
![자동차옆](https://user-images.githubusercontent.com/46042936/94984688-8ed64e80-0589-11eb-8ec8-4f4bf3516923.png)

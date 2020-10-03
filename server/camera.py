import cv2 
#0이면 노트북 내장 웹캠 숫자를 올리면 추가된 웹캠을 이용할 수 있다.
def capture():
	filepath = './take.jpg'
	cap = cv2.VideoCapture(1)
	# 3은 가로 4는 세로 길이
	cap.set(3, 720)
	cap.set(4, 1080)
	ret, frame = cap.read()
	ret, frame = cap.read()
	ret, frame = cap.read()
	ret, frame = cap.read()
	ret, frame = cap.read()
	ret, frame = cap.read()
	dst = cv2.flip(frame, 1)
	dst2 = cv2.resize(dst, dsize=(0, 0), fx=1.3, fy=1, interpolation=cv2.INTER_LINEAR)
	cv2.imwrite(filepath, dst2)



	cap.release()
	cv2.destroyAllWindows()

data = capture()
# cap = cv2.VideoCapture(1)
# # 3은 가로 4는 세로 길이
# cap.set(3, 720)
# cap.set(4, 1080)
# while True:
# 	ret, frame = cap.read()
# 	cv2.imshow('test', frame)
# 	k = cv2.waitKey(33)
#
# 	if k == 27:
# 		break
# cap.release()
# cv2.destroyAllWindows()
#
# filepath = './take.jpg'
# cap = cv2.VideoCapture(1)
# ret, frame = cap.read()
# cv2.imwrite(filepath, frame)
# cap.release()
# print("gsdg", filepath)

# cap = cv2.VideoCapture(1)
# # 3은 가로 4는 세로 길이
# cap.set(3, 720)
# cap.set(4, 1080)
# ret, frame = cap.read()
# cv2.imshow('test', frame)
# cv2.imwrite('./take.jpg', frame)

from openalpr import Alpr
import cv2
print("openalpr")

class License():
    def __init__(self):
        super()
        self.country = 'kr'
        self.config = 'openalpr.conf'
        self.runtime_data = 'runtime_data'
        self.alpr = Alpr(self.country, self.config, self.runtime_data)

        if not self.alpr.is_loaded():
            print("Error loading OpenALPR")

        print("Using OpenALPR " + self.alpr.get_version())
        self.number = '-1'

    def imgProcessing(self, file):
        _file = self.capture()
        if(_file == None):
            _file = file
        results = self.alpr.recognize_file(_file)
        print("Image size: %dx%d" %(results['img_width'], results['img_height']))
        print("Processing Time: %f" % results['processing_time_ms'])

        i = 0
        for plate in results['results']:
            i += 1
            print("Plate #%d" % i)
            print("   %12s %12s" % ("Plate", "Confidence"))
            self.number = plate['candidates'][0]['plate']
            for candidate in plate['candidates']:
                prefix = "-"
                if candidate['matches_template']:
                    prefix = "*"

                print("  %s %12s%12f"%(prefix, candidate['plate'], candidate['confidence'])+"%")
        #번호판 문자열을 찾지 못햇을경우 12자1234
        if (self.number == '-1' or len(results) == 0):
            self.number = '00허7777'
            return self.number
        return self.number

    def capture(self):
        filepath = './take.jpg'
        _cap = cv2.VideoCapture(1)
        if not _cap.isOpened():
            return None
        ret, frame = _cap.read()
        ret, frame = _cap.read()
        ret, frame = _cap.read()
        ret, frame = _cap.read()
        ret, frame = _cap.read()
        ret, frame = _cap.read()
        dst = cv2.flip(frame, 1)
        dst2 = cv2.resize(dst, dsize=(0, 0), fx=1.3, fy=1, interpolation=cv2.INTER_LINEAR)
        cv2.imwrite(filepath, dst2)
        _cap.release()
        return filepath

    def __del__(self):
        print("license class del")

#test

if __name__ == '__main__':
    license = License()
    data = license.imgProcessing('C:/Users/BeaJunsu/Desktop/test14.jpg')
    print()
    print("번호판 : ", data)

# if (self.number == '-1' or len(results) == 0):
#     self.number = '12자1234'
#     return self.number
#

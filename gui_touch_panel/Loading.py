import time
from PyQt5.QtCore import QThread, pyqtSignal

class Load(QThread):
    load = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        self.isLoad = True

    def run(self):
        start = time.time()
        if(not self.isLoad):
            return
        while (True):
            if (time.time() - start > 1.5):
                print("loading end")
                self.load.emit()
                time.sleep(0.5)
                break

    def __del__(self):
        self.isLoad = False
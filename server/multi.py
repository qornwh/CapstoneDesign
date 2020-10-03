import time
from multiprocessing import Process, Queue, Event

class multi():
    def __init__(self):
        self.q = Queue()
        self.e = Event()
        self.val = 0
        self.e.set()
        self.q.maxsize = 20

    def produce(self, data):
        if(self.e.is_set()):
            self.e.clear()
            if(self.q.full()):
                print('큐 가득참 대기하삼')
                self.e.set()
            else:
                self.q.put(data)
                print('produce', data)
                self.e.set()

    def consum(self):
        _data = -1
        if (self.e.is_set()):
            self.e.clear()
            if(self.q.empty()):
                print('큐 비었음 대기하삼')
                self.e.set()
            else:
                self.val = self.q.get()
                print('consum',self.val)
                self.e.set()
                _data = 1
        return _data

    def setToEvent(self):
        self.e.set()

    def getVal(self):
        return self.val

    def removeVal(self):
        self.val = 0


if __name__ == '__main__':
    print('시작')
    m = multi()
    p1 = Process(target=m.produce, args={'12'})
    p2 = Process(target=m.consum, args={})
    p3 = Process(target=m.produce, args={'12'})
    p4 = Process(target=m.consum, args={})
    p5 = Process(target=m.produce, args={'12'})
    p6 = Process(target=m.consum, args={})

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()

    time.sleep(10)
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()

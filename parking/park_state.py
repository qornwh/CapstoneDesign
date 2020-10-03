from enum import Enum

class pEnum(Enum):
    no = -1
    open = 1
    on = 2
    up = 3
    down =4
    run = 5
    out = 6

class pState():
    def __init__(self):
        self.__name = "park"
        self.__state = pEnum.no
        self.__speed = 90
        self.__floor = 1
        
    def setName(self, name):
        self.__name = name
        print('name setting')
        
    def setSpeed(self, speed):
        self.__speed = speed
        
    def setState(self, state):
        self.__state = state
        print('state change :' , self.__state)
    
    def setFloor(self, floor):
        self.__floor = floor
        print('floor change :' , self.__floor)
    
    def name(self):
        return self.__name
    
    def speed(self):
        return self.__speed

    def state(self):
        return self.__state
    
    def floor(self):
        return self.__floor
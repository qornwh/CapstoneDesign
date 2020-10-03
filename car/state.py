from enum import Enum

class pEnum(Enum):
    no = 0
    open = 1
    on = 2
    run = 3
    restart = 4
    reset = 9
    end = 10

class pState():
    _name = "car01"
    _state = 0
    _speed = 75
    _park_number = 0
    _car_number = ''
    _car_type = 0

    @staticmethod
    def setName(name):
        pState._name = name
        print('Name Setting')

    @staticmethod
    def setSpeed(speed):
        pState._speed = speed

    @staticmethod
    def setState(state):
        pState._state = state
        print('State Setting :' , pState._state)

    @staticmethod
    def setParkNumber(value):
        pState._park_number = value
        print('ParkName Setting :' , pState._park_number)

    @staticmethod
    def setCarNumber(value):
        pState._car_number = value
        print('CarName Setting :' , pState._car_number)

    @staticmethod
    def setCarType(value):
        pState._car_type = value
        print('CarType Setting :' , pState._car_type)

    @staticmethod
    def name():
        return pState._name

    @staticmethod
    def speed():
        return pState._speed

    @staticmethod
    def state():
        return pState._state

    @staticmethod
    def park_number():
        return pState._park_number

    @staticmethod
    def car_number():
        return pState._car_number

    @staticmethod
    def car_type():
        return pState._car_type

    @staticmethod
    def stateChange(value=1):
        pState._state = pState._state + value
        print('State Change :' , pState._state)

    @staticmethod
    def re_setting():
        pState._park_number = 0
        pState._car_number = ''
        pState._handle_data = 0
        pState._car_type = 0

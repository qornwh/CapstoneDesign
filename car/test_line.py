import test_gpio

pin_otl = 15
pin_otc = 13
pin_otr = 11

def setting():
    test_gpio.GPIO.setup(pin_otl, test_gpio.GPIO.IN)
    test_gpio.GPIO.setup(pin_otc, test_gpio.GPIO.IN)
    test_gpio.GPIO.setup(pin_otr, test_gpio.GPIO.IN)

def line_data():
    left = test_gpio.GPIO.input(pin_otl)
    cent = test_gpio.GPIO.input(pin_otc)
    righ = test_gpio.GPIO.input(pin_otr)
    return left,cent,righ
    
'''
import time
if __name__ == '__main__':
    while(True):
        l,c,r = line_data()
        print(l,' : ',c, ' : ', r ,':')
        time.sleep(0.5)
'''

import test_gpio

pin_jodo = 31

def setting():
    test_gpio.GPIO.setup(pin_jodo, test_gpio.GPIO.IN)

def jodo_data_a0():
    count = 0

    while(test_gpio.GPIO.input(pin_jodo) == test_gpio.GPIO.LOW):
                count += 1

    return count

def jodo_data_d0():
    jodo = test_gpio.GPIO.input(pin_jodo)
    return jodo
    
def jodo_interrpt():
    print('interrpt jodo')

import test_gpio
import test_jodo

test_gpio.setting_gpio()
test_jodo.setting()

test_gpio.GPIO.add_event_detect(test_jodo.pin_jodo, test_gpio.GPIO.FALLING, callback = test_jodo.jodo_interrpt)

try:
    while(True):
        jodo = test_jodo.jodo_data_d0()
        print(jodo)
        test_gpio.time.sleep(1)


except KeyboardInterrupt:                            
    print("close")
    
test_gpio.cleaning()

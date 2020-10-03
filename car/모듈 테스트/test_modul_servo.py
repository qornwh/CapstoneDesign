import test_gpio
import test_servo

test_gpio.setting_gpio()
test_servo.setting()

test_servo.setMoterControl(12.5) #아래로 
test_gpio.time.sleep(2)
test_servo.setMoterControl(1) #위로 
                           
#test_servo.setMoterControl(6)
                           
test_gpio.time.sleep(2)
print('ok')
test_gpio.cleaning()

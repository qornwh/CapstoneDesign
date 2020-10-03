import test_gpio as gpio
import test_moter_liner as moter_liner

def setting():
    gpio.setting_gpio()
    moter_liner.setting()

def ending():
    gpio.cleaning()

setting()

state = 2

#moter_liner.setMoterControl(99, 1)
moter_liner.setMoterControl(99, state)
moter_liner.setMoterControl(99, state)
moter_liner.setMoterControl(99, state)
moter_liner.setMoterControl(99, state)
moter_liner.setMoterControl(99, state)
moter_liner.setMoterControl(99, state)

print('end')
ending()



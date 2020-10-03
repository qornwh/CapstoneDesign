import test_gpio  as gp
import test_act   as act
import test_limit as limit
import test_approach2 as app

gp.setting_gpio()
#limit.setting_limit()
app.setting_approach()
#limit.setting_interrupt()
app.setting_interrupt()

while(True):
    try:
        print()
        
    except KeyboardInterrupt:
        print('keyboardInterrupt')
    
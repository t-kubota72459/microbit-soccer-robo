from microbit import *

def soccor_action():
    """
    LED 点灯パフォーマンス
    """
    for i in range(3):
        display.show(Image.HAPPY)
        sleep(50)
        display.clear()
        sleep(50)
    display.show(Image.HAPPY)
    sleep(50)
    display.clear()

def rescue_action():
    """
    赤外線 LED 放射
    """
    for _ in range(20):
        pin1.write_digital(1)
        pin1.write_digital(0)
        sleep_us(500)
    for _ in range(20):
        pin1.write_digital(1)
        pin1.write_digital(0)
        sleep_us(500)
    for _ in range(20):
        pin1.write_digital(1)
        pin1.write_digital(0)

def no_action():
    pass

def setup(job):
    if job == "SOCCOR":
        return soccor_action
    elif job == "RESCUE":
        return rescue_action
    else:
        return no_action

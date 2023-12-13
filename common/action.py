from microbit import *
import time

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
    for _ in range(350):
        pin1.write_digital(1)
        time.sleep_us(8)
        pin1.write_digital(0)
        time.sleep_us(16)


def no_action():
    pass

def setup(job):
    if job == "SOCCOR":
        return soccor_action
    elif job == "RESCUE":
        return rescue_action
    else:
        return no_action

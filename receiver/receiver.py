##
## receiver.py
##
## ロボットを操作してゴールを決めろ！
##
## micro:bit 受信側プログラム
## 送られてきたメッセージを解釈し，決められた処理をする
##
## Copyright (c) 2022 Hiroshima Politechnical College.
##

from microbit import *
from motor_command import *
from k_motor import *
import radio

#
# 初期設定
#
CHANNEL = 2
VERSION = "1.0"
DEBUG = False
POWER = 80          # 出力値 (最大でここまで)

def wait_msg():
    """
    受信メッセージを待ちうける
    """
    s = None
    while s is None:
        s = radio.receive()
    return s


def flush():
    """
    受信メッセージを読み捨てる
    """
    s = radio.receive()
    while s is not None:
       s = radio.receive()


def performance():
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
    flush()     # 溜まっていたメッセージを読み捨てる


#------------------------------------------------------------
# メイン処理
#------------------------------------------------------------
uart.init(9600)
uart.write("**** RECEIVER {}****\r\n".format(VERSION))
uart.write("CHANNEL:{}\r\n".format(CHANNEL))
r = KMotor()    # モーターオブジェクト

radio.on()
radio.config(channel=CHANNEL, queue=4)

# x 値，y 値の初期値
x = 0
y = 0
while True:
    msg = wait_msg().split(",")
    command = msg[0]

    #
    # 命令に従って処理をする
    #
    if command == "B":      # ボタン・コマンド
        if msg[1] == "A":
            rotate_left(r)
        elif msg[1] == "B":
            rotate_right(r)
        elif msg[1] == "C":
            performance()
    elif command == "A":    # 加速度センサー・コマンド
        (x, y, z) = (int(msg[1]), int(msg[2]), int(msg[3]))

        if -200 < x < 200 and -250 < y < 250:       ## 静置
            stop(r)
        elif 500 < x:                               ## 右に傾けた
            turn_right(r, KMotor.FORWARD, POWER-10)
        elif x < -500:                              ## 左に傾けた
            turn_left(r, KMotor.FORWARD, POWER-10)
        elif y < -300:                              ## (頭を) 下に傾けた
            speed = min(int((-y / 1024) * POWER), 100)
            forward(r, speed)
        elif y > 300:                               ## (頭を) 上に傾けた
            speed = min(int((y / 1024) * POWER), 100)
            reverse(r, speed)
    sleep(50)

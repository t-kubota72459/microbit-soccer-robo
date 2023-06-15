##
## sender.py
##
## ロボットを操作してゴールを決めろ！
##
## micro:bit 送信側プログラム
## ボタンの状態と加速度センサーの値を送信する
##
## Copyright (c) 2022 Hiroshima Politechnical Callege.
##

import radio
from microbit import *

##
## 初期設定
##
VERSION = "1.0"
DEBUG = False
CHANNEL = 1

def button_stats():
    """
    A, B ボタンの状態を文字列で返す関数
    """
    if button_a.is_pressed() and button_b.is_pressed():  # A と B を押している
        return "B,C"
    elif button_a.is_pressed():  # A のみ押している
        return "B,A"
    elif button_b.is_pressed():  # B のみ押している
        return "B,B"
    return "B,N"  # なにも押していない

##
## メイン
##
uart.init(9600)
uart.write("**** SENDER {}****\r\n".format(VERSION))
uart.write("CHANNEL:{}\r\n".format(CHANNEL))

radio.config(channel=CHANNEL)
radio.on()

while True:
    bt = button_stats()                     # ボタンの状態を取得
    accl = accelerometer.get_values()       # X, Y, Z 軸方向の G を取得
    accl_msg = "A,{},{},{}".format(accl[0], accl[1], accl[2])

    radio.send(bt)
    radio.send(accl_msg)
    if DEBUG:
        uart.write("sending\r\n")
        uart.write("{},{},{},{}\r\n".format(bt, accl[0], accl[1], accl[2]))
    sleep(200)

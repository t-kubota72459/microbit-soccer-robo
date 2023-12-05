##
## sender.py
##
## ロボットを操作してゴールを決めろ！
##
## micro:bit 送信側プログラム
## ボタンの状態と加速度センサーの値を送信する
##
## Copyright (c) 2022,2023 Hiroshima Politechnical Callege.
##
import radio
from microbit import *
VERSION = "1.1"
DEBUG = False

##
## 初期設定
##
CHANNEL = 1
TX_INTERVAL = 300   ## 命令の送信間隔

def get_signed_int(b):
    """
    byte を integer にする (2000 を超えたときはマイナス値として扱う)
    """
    v = int.from_bytes(b, 'little')
    if v > 2000:    ## sensor's value should not exceed 2000 mg
        return v - 65536
    return v

def button_stats():
    """
    A, B ボタンの状態を返す
    """
    if button_a.is_pressed() and button_b.is_pressed():  # A と B を押している
        return b"\xbc"
    elif button_a.is_pressed():  # A のみ押している
        return b"\xba"
    elif button_b.is_pressed():  # B のみ押している
        return b"\xbb"
    return b"\xb0"               # なにも押していない

## ------------------------------------------------------------
## メイン
## ------------------------------------------------------------
uart.init(9600)
uart.write("**** SENDER {}****\r\n".format(VERSION))
uart.write("CHANNEL:{}\r\n".format(CHANNEL))

radio.config(channel=CHANNEL)
radio.on()

display.scroll("ch:{}".format(str(CHANNEL)))

while True:
    # ボタンの状態を取得する
    b = button_stats()

    # X, Y, Z 軸方向の G を取得する
    for v in accelerometer.get_values():
        b += v.to_bytes(2, 'little')

    # 送信する
    radio.send_bytes(b)

    if DEBUG: uart.write("command:{},{},{},{}\r\n".format(b[0], get_signed_int(b[1:3]), get_signed_int(b[3:5]), get_signed_int(b[5:7])))

    # つぎの送信まで休む
    sleep(TX_INTERVAL)

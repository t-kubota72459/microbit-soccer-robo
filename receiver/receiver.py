##
## receiver.py
##
## ロボットを操作してゴールを決めろ！
##
## micro:bit 受信側プログラム
## 送られてきたメッセージを解釈し，決められた処理をする
##
## Copyright (c) 2022,2023 Hiroshima Politechnical College.
##
from microbit import *
from motor_command import *
from k_motor import *
import action
import radio
DEBUG = False
VERSION = "1.1"

#
# 初期設定
#
CHANNEL = 1
POWER   = 80        # 出力値 (最大でここまで)

#  
# どちらかの能力を身に着ける
#
JOB     = "SOCCOR"  # SOCCOR: サッカー選手 / RESCUE: レスキュー隊員
action = action.setup(JOB)

def get_signed_int(b):
    """
    加速度センサーの値を整数値にする
    """
    v = int.from_bytes(b, 'little')
    if v > 2000:    ## sensor's value could not exceed 2000 mg
        return v - 65536
    return v


def wait_msg():
    """
    受信メッセージを待ちうける
    """
    s = None
    while s is None:
        s = radio.receive_bytes()
    return s


def flush():
    """
    受信メッセージを読み捨てる
    """
    s = radio.receive_bytes()
    while s is not None:
       s = radio.receive_bytes()


#------------------------------------------------------------
# メイン処理
#------------------------------------------------------------
uart.init(9600)
uart.write("**** RECEIVER {}****\r\n".format(VERSION))
uart.write("CHANNEL:{}\r\n".format(CHANNEL))
display.scroll("ch:{}".format(str(CHANNEL)))

r = KMotor()    # モーターオブジェクト

radio.config(channel=CHANNEL, queue=2)
radio.on()

(x, y) = (0, 0)     # x 値，y 値の初期値

while True:
    #
    # メッセージ受信
    #
    msg = wait_msg()
    if len(msg) != 7:   ## 7bytes のみ受け入れる
        continue

    bt = msg[0]
    if bt == 0xba:      # A ボタン
        rotate_left(r)
    elif bt == 0xbb:    # B ボタン
        rotate_right(r)
    elif bt == 0xbc:    # A＋B ボタン
        action()
        flush()
    
    # 加速度センサーの値
    (x, y, z) = ( get_signed_int(msg[1:3]), get_signed_int(msg[3:5]), get_signed_int(msg[5:7]) )
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
    
    if DEBUG: uart.write("msg:{}, {}, {}, {}\r\n".format("%x" % msg[0], x, y, z))
    sleep(50)

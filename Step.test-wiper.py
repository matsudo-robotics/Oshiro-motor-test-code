from machine import Pin
import utime

# --- ピンの設定 (GP番号) ---
PUL = Pin(16, Pin.OUT)
DIR = Pin(17, Pin.OUT)
ENA = Pin(18, Pin.OUT)

# 1回転のパルス数 (DIPスイッチ設定 1:OFF, 2:ON, 3:ON なら 400)
PULSES_PER_REV = 400

def move_angle(degree, speed_us=1000):
    # パルス数の計算
    pulses = int(abs(degree) * (PULSES_PER_REV / 360))
    
    # 方向設定 (1: 正回転, 0: 逆回転)
    DIR.value(1 if degree > 0 else 0)
    
    # 指定パルス分ループ
    for _ in range(pulses):
        PUL.value(1)
        utime.sleep_us(speed_us)
        PUL.value(0)
        utime.sleep_us(speed_us)

# --- メイン動作 ---
try:
    # 最初にモーターを有効化
    ENA.value(1)
    print("ワイパー開始")

    # 5回往復させる
    for i in range(5):
        print(f"{i+1}往復目")
        
        move_angle(180, 500)   # 90度右へ (800usは少し速め)
        utime.sleep_ms(200)   # 0.2秒待機
        
        move_angle(-180, 500)  # 90度左へ
        utime.sleep_ms(200)   # 0.2秒待機

    print("完了しました")

finally:
    # 終わったらモーターの電気を切って発熱を防ぐ
    ENA.value(0)
    print("モーターOFF")
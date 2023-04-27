from machine import Pin, I2C
from sh1106 import SH1106_I2C
import network
import espnow

#Initializing
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000) 
oled = SH1106_I2C(128, 64, i2c, None, addr=0x3C)
oled.sleep(False)
oled.invert(False)

def PrintLCD(text,col,row):
    oled.text(text, col, row)
    oled.show()
    
def espnow_rx():

    # A WLAN interface must be active to send()/recv()
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.disconnect()                # Disconnect from last connected WiFi SSID

    e = espnow.ESPNow()                  # Enable ESP-NOW
    e.active(True)

    peer = b'\xaa\xaa\xaa\xaa\xaa\xaa'   # MAC address of peer's wifi interface
    e.add_peer(peer)                     # Sender's MAC registration
    var0 = 0
    var1 = 0
    var2 = 1
    row = 0
    while True:
        host, msg = e.recv()
        if msg:                          # wait for message
            if msg == b'detect':           # decode message and translate
                print(str(var0) + "-Motion Detected")       # to the NyBoard's command
                var0 += 1
                if var1 +25 < var0:
                    var1 = var0
                    txt = str(var2) + "-Motion Detect"
                    if row == 60:
                        oled.fill(0)
                        row = 0
                    PrintLCD(txt, 0, row)
                    var2 += 1
                    row += 10


if __name__ == "__main__":
    espnow_rx()

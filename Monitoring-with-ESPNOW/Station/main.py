import network
import espnow
import time
from machine import Pin

led = Pin(2,Pin.OUT)
PIR = Pin(14,Pin.IN) # Pin D5 on the controller which is SCLK 

sta = network.WLAN(network.STA_IF)    # Enable station mode for ESP
sta.active(True)
sta.disconnect()        # Disconnect from last connected WiFi SSID

e = espnow.ESPNow()     # Enable ESP-NOW
e.active(True)

peer1 = b'\xaa\xaa\xaa\xaa\xaa\xaa'   # MAC address of peer1's wifi interface
e.add_peer(peer1)                     # add peer1 (receiver1)

# led.value(0)
print("Starting...")            # Send to all peers
var =0
while True:
    if PIR.value() == 1: 
        e.send(peer1, "detect", True)     # send commands to pear 1
        print(str(var) + 'detect')
        led.value(0)
        var += 1
    else:
        led.value(1)
        e.send(peer1, "None", True)

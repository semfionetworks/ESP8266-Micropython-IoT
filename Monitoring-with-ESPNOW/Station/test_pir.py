from machine import Pin
PIR = Pin(14,Pin.IN)
led = Pin(2,Pin.OUT)

while True:
    if PIR.value() == 1:
        led.value(0)
    else:
        led.value(1)

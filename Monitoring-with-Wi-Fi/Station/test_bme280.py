#test
#import modules
from machine import Pin, I2C
from utime import sleep
import bme280

#initialize I2C
i2c= I2C(sda=Pin(4), scl=Pin(5), freq=400000)

while True:
    bme = bme280.BME280(i2c=i2c)
    temp = bme.values[0]
    pressure = bme.values[1]
    humidity = bme.values[2]
    SensorData = 'Temperature: ' + temp + '. Pressure: ' + pressure + '. Humidity: ' + humidity
    print(SensorData)
    print("-"*60)
    sleep(10)

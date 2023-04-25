import network
import socket
from machine import Pin, I2C
from time import sleep
import bme280

#initialization 
led = Pin(2, Pin.OUT)
i2c=I2C(sda=Pin(4), scl=Pin(5), freq=400000)

led = Pin(2,Pin.OUT)
led.value(0)
sleep(0.4)
led.value(1)

# Connect to Wi-Fi
def Connect():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.ifconfig(('192.168.0.205','255.255.255.0','192.168.0.1','192.168.0.1'))
    station.connect("SSID", "PASSWORD")
    while not station.isconnected():
        pass
    led.value(0)
    print(station.ifconfig())

#Ambience Sensing
def Ambience():
    bme = bme280.BME280(i2c=i2c)
    temp = bme.values[0]
    humidity = bme.values[2]
    reading = 'Temperature: ' + temp + ' Humidity: ' + humidity
    return reading

# Set up a socket for the web server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

Connect()
# Serve web pages
while True:
    conn, addr = s.accept()
    request = conn.recv(1024)
    if request:
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        html = "<html><body><h1> " + Ambience() + "</h1></body></html>"
        conn.send(response + html)
    conn.close()

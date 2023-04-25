#import modules
import network
import usocket as socket
from time import sleep
from machine import Pin, I2C
import bme280

#initialization 
led = Pin(2, Pin.OUT)
i2c=I2C(sda=Pin(4), scl=Pin(5), freq=400000)

led.value(0)
sleep(0.7)
led.value(1)

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("SSID", "PASSWORD")
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(2)
    wlan.ifconfig(('YOUR_STATIC_IP_ADDR', '255.255.255.0', '192.168.0.1', '192.168.0.1'))
    # If you don't want a static IP address just comment the above line
    sleep(1)
    ip = wlan.ifconfig()[0]
    print('The IP addr is: ', wlan.ifconfig()[0])
    led.value(0)
    return ip

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.bind(('',80))
    connection.listen(5)
    return connection

def webpage(reading):
    #Template HTML
    html = """<!DOCTYPE HTML>
<html>
<head>
    <meta http-equiv="refresh" content="10">
</head>
<body>
    <p><h1>""" + reading + """</h1></p>
</body>
</html>"""
    return html
    
def serve(connection):
    #Start a web server
    
    while True:
        bme = bme280.BME280(i2c=i2c)
        temp = bme.values[0]
        pressure = bme.values[1]
        humidity = bme.values[2]
        reading = 'Temperature: ' + temp + ' Humidity: ' + humidity + ' Pressure: ' + pressure
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)       
        html = webpage(reading)
        client.send('HTTP/1.1 200 OK\n')
        client.send('Content-Type: text/html\n')
        client.send('Connection: close\n\n')
        client.sendall(html)
        client.close()

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()

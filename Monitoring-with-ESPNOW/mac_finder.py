import network

# Initialize WiFi in station mode
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Print the MAC address
print(':'.join('%02x' % b for b in wlan.config('mac')))

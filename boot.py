import network
import time

def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("Connecting to WiFi...")
        sta_if.active(True)
        sta_if.connect('id', 'password')

        timeout = 10  # seconds
        for _ in range(timeout * 10):
            if sta_if.isconnected():
                break
            time.sleep(0.1)

    if sta_if.isconnected():
        print("WiFi connected:", sta_if.ifconfig())
    else:
        print("Failed to connect to WiFi")
        raise OSError("WiFi Connection Failed")

connect_wifi()


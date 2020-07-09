from network import WLAN
import urequests as requests
import machine
import pycom
import time

TOKEN = "xxxxx" # Put your TOKEN here 
DELAY = 300  # Delay in seconds

wlan = WLAN(mode=WLAN.STA)
wlan.antenna(WLAN.INT_ANT)

# Assign your Wi-Fi credentials
wlan.connect("SSID", auth=(WLAN.WPA2, "password"), timeout=5000)

while not wlan.isconnected ():
    machine.idle()
print("Connected to Wifi\n")

# Gets the temperature from pycom device
def calTemp():
    try:
        adc = machine.ADC()
        pinIn = adc.channel(pin='P13')

        mVolts = pinIn.voltage()
        degC = (mVolts - 500.0) / 10.0 # Converts millivolts to degrees celsius

        return degC
    except:
        return 0

# Sends the request
def post_var(device, value):
    try:
        url = "https://industrial.api.ubidots.com/"
        url = url + "api/v1.6/devices/" + device # Url for ubidots api
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"} # Builds the header
        data = {"temperature": {"value": value}} # Builds the json
        if data is not None:
            print(data)
            req = requests.post(url=url, headers=headers, json=data)
            return req.json()
        else:
            pass
    except:
        pass

while True:
    post_var("pycom", calTemp())
    time.sleep(DELAY)

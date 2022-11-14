import RPi.GPIO as GPIO
import http.client 
import urllib 
import time 
import sys 
import Adafruit_DHT 

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
MOIST=18
PIR=25
PUMP=24
LED1=12
LED2=16
LED3 = 17
BUZZER = 13
DHT = 19
key = 'I6YAUEQLKT3JP3G2' 


GPIO.setup(MOIST,GPIO.IN)
GPIO.setup(PUMP, GPIO.OUT)
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(PIR,GPIO.IN)
GPIO.setup(LED1,GPIO.OUT)
GPIO.setup(LED3,GPIO.OUT)


def thermometer(): 
    while True:
        h,t = Adafruit_DHT.read_retry(11,DHT) 
        params1 = urllib.parse.urlencode({'field1': t, 'key':key }) 
        params2 = urllib.parse.urlencode({'field2': h, 'key':key }) 

        headers = {"Content-typZZe": "application/x-www-form- urlencoded","Accept": "text/plain"} 
        conn = http.client.HTTPConnection("api.thingspeak.com:80") 
        try: 
            conn.request("POST", "/update", params1, headers) 
            response = conn.getresponse() 
            print ("Temperature = ", t) 
            #print (response.status, response.reason) 
            data = response.read() 
            conn.close() 

            conn.request("POST", "/update", params2, headers) 
            response = conn.getresponse() 
            print ("Humidity",h) 
            #print (response.status, response.reason) 
            data = response.read() 
            conn.close() 
        except: 
            print ("connection failed") 
        break
    
    
while True:
    print(" ")
    print(" ")
    print("Running DHT Sensor")
    thermometer()
    time.sleep(0.1)
    print(" ")
    print(" ")
    print("Running PIR")
    if (GPIO.input(PIR) == 0):
        print("No Intrueder")
        GPIO.output(LED3, 0)
        GPIO.output(BUZZER,0)
        time.sleep(0.5)
    elif (GPIO.input(PIR)== 1):
        print("Intruder Detected")
        GPIO.output(LED3, 1)
        GPIO.output(BUZZER,1)
        time.sleep(0.5)
    
        
    print("  ")
    print("  ")
    print("Running Moisture Sesor")
    if (GPIO.input(MOIST) == 0): 
        print ("  Water Detected!")
        print("Pump Stop")
        GPIO.output(PUMP,1)
        GPIO.output(LED1,0)
        GPIO.output(LED2,1)
        time.sleep(1)
    else: 
        print ("No Water Detected!")
        GPIO.output(PUMP,0)
        print("Pump Start")
        GPIO.output(LED1,1)
        GPIO.output(LED2,0)
        time.sleep(1)
        
        






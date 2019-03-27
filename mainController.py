#MAIN CLASS FOR ICARUS v1.0 (NO SAT COMS)
#Author:: Francisco Molina

import network
from umqtt.robust import MQTTClient
import machine
import time
#control de temperatura..
from temp import *


#Forced GLOBAL VARIABLES...
#mqtt
client= None
mqtt_client_id = bytes('client_'+'Icarus1', 'utf-8')
ADAFRUIT_IO_URL = b'io.adafruit.com' 
ADAFRUIT_USERNAME = b'molinajimenez'
ADAFRUIT_IO_KEY = b'd3727eec53bd4502a294bfbfaf379a6b'
try:
    client = MQTTClient(client_id=mqtt_client_id, 
                    server=ADAFRUIT_IO_URL, 
                    user=ADAFRUIT_USERNAME, 
                    password=ADAFRUIT_IO_KEY,
                    ssl=True)
    client.connect()
    print("conexion exitosa.")
except Exception as e:
    print("Ocurrio un error al comunicarse con servicio en nube, chequear params")

class mainController(object):
    
    def __init__(self,network,pw):
        self.gps=[]
        self.co2=0
        self.net=network
        self.pw=pw
        self.feedTemp=''
        self.feedHum=''
        self.feedGPS=''
        self.user=b'molinajimenez'
        

    '''
    Conexion con internet...
    TODO: Generalizar conexion.
    '''
    def connect(self):
        station = network.WLAN(network.STA_IF)
        if station.isconnected()==True:
            print("Conexion exitosa")
            return 1
        
        else:
            station.active(True)
            #conectamos...
            station.connect(self.net,self.pw)

        while station.isconnected()==False:
            pass
    
        print("Conexion exitosa")
        print(station.ifconfig())

    
    '''
    Crea comunicacion por MQTT. 
    IN: PARAMS para conexion
    OUT: 0-> Conexion exitosa ; -1-> Conexion fallida por cualquier factor..
    '''
        

    def dataCollection(self, tempPin,tempRefresh,tempFile):

        tempControll=tempController(tempPin,tempRefresh,tempFile)
        #asignamos feed
        self.feedTemp=bytes('{:s}/feeds/{:s}'.format(self.user, b'temp_data'), 'utf-8')
        self.feedHum=bytes('{:s}/feeds/{:s}'.format(self.user, b'humid_data'), 'utf-8')
        
        #self.feedHum="molinajimenez∕Feeds∕humid_data"
        x=True
        #vamos a recolectar toda la informacion posible..
        while x: 
            tempControll.recordTemp()
            #publicamos
            client.publish(self.feedTemp,bytes(str(tempControll.temp), 'utf-8'), qos=0)
            client.publish(self.feedHum,bytes(str(tempControll.humid), 'utf-8'), qos=0)
            if tempControll.retry >=45:
                break
                print("Error de sensor TEMP")
                #Kill cycle..
                print("Fatal error -- FAULTY TEMP SENSOR")
                return -1
            time.sleep(5)

control=mainController("UVG 2018","")
control.connect()
control.dataCollection(14,10,"logTemp.txt")



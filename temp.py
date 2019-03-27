# TEMP READER 
# Autor: Francisco Molina
# Usando librerias opensource obtenidas en Git
# SENSOR AM2306/DHT22
from machine import Pin
from dht import DHT22
import time, utime
#Cada 10 segundos vamos a actualizar temp y humedad.

class tempController(object):
    def __init__(self, pinRef, timeUpdate,filename):
        self.dht=DHT22(Pin(pinRef))
        self.UPDATE_TEMP=timeUpdate
        self.filename=filename
        self.temp=0
        self.humid=0
        self.retry=0
        print("paso de pin", pinRef)

    '''
    Chequea si existe en entorno el archivo con el nombre 'filename', que sera el log
    IN: nombre del archivo +.txt
    OUT: Int value, 1 si existe, 0 si no...
    '''

        
    def checkFile(self,filename):
        try:
            f=open(filename, 'r')
            print(filename+ ' already exists!')
            return 1
        except Exception:
            print("creating filename: " + filename)
            f=open(filename, 'w')
            #formatting for CSV
            f.write("TEMP,HUM")
            f.close()
            return 0


    '''
    Hace records de temperatura, construye json y se encarga de hacer LOGFILE (txt)
    IN: filename + .txt
    OUT: TEMP + HUMID dict, LOGFILE. -1 si falla el sensor.
    '''
    #normal recording method..
    #normal recording method..
    def recordTemp(self,value="tempLog.txt"):
        
        now = utime.ticks_ms()
        lineClose=0
        #creamos el txt
        self.checkFile(value)
        #intentos para que agarre onda el sensor..
        while self.retry < 45:
            try:
                self.dht.measure()
                break
            except:
                    
                self.retry = self.retry + 1
                print(".", end = "")

            print("")

        if (self.retry < 45 and utime.ticks_ms() - now >=self.UPDATE_TEMP):
            now = utime.ticks_ms()
            #damos formato a datos...
            self.temp="%3.1f " % self.dht.temperature()
            self.humid="%3.1f %% " % self.dht.humidity()
            
            #append: add line at EOF
            f=open(value, 'a')
            #CSV formatting
            f.write(self.temp + ',' + self.humid +'\n')
            lineClose = lineClose +1
            time.sleep(5)

            if lineClose>=2:
                f.close()
                lineClose=0

        
        
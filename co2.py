#MQ135 controller
#Autor: Francisco Molina
#RETURNS NOT CORRECTED PPM
from machine import Pin
from MQ135 import MQ135
import time, utime
print("MQ135")
class mqController(object):
    def __init__(self, pinRef,filename,co2Refresh):
        self.mq=MQ135(Pin(pinRef))
        self.filename=filename
        self.co2=0
        self.retry=0
        self.updateCO2=co2Refresh

    
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
            f.write("CO2")
            f.close()
            return 0

    def recordGas(self,temp,humid):
        now = utime.ticks_ms()
        lineClose=0
        #creamos el txt
        self.checkFile(self.filename)

        while self.retry < 45:
            try:
                self.mq.get_rzero()
                if (self.mq.get_resistance()== -1):
                    print("RESISTANCE FAILED, not getting val.")
                    break
                print("fase 1: co2")
                break
            except:
                self.retry = self.retry + 1
                print(".", end = "")

                
        if (self.retry < 45):
            now = utime.ticks_ms()
            self.mq.get_rzero()
            
            self.mq.get_resistance()
            #damos formato a datos...
            self.co2=self.mq.get_corrected_ppm(float(temp), float(humid))
            
            #append: add line at EOF
            #f=open(self.filename, 'a')
            #CSV formatting
            #f.write(str(self.co2))
            #lineClose = lineClose +1
            #if lineClose>=2:
             #   f.close()
              #  lineClose=0
    
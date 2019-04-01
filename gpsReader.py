# DATA GPS READER
# Autor: Francisco Molina
# Usando librerias opensource obtenidas en Git
# INPUT RAW GPS DATA
# OUTPUT: PARSED GPGGA provisional.
'''
Cada vez que sea llamada esta clase, se refrescara el GPS.
Devolvera sentence NMEA de tipo: 

TO-DO:
Hora bug fix, esta corrido el huso horario.
PARSEO CORRECTO CON NMEA, micropyGPS puede ser muy pesado.
'''
from machine import UART, Pin
from micropyGPS import MicropyGPS
import utime, time
import nmea
print("Neo 6M - OBJ")
class gpsController(object):
    #Guessing baud rate between GPS, ESP module-- Correct...
    def __init__(self, pinRefTx,pinRefRx, timeUpdate,filename,bauds=9600):
        print("pin TX", pinRefTx)
        print("pin RX", pinRefRx)
        print("baudios", bauds)
        self.uart=UART(1, baudrate=bauds,tx=pinRefTx,rx=pinRefRx)
        self.statement=None
        self.lat=''
        self.longitude=''
        self.UPDATE_GPS=timeUpdate

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
            f.write("Latitud,Longitud"+'\n')
            f.close()
            return 0

    def posUpdate(self,value='locationAccess.txt'):

        updateGPS = utime.ticks_ms()
        #indicamos offset de UTC.
        my_gps = MicropyGPS(6)
        
        cont=0
        my_nmea = nmea.nmea()        
        # Cada cierto tiempo, en este caso
        #if(utime.ticks_ms() - updateGPS >= self.UPDATE_GPS):
        updateGPS = utime.ticks_ms()
        time.sleep(1)
        self.statement = self.uart.read()
        my_nmea.parse(self.statement)
        self.lat=('{}'.format(my_nmea.latitude))
        self.longitude=('{}'.format(my_nmea.longitude))

        print(self.lat,self.longitude)
    
        #append: add line at EOF
        f=open(value, 'a')
        f.write('{} {}'.format(my_nmea.latitude, my_nmea.longitude))
        f.write('\n')
        f.close()
        cont+=1
        #matamos el ciclo
        if cont>=2:
            f.close()
            cont=0
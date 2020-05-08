# Librerias
import serial
import pymongo


class arduino_serial:
    # Variables
    serialPort = "/dev/cu.usbmodem14101"
    temp_sens = ""
    temp_min = ""
    temp_max = ""
    temp_pref = ""
    act0_status = ""
    act1_status = ""

    # Constructor
    def __init__(self, conexion):
        print("Arduino OK")
        self.con = conexion
        self.temp_sens=0
        self.temp_min=0
        self.temp_max=0
        self.temp_pref=0
    

    # Función encargada de leer mensajes enviados por el microcontrolador Arduino
    def readArduino_Serial(self):
        ser = serial.Serial(self.serialPort,115200)
        line = ser.readline().decode()
        ser.close()
        arduino_data = (line.replace('\r\n','').replace(';','')).split('?')
        
        self.ID_Device = arduino_data[0]
        if(arduino_data[0] == self.ID_Device) and (len(arduino_data) > 1):
            objeto = self.parseJSON(arduino_data[0], arduino_data[1])
            if(objeto['t0']!=self.temp_sens):
                if(objeto['t0']=="error"):
                    print("Error de dispositivo")
                else:
                    self.temp_sens = float(objeto['t0'])
        else:
            return "No device"
    
    # Función encargada de enviar mensajes al microcontrolador Arduino
    def writeArduino_Serial(self, str_Serial):
        ser = serial.Serial(self.serialPort,115200)
        ser.write((str_Serial+"\r\n").encode('ascii'))
        ser.close()
    
    # Función encargada de parsear una cadena recibida desde el microcontrolador Arduino a una lista con formato JSON
    def parseJSON(self, ID_Device, str_Data):
        dict_Data = {}
        dict_Data["ID_Device"] = ID_Device
        str_lecturaSensor = str_Data.split('@')[0]
        str_chain = str_lecturaSensor.split('|')
        ## Armar JSON
        for i in str_chain:
            if i.find(':') >= 0:
                arr_values = i.split(':')
                dict_Data[arr_values[0]]=arr_values[1]
        ## Devolver JSON
        return dict_Data

    # Función encargada de obtener datos relacionados con una enfermedad desde la base de datos
    def getInfo_DB(self):
        db = self.con.conexion()
        coleccion = db['sensor_temp']
        query = {"activo" : "t"}
        req = list(coleccion.find(query))[0]

        # Asignación de respuesta del query a variables globales de la clase
        if(len(req)>0):
            if(self.temp_min != req['temp_min']):
                self.temp_min=req['temp_min']
            
            if(self.temp_max != req['temp_max']):
                self.temp_max=req['temp_max']

            if(self.temp_pref != req['temp_pref']):
                self.temp_pref=req['temp_pref']
            
            if(self.act0_status != req['act0_status']):
                self.act0_status=req['act0_status']
            
            if(self.act1_status != req['act1_status']):
                self.act1_status=req['act1_status']
        else:
            self.act0_status = self.act1_status = "f"
            self.temp_sens = self.temp_min = self.temp_max = 0
    
    # Función encargada de actualizar los valores de los datos relacionados con una enfermedad en la base de datos
    def updateInfo_DB(self,act0,act1):
        db = self.con.conexion()
        coleccion = db['sensor_temp']
        query = {"activo" : "t"}
        data = {"$set":{"act0_status": act0, "act1_status" : act1}}
        coleccion.update_one(query, data)


    # Función principal de la operación de comunicación con microcontrolador Arduino
    def arduino_worker(self):
        while(True):
            str_enviarArduino=""

            self.getInfo_DB()
            self.readArduino_Serial()

            if(self.temp_sens<self.temp_pref):
                str_enviarArduino = "act?a0:t|a1:f;"
                self.updateInfo_DB("t","f")
            elif(self.temp_sens>self.temp_pref):
                str_enviarArduino = "act?a0:f|a1:t;"
                self.updateInfo_DB("f","t")
            elif(self.temp_sens>=self.temp_min and self.temp_sens<=self.temp_max):
                self.updateInfo_DB("f","f")
                if(self.act0_status=="t"):
                    self.act1_status = "f"
                    str_enviarArduino = "act?a0:t|a1:f;"
                elif(self.act1_status=="t"):
                    str_enviarArduino = "act?a0:f|a1:t;"
                    self.act1_status = "t"
                else:
                    str_enviarArduino = "act?a0:f|a1:f;"
                    self.act1_status = self.act0_status = "t"
            
            self.writeArduino_Serial(str_enviarArduino)
from pyDatalog import pyDatalog, Logic

con = ''
first=''

class knowledgebase:
    def __init__(self,conexion):
        print('KB loaded')
        self.con = conexion
        self.first=Logic(True)

        pyDatalog.load("""
            #Reglas para la inferencia de la edad
            #Niñez
            + stage_life('0','childhood')
            + stage_life('1','childhood')
            + stage_life('2','childhood')
            + stage_life('3','childhood')
            + stage_life('4','childhood')
            + stage_life('5','childhood')
            + stage_life('6','childhood')
            + stage_life('7','childhood')
            + stage_life('8','childhood')
            + stage_life('9','childhood')
            + stage_life('10','childhood')
            + stage_life('11','childhood')
            + stage_life('12','childhood')
            + stage_life('13','childhood')
            + stage_life('14','childhood')
            + stage_life('15','childhood')
            + stage_life('16','childhood')
            + stage_life('17','childhood')

            #Adulto
            + stage_life('18','adulthood')
            + stage_life('19','adulthood')
            + stage_life('20','adulthood')
            + stage_life('21','adulthood')
            + stage_life('22','adulthood')
            + stage_life('23','adulthood')
            + stage_life('24','adulthood')
            + stage_life('25','adulthood')
            + stage_life('26','adulthood')
            + stage_life('27','adulthood')
            + stage_life('28','adulthood')
            + stage_life('29','adulthood')
            + stage_life('30','adulthood')
            + stage_life('31','adulthood')
            + stage_life('32','adulthood')
            + stage_life('33','adulthood')
            + stage_life('34','adulthood')
            + stage_life('35','adulthood')
            + stage_life('36','adulthood')
            + stage_life('37','adulthood')
            + stage_life('38','adulthood')
            + stage_life('39','adulthood')
            + stage_life('40','adulthood')
            + stage_life('41','adulthood')
            + stage_life('42','adulthood')
            + stage_life('43','adulthood')
            + stage_life('44','adulthood')
            + stage_life('45','adulthood')
            + stage_life('46','adulthood')
            + stage_life('47','adulthood')
            + stage_life('48','adulthood')
            + stage_life('49','adulthood')
            + stage_life('50','adulthood')
            + stage_life('51','adulthood')
            + stage_life('52','adulthood')
            + stage_life('53','adulthood')
            + stage_life('54','adulthood')
            + stage_life('55','adulthood')
            + stage_life('56','adulthood')
            + stage_life('57','adulthood')
            + stage_life('58','adulthood')
            + stage_life('59','adulthood')

            #Edad Adulta
            + stage_life('60','senior')
            + stage_life('61','senior')
            + stage_life('62','senior')
            + stage_life('63','senior')
            + stage_life('64','senior')
            + stage_life('65','senior')
            + stage_life('66','senior')
            + stage_life('67','senior')
            + stage_life('68','senior')
            + stage_life('69','senior')
            + stage_life('70','senior')
            + stage_life('71','senior')
            + stage_life('72','senior')
            + stage_life('73','senior')
            + stage_life('74','senior')
            + stage_life('75','senior')
            + stage_life('76','senior')
            + stage_life('77','senior')
            + stage_life('78','senior')
            + stage_life('79','senior')
            + stage_life('80','senior')
            + stage_life('81','senior')
            + stage_life('82','senior')
            + stage_life('83','senior')
            + stage_life('84','senior')
            + stage_life('85','senior')
            + stage_life('86','senior')
            + stage_life('87','senior')
            + stage_life('88','senior')
            + stage_life('89','senior')
            + stage_life('91','senior')
            + stage_life('92','senior')
            + stage_life('93','senior')
            + stage_life('94','senior')
            + stage_life('95','senior')
            + stage_life('96','senior')
            + stage_life('97','senior')
            + stage_life('98','senior')
            + stage_life('99','senior')
            + stage_life('100','senior')

            #Regla para inferir la etapa de una persona
            is_in_stage(X,Z) <= age(X,Y) & stage_life(Y,Z)


            #Limites de temperatura
            #Respiratoria
            + has_limits('respiratory','childhood','26','25')
            + has_limits('respiratory','adulthood','27','24')
            + has_limits('respiratory','senior','27','24')

            #Golpe de calor y similares
            + has_limits('heatstroke','childhood','25','22')
            + has_limits('heatstroke','adulthood','25','21')
            + has_limits('heatstroke','senior','26','22')

            #Hipotermia y similares
            + has_limits('hypothermia','childhood','29','25')
            + has_limits('hypothermia','adulthood','30','24')
            + has_limits('hypothermia','senior','30','25')

            #Otras enfermedades
            + has_limits('other','childhood','27','25')
            + has_limits('other','adulthood','28','24')
            + has_limits('other','senior','28','24')

            #Temperatura preferida anterior
            #Respiratoria
            + prefer_temperature('respiratory','childhood','24')
            + prefer_temperature('respiratory','adulthood','25')
            + prefer_temperature('respiratory','senior','26')

            #Golpe de calor y similares
            + prefer_temperature('heatstroke','childhood','22')
            + prefer_temperature('heatstroke','adulthood','23')
            + prefer_temperature('heatstroke','senior','25')

            #Hipotermia y similares
            + prefer_temperature('hypothermia','childhood','28')
            + prefer_temperature('hypothermia','adulthood','27')
            + prefer_temperature('hypothermia','senior','28')

            #Otras enfermedades
            + prefer_temperature('other','childhood','25')
            + prefer_temperature('other','adulthood','27')
            + prefer_temperature('other','senior','27')

            #Reglas para inferencia de datos de temperatura
            require_temperature(X,A) <= is_in_stage(X,Y) & sick_of(X,Z) & prefer_temperature(Z,Y,A)
            require_limits_temperature(X,A,B) <= is_in_stage(X,Y) & sick_of(X,Z) & has_limits(Z,Y,A,B)
        """)
    
    def assertPatient(self,name,age,sick):
        Logic(self.first)
        #metodo que agrega un paciente a la base de conocimiento
        pyDatalog.assert_fact('age',name,age)
        pyDatalog.assert_fact('sick_of',name,sick)

        tq2 = "sick_of("+name+",Y)"
        tq3 = "require_limits_temperature("+name+",A,B)"
        tq4 = "require_temperature("+name+",A)"
        tq5 = "is_in_stage("+name+",A)"
        q2 = pyDatalog.ask(tq2)
        q3 = pyDatalog.ask(tq3)
        q4 = pyDatalog.ask(tq4)
        q5 = pyDatalog.ask(tq5)
        db = self.con.conexion()
        coleccion = db['sensor_temp']
        query = {"activo" : "t"}
        data = {"$set":{"act0_status": "f", "act1_status" : "f", "enfermedad" : q2.answers[0][0] , "temp_min" : int(q3.answers[0][1]), "temp_max" : int(q3.answers[0][0]), "temp_pref" : int(q4.answers[0][0]), "stage": q5.answers[0][0]}}
        coleccion.update_one(query, data)
        print("mongodb updated")

        return 'saved'
    
    def readPatient(self,name):
        Logic(self.first)
        #metodo que consulta los datos del paciente actualmente presente en la base de conocimiento
        returnvalue = "" 
        try:
            tq1 = "age("+name+",Y)"
            tq2 = "sick_of("+name+",Y)"
            q1 = pyDatalog.ask(tq1)
            q2 = pyDatalog.ask(tq2)
            returnvalue = "{'name':'"+name+"','age':'"+q1.answers[0][0]+"','sick':'"+q2.answers[0][0]+"'}"   
        except:
            returnvalue = "NOPATIENT"
        return returnvalue

    def retractPatient(self,name):
        Logic(self.first)
        #Método para olvidar el paciente, recupera sus datos de la base de conocimiento y lo elimina
        returnvalue = ''
        try:
            tq1 = "age("+name+",Y)"
            tq2 = "sick_of("+name+",Y)"
            q1 = pyDatalog.ask(tq1)
            q2 = pyDatalog.ask(tq2)
            pyDatalog.retract_fact('age',name,q1.answers[0][0])
            pyDatalog.retract_fact('sick_of',name,q2.answers[0][0])
            return 'retracted'
        except:
            returnvalue = "NOPATIENT"
        return returnvalue

    def retractpreferences(self):
        Logic(self.first)
        returnvalue = ''
        try:
            db = self.con.conexion()
            coleccion = db['sensor_temp']
            query = {"activo" : "t"}
            req = list(coleccion.find(query))[0]
            
            tq1 = "prefer_temperature("+req['enfermedad']+","+req['stage']+",X)"
            q1 = pyDatalog.ask(tq1)

            pyDatalog.retract_fact('prefer_temperature',req['enfermedad'],req['stage'],q1.answers[0],[0])
            pyDatalog.assert_fact('prefer_temperature',req['enfermedad'],req['stage'],req['temp_pref'])
            return 'retracted'
        except:
            returnvalue = "NOPATIENT"
        return returnvalue

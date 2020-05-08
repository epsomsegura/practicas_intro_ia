# Librerias
import pymongo

class mongo_con:
    @staticmethod
    def conexion():
        cliente = pymongo.MongoClient("mongodb://localhost:27017/")
        dblist = cliente.list_database_names()
        if "proyecto_ia" in dblist:
            base = cliente["proyecto_ia"]
            return base
        else:
            print("No existe la base de datos")
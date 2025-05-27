#archivo de configuración
from pymongo import MongoClient #importar el cliente de pymongo
import certifi #importar certificado

#variable de conexion
MONGO="mongodb+srv://eleiva:eleiva123456@cluster0.guwgbzw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

certificado=certifi.where()

#funcion para que permite la conexción con la base de datos
def Conexion():
    try:
        client=MongoClient(MONGO, tlsCAFile=certificado)
        bd=client["nexusgame"]
    except ConnectionError:
        print("Error de conexcion")
    return bd 
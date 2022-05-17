print()
print()
print()
print()
print("        MMMMMMMMMMMMMMMMMMMMMMWWMMMMMMMMMMMMMMMMMMMM        ")
print("     MMMMMMMMMMMMMMMMMMMMMMMMMWMWXNWMMMMMMMMMMMMMMMMMMM     ")
print("   MMMMMMMMMMMMMMMMMMMMMMWWWNOxxOXWWMMMMMMMMMMMMMMMMMMMMM   ")
print("   MMMMMMMMMMMMMMMMMMMMMWNOocldONXO0WMWMMMMMMMMMMMMMMMMMM   ")
print(" MMMMMMMMMMMMMMMWMMMMWKxl;,ckOkdc,,oOOkkOKNMMMMMMMMMMMMMMMM ")
print("MMMMMMMMMMMMMMMWWWNOl,.   .'..    .....;lkNMMMMWMMMMMMMMMMMM")
print("MMMMMMMMMMMMMWWX0x;..;ol'             .,cokXWMMMMMMMMMMMMMMM")
print("MMMMMMMMMMMWKo;..   .;;.                   .:dKWMMMMMMMMMMMM")
print("MMMMMMMNKKOl::.                               .:xXWWMMWWMMMM")
print("MMMMMMMk'.. ,lodo;.                  ..          .cdOKXWMMMM")
print("MMMMMMMK; ,d0KK0XXc                  .;'       .clccld0NMMMM")
print("MMMMMMMMKxxkO0xcc;.          .,;,.    .c:.      ,kNWWMWWMMMM       UJI MOTORSPORT ELECTRONIC DEPARTMENT ")
print("MMWX0OOkkxkKNx'.,coddol:'...,xXNNk,    ,lc'      .lXMMMMMMMM")
print("MMXxcclx0NNOc;o0WMMWWMMWNK0KNWMMMWk.   .col,       cXMMMMMMM                         by                 ")
print("WXOxxk0NWWN0kKWMMMMMMMMMWWMWXXWWMWd.   .:ool'       ;0WMMMMM")
print("WWWNWWWWWNNWMWWWNWWWMWWWWMMWk;;dXx.    .:oooc.  .c'  'kWMMMM       Victor, Jordi, Antonio, Luis, Ivan,  ")
print("MXl;xNWWx,,dNMWO;,oKk::0MMMMO. .,.     .ldodo'  '0Xkc,'oNMMM               Ahmed, Izan and Mohamed      ")
print("Wd. lNWWl  :NMWd. ;O; .kMMMMk.         ;ddddd;  .kWWMWK0NMMM")
print("Wo  lWMNl  :NMWd. :k, .kMWMWd.        .oddddd:. .OMMMMMMMMMM")
print("Wl  'llc'  cOdl,  ck, .kMMMX:        .lddddddc. ,0MMMMMMMMMM")
print("Wd.........lx,...:0K:.,kWWWx.       .lxxxdddx:  cNMWMMMMMMMM        @motorsportuji ujimotorsport.uji.es ")
print(" NKKKK0K0K0XNK0KKNMWXKKKxO0,       ,oxxxxxxxd, .OWWWWMMMMMM ")
print("   MWXKXWNXXXXNXKKXXXXXOclc..,,,..:xkxdxkkxdo:,o0KXXXKKXX   ")
print("   MNK000K0O00K0kOKKOOOOx0l;OdcxkdOO0Ook000dx0KKkOK00kkKK   ")
print("     KN0KN0O0O00XKO0K00l;d;l0l:dxxKkddxOdkOdO0O0O00OOKK     ")
print("        XKOO000KXK0XNKk,ld:x0KKkddkKOdO0kkdx0O00OO0K        ")
print()
print()
print()
print()


from peewee import PostgresqlDatabase, AutoField, CharField, DateField, ForeignKeyField, Model, DateTimeField, BigIntegerField
from datetime import datetime
import serial
import time 
import paho.mqtt.client as mqtt
import multiprocessing


ahora = datetime.now()

#Este script funcionará como broker de mqtt
def enviarMQTT(Topico, Mensaje, Host="localhost", Puerto=9002):
    client = mqtt.Client(transport="websockets")
    client.connect(Host, Puerto, 60)
    client.publish(Topico, Mensaje)
    print("Se envió la data")


#Indico la base de datos de PostGres a la que mas tarde debe conectarse
pg_db = PostgresqlDatabase("my_db", user="uji_motorsport", password="ujimotorsport", host="localhost", port=5432)

#Te preguta que puerto quieres usar, y si no pones nada, coje el serial0 (default para la esp32)
def Puerto():

    Puerto = input("Que puerto estamos usando?: ")

    if Puerto == "" or Puerto ==  " ":
        Puerto = "/dev/serial0"

    return Puerto

#Te pregunta que baudrate quieres usar y si no pones nada, coje el 115200 que es el que usar la esp32
def baudRate():

    baudRate = input("Que baudrate quieres usar?: ")
    
    if baudRate == "" or baudRate == " ":
        baudRate = 115200

        return baudRate

    baudRate = int(baudRate)

    return baudRate
    
#Leo señal recibe los valores del puerto, los lee y decodifica en formato ASCII
#dev.readline lee y dev.decode decodifica
def leo_señal(dev):
    #Omitiendo lo anterior, podemos poner directamente:
    #cad = dev.readline().decode(ascii)

    cad = dev.readline()
    cad = cad.decode("ascii")

    return cad

#La calse representa una tabla dentro de la base de datos
#CUIDADO CON EL ID
class Prueba(Model):
   Id = AutoField() #BigIntegerField(primary_key=True)
   #id = peewee.BigIntegerField(primary_key=True, unique=True,
            #constraints=[peewee.SQL('AUTO_INCREMENT')])
   revoluciones = CharField()
   timestop = DateTimeField()
   
   class Meta:
       database = pg_db
#Funcion que inserta datos dentro de la base de datos dentro de una tabla. Solo recive 3 datos en una linea porque
#la SP32 relacionara los datos de 3 en 3 (Por ahora)
def insertar_datos(Tabla, dato1, dato2):

    linea = Tabla( Id=dato1,
                       revoluciones=dato2,
                       timestop= ahora)
    linea.save(force_insert=True)                   

#Funcion que se conecta a la tabla de la base datconos indicada y lee los datos que tiene
def mostrar_datos(Tabla):
    for i in Tabla.select():
        print('Id: {} - revoluciones: {} - timestop: {}'
        .format(Tabla.Id, Tabla.revoluciones, Tabla.timestop))

#La función main que llama a las anteriores funciones 
def main():
    puerto = Puerto()
    BaudRate = baudRate()
    
    dev = serial.Serial(puerto, baudrate = BaudRate)
    time.sleep(1)

    #CONEXION A MQTT
    
    #Me conecto a la base de datos
    #pg_db.connect()

    #Crea una taba llamada "Prueba" en la base de datos
    #pg_db.create_tables([Prueba])

    #BUCLE QUE PERMITE LA ENTRADA SUCCESCIVA DE DATOS EN TIEMPO REAL Y GUARDARLO EN EL MISMO TIEMPO EN LA BASE DE DATOS

    Id  = 1
    while True:

        lista = []

        lista.append(Id)
        #Lo que pasa aquí es que un dato de los 3 es el Id que ese lo ponemos nosotros. El segundo los lee por el bucle for. He hecho un for porque aunque por ahora 
        #solo susamos uno dato, luego introduciremos mas, y seria solo cambiar el range. El timestop que es el tercer dato se introduce en la propia funcion 
        for i in range(1):
            cad = leo_señal(dev)
            lista.append(cad)

        inicio = time.time()
        procesoMQTT = multiprocessing.Process(target=enviarMQTT, args=("ALSW/demo", lista[1]))
        procesoMQTT.start()
        final = time.time()
        tiempo = (final - inicio) * 1000
        print(f"El código tardo {tiempo} ms")
        time.sleep(1)
        
        #insertar_datos(Prueba, lista[0], lista[1])

        Id += 1
            
main()

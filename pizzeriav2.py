#Imports
#=======================================================================================================
import os
import json
import datetime
import copy
#=======================================================================================================
#Constantes
pizzas = [
    ['Peperoni',{'small': 5000, 'medium': 8000, 'large': 10000}],
    ['Mediterranea',{'small': 6000, 'medium': 9000, 'large': 12000}],
    ['Vegetariana',{'small': 5500, 'medium': 8500, 'large': 11000}],
]

dctos = {
    'diurno' : 0.15,
    'vespertino' : 0.2,
    'administrativo' : 0.1,
}

ventasCollection = []
ventasId = 1

directory = os.getcwd()
dbpath = os.path.join(directory, 'ventasdb.json')
#=======================================================================================================
#Utilidades
def loadVentas():
    try:
        with open(dbpath, 'r') as f:
            ventasCollection = json.load(f)
            ventasId = ventasCollection[-1]['detalle']['id']+1
            print(f"{len(ventasCollection)} ventas cargadas con éxito desde {dbpath}")
        return ventasCollection, ventasId
    except FileNotFoundError:
        print(f"No se ha encontrado archivo .json que contenga las ventas.")

def intInputChecker(opciones):
    while True:
        try:
            num = int(input(": "))
        except ValueError:
            print("Por favor ingrese un número entero.")
            continue

        if num in opciones:
            return num
        else:
            print("Por favor ingrese una opción válida.")

def reset(*args):
    for arg in args:
        if isinstance(arg, list) or isinstance(arg, dict):
            arg.clear()
        else:
            print("Por favor, ingrese una lista o un diccionario.")

def get_ventaFinalTemplate():
    return {
        'id': "",
        'cliente': "",
        'pizza': "",
        'size': [],
        'cantidad': 0,
        'dcto': [],
        'subtotal': 0,
        'total': 0,
    }
    

#=======================================================================================================   
#Menu
def menu():
    while True:
        os.system('cls')
        print(f"==== PIEZZERIA DUOC ==== \n"
            "1. Vender Pizza \n"
            "2. Mostrar todas las ventas \n"
            "3. Buscar ventas por clientes \n"
            "4. Guardar las ventas \n"
            "5. Cargar las ventas desde un archivo \n"
            "6. Generar Boleta \n"
            "7. Salir. \n")
        opciones = [1, 2, 3, 4, 5, 6, 7]
        choice = intInputChecker(opciones)
        return choice
    
#=======================================================================================================
#Venta.
def opt1(): 
    while True:
        os.system('cls')
        print(f"==== VENTA DE PIZZA ==== \n"
            "Ingrese el nombre/ID del cliente: \n")
        cliente = str(input(": "))
        tracker = [f"Cliente: {cliente}",]
        os.system('cls')
        print('\n'.join(tracker))
        print("================================ \n"
            "Seleccione el tipo de pizza: \n"
            "1. Peperoni \n"
            "2. Mediterranea \n"
            "3. Vegetariana \n")
        opciones = [1, 2, 3]
        pizza = intInputChecker(opciones)
        tracker.append(f"Tipo de pizza: {pizzas[pizza-1][0]}")
        os.system('cls')
        print('\n'.join(tracker))
        print("================================= \n"
            "Selecione el tamaño de la pizza: \n"
            "1. Pequeña \n"
            "2. Mediana \n"
            "3. Familiar \n")
        pizzaSize = intInputChecker(opciones)
        tracker.append(f"Tamaño de la pizza: {list(pizzas[pizza-1][1].keys())[pizzaSize-1]}")
        os.system('cls')
        print('\n'.join(tracker))
        print("================================ \n"
              "ingrese cantidad de pizzas: \n")
        cantidad = intInputChecker(range(1, 999999999999999999999))
        tracker.append(f"Cantidad de pizzas: {cantidad}")
        os.system('cls')
        print('\n'.join(tracker))
        print("=============================== \n"
            "Que descuento aplica: \n"
            "1. Estudiante diurno \n"
            "2. Estudiante vespertino \n"
            "3. Administrativo \n")
        dctoApplied =  intInputChecker(opciones)
        tracker.append(f"Descuento aplicado: {list(dctos.keys())[dctoApplied-1]}")
        os.system('cls')
        print('\n'.join(tracker))
        break
    #Todos los datos requeridos completados.
    #==========================================================
    #Extraer inputs y devolver objeto venta preeliminar.
    global ventasId
    pizzaType = pizzas[pizza-1][0]
    pizzaSize = list(pizzas[pizza-1][1].keys())[pizzaSize-1]
    dctoApplied = list(dctos.keys())[dctoApplied-1]
    ventaPreeliminar = {
        'id': ventasId,
        'cliente': cliente,
        'pizza': pizzaType,
        'size': [pizzaSize, pizzas[pizza-1][1][pizzaSize]],
        'cantidad': cantidad,
        'dcto': [dctoApplied, dctos[dctoApplied]],
    }
    ventaTracked = ventaTracker(ventaPreeliminar)
    ventasId += 1
    return ventaTracked


def procesoPago(ventaTracked):#Recoradar ejecutar y guardar en variable. 
    subtotal = ventaTracked['size'][1]*ventaTracked['cantidad']
    dcto = round(ventaTracked['dcto'][1]*subtotal)
    total = subtotal - dcto
    paymentInfo = {
        'subtotal': subtotal,
        'dcto': dcto,
        'total': total,
    }
    ventaFinal = ventaTracker(paymentInfo)
    return ventaFinal

#========================================================================================================
#Mostrar todas las ventas.
def mostrarVentas(filter = None):
    if filter == None:
        for venta in ventasCollection:
            print(f"{venta['registeredName']}")
            for key, value in venta['detalle'].items():
                print(f"{key}: {value}")
            print("\n")
    else:
        for venta in ventasCollection:
            if venta['detalle']['cliente'] == filter:
                print(f"{venta['registeredName']}")
                for key, value in venta['detalle'].items():
                    print(f"{key}: {value}")
                print("\n")
def opt2():
    if ventasCollection == []:
        print("No hay ventas registradas.")
    elif ventasCollection != []:
        mostrarVentas()
#=======================================================================================================
#Buscar ventas por cliente.
def getClients():
    clients = []
    for venta in ventasCollection:
        if venta['detalle']['cliente'] not in clients:
            clients.append(venta['detalle']['cliente'])
    return clients

def opt3(): 
    clients = getClients()
    if clients == []:
        print("No hay ventas registradas.")
        input()
    else:
        while True:
            print("Clientes registrados: \n")
            for name in clients:
                print(name)
            print("Ingrese el nombre del cliente que desea buscar: ")
            client = str(input(": "))
            if client in clients:
                os.system('cls')
                print(f"Ventas de {client}: \n")
                mostrarVentas(client)
                input()
                break
            else:
                print("Cliente no encontrado.")
                input()
                os.system('cls')

#=======================================================================================================
#Guardar las ventas.

#Trackea el proceso de venta y crea el objeto ventaFinal.
ventaFinalTemplate = get_ventaFinalTemplate()
def ventaTracker(ventaPreeliminar):
    ventaPreeliminarKeys=set(ventaPreeliminar.keys())
    ventaFinalTemplateKeys=set(ventaFinalTemplate.keys())
    for key in ventaFinalTemplateKeys:
        if key in ventaPreeliminarKeys:
            if ventaFinalTemplate[key] != "" and ventaFinalTemplate[key] != 0 and ventaFinalTemplate[key] != []:
                if isinstance(ventaFinalTemplate[key], list):
                    ventaFinalTemplate[key].append(ventaPreeliminar[key])
                else:
                    ventaFinalTemplate[key] = [ventaFinalTemplate[key], ventaPreeliminar[key]]
            else:
                ventaFinalTemplate[key] = ventaPreeliminar[key]
    return ventaFinalTemplate
    

def addVenta(ventaFinal): 
    global ventasCollection
    now = datetime.datetime.now()
    formatted_now = now.strftime("%d/%m/%Y, %H:%M:%S")
    ventaCollectionIdString = f"venta_{ventaFinal['id']} - {formatted_now}"
    ventaData = {
        'registeredName': ventaCollectionIdString,
        'detalle': copy.deepcopy(ventaFinal)
    }
    ventasCollection.append(ventaData)
    
def opt4():
    if ventasCollection == []:
        print("No hay ventas registradas.")
    else:
        with open(dbpath, 'w') as f:
            json.dump(ventasCollection, f)
        print(f"{len(ventasCollection)} ventas guardadas en con éxito en {dbpath}")
  

#=======================================================================================================
#Cargar las ventas desde un archivo.
def opt5(): 
    global ventasCollection, ventasId
    try:
        ventasCollection, ventasId = loadVentas()
    except TypeError:
        pass

#=======================================================================================================
#Generar Boleta.
def generarBoleta(detalleVenta):
    now = datetime.datetime.now()
    formatted_now = now.strftime("%d/%m/%Y, %H:%M:%S")
    subtotal = detalleVenta['subtotal']
    dcto = detalleVenta['dcto'][2]
    total = detalleVenta['total']
    boleta = f"==== BOLETA DE VENTA ==== \n"
    boleta += f"ID: {detalleVenta['id']} \n"
    boleta += f"Cliente: {detalleVenta['cliente']} \n"
    boleta += f"{detalleVenta['cantidad']} : {detalleVenta['pizza']} {detalleVenta['size'][0]} \n" #Tamaño en español y agregar cantidad opcional
    boleta += f"-------------------------------- \n"
    boleta += f"SUBTOTAL: {subtotal} \n"
    boleta += f"DESCUENTO: -{dcto} \n"
    boleta += f"TOTAL: {total} \n"
    boleta += f"-------------------------------- \n"
    boleta += f"Gracias por su compra! \t\t {formatted_now}"
    return boleta

#Pregunta por boleta y la imprime.
def opt6(): 
    if ventasCollection == []:
        print("No hay ventas registradas.")
    else:
        mostrarVentas()
        print("Ingrese el ID de la venta que desea generar la boleta (sólo número): ")
        ventaId= intInputChecker(range(1, len(ventasCollection)+1))
        detalleVenta = ventasCollection[ventaId-1]['detalle']
        os.system('cls')
        print(generarBoleta(detalleVenta))
        
#====== EJECUCION =======
while True:
    choice = menu()
    if choice == 1: #Ingresar venta
        ventaTracked = opt1() #Inicia la venta capturando los datos pero sin procesar el pago.
        ventaFinal = procesoPago(ventaTracked) #Procesa el pago y genera el objeto ventaFinal.
        ventaFinalTemplate = get_ventaFinalTemplate() #Obtiene una nueva plantilla de venta para la siguiente venta.
        print("=====================================")
        print("Es esta venta correcta? \n"
              "1. Si \n"
              "2. No")
        isValid = intInputChecker([1, 2])
        if isValid == 1:
            os.system('cls')
            addVenta(ventaFinal) #Agrega la venta a la colección de ventas.
            reset(ventaTracked) #Resetea la venta preeliminar, la ventaFinal y la ventaTracked, al ser estas referencias de la una a la otra.
            print("Venta registrada con éxito.")
            input()
        elif isValid == 2:
            os.system('cls')
            reset(ventaTracked)
            ventasId -= 1
            print("Venta cancelada.")
            input()
    elif choice == 2: #Muestra las ventas
        os.system('cls')
        opt2()
        input()
        print("\033[H\033[3J", end="") #Limpia el buffer de la terminal.
    elif choice == 3:#Buscar ventas por cliente
        os.system('cls')
        opt3()
        print("\033[H\033[3J", end="")
    elif choice == 4: #Guarda las ventas
        os.system('cls')
        opt4()
        input()
    elif choice == 5: #Carga las ventas
        os.system('cls')
        opt5()
        input()
    elif choice == 6: #Imprime las boletas
        os.system('cls')
        opt6()
        input()
    elif choice == 7:
        break

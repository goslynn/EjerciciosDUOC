#REFACTORIZAR todo
#Imports
#=======================================================================================================
import os
import json
import datetime
import copy
#=======================================================================================================
#Constantes
#Juego Consola Precio para Boleta
juegos = [
    ["Princess Peach:Showtime!",{'consola':'nintendo', 'tipo':'Aventura', 'precio':27990 }],
    ["Mario vs. Donkey Kong",{'consola':'nintendo', 'tipo':'Aventura', 'precio':31990 }],
    ["Hogwarts Legacy",{'consola':'nintendo', 'tipo':'Aventura', 'precio':28990 }],
    ["METAL SLUG ATTACK RELOADED",{'consola':'PS5', 'tipo':'Accion', 'precio':9990 }],
    ["Crown Wars",{'consola':'PS5', 'tipo':'Accion', 'precio':36990 }],
    ["EA SPORTS FC 24 FIFA 24",{'consola':'PS5', 'tipo':'Deporte', 'precio':26990 }],
]

dctos = {
    'socio' : 0.2,
    'estudiante' : 0.15,
    'trabajador' : 0.1,
}

ventasCollection = []
ventasId = 1

directory = os.getcwd()
dbpath = os.path.join(directory, 'ventasdb.json')
#=======================================================================================================
#Utilidades


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
        'id': 0,
        'cliente': "",
        'juego': [],
        'precio': [],
        'consola': [],
        'tipo': [],
        'cantidad': [],
        'dcto': [],
        'subtotal': 0,
        'total': 0,
    }
    

#=======================================================================================================   
#Menu
def menu():
    while True:
        os.system('cls')
        print(f"==== MICROPLAY ==== \n"
            "1. Vender Juegos \n"
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
    tracker = {'juego': [], 'cantidad':[] , 'precio': []}
    addMore = True
    while True:
        if 'cliente' not in tracker:
            os.system('cls')
            print(f"==== VENTA DE JUEGOS ==== \n"
                "Ingrese el nombre/ID del cliente: ")
            cliente = str(input(": "))
            tracker['cliente'] = cliente
            os.system('cls')
            for key, value in tracker.items():
                print(f"{key}: {value}")
        if addMore == True:
            print("================================ \n"
                "Seleccione el Juego que quiere comprar:")
            for i in juegos:
                print(f" {juegos.index(i)+1} {i[0]}")
            juego = intInputChecker(list(range(1,len(juegos)+1)))
            tracker['juego'].append(juegos[juego-1][0])
            tracker['precio'].append(juegos[juego-1][1]['precio'])
            os.system('cls')
            for key, value in tracker.items():
                print(f"{key}: {value}")
        if addMore == True:
            print("================================ \n"
                "ingrese unidades del juego que vende:")
            cantidad = intInputChecker(range(1, 999999999999999999999))
            tracker['cantidad'].append(cantidad)
            os.system('cls')
            for key, value in tracker.items():
                print(f"{key}: {value}")
        if 'dcto' not in tracker:
            print("=============================== \n"
                "Que descuento aplica: \n"
                "1. Socio \n"
                "2. Estudiante \n"
                "3. Trabajador ")
            dctoApplied =  intInputChecker([1,2,3])
            tracker['dcto'] = [list(dctos.keys())[dctoApplied-1], list(dctos.values())[dctoApplied-1]]
            os.system('cls')
            for key, value in tracker.items():
                print(f"{key}: {value}")
        print("================================ \n"
            "Desea Agregar mas juegos a la compra?: \n"
            "1. Si \n"
            "2. No ")
        addMore = intInputChecker([1,2])
        os.system('cls')
        if addMore == 1:
            addMore = True
        else:
            addMore = False
            break

    #Todos los datos requeridos completados.
    #==========================================================
    #Extraer inputs y devolver objeto venta preeliminar.
    global ventasId
    tracker['id'] = ventasId
    tracker['tipo'] = []
    tracker['consola'] = []
    for i in tracker['juego']:
        for j in juegos:
            if i == j[0]:
                tracker['tipo'].append(j[1]['tipo'])
                tracker['consola'].append(j[1]['consola'])
    ventasId += 1
    ventaPreeliminar = ventaTracker(tracker)
    return ventaPreeliminar


def procesoPago(ventaTracked):#Recoradar ejecutar y guardar en variable. 
    subtotal = 0
    for i in range(len(ventaTracked['juego'])):
        subtotal += ventaTracked['precio'][i] * ventaTracked['cantidad'][i]
    dcto = round(ventaTracked['dcto'][1]*subtotal) #el descuento se aplica a cada item, o solo se aplica al subtotal?. 
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
def mostrarVentas(filter = None): #make filter dynamic
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
def loadVentas():
    try:
        with open(dbpath, 'r') as f:
            ventasCollection = json.load(f)
            ventasId = ventasCollection[-1]['detalle']['id']+1
            print(f"{len(ventasCollection)} ventas cargadas con éxito desde {dbpath}")
        return ventasCollection, ventasId
    except FileNotFoundError:
        print(f"No se ha encontrado archivo .json que contenga las ventas.")
        
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
    itemString = ""
    for i in range(len(detalleVenta['juego'])):
        itemString += f"\t {detalleVenta['juego'][i]} \t {detalleVenta['consola'][i]} \t {detalleVenta['tipo'][i]} \t {detalleVenta['cantidad'][i]} \t {detalleVenta['precio'][i]} \n"
    boleta = f"==== BOLETA DE VENTA ==== \n"
    boleta += f"ID: {detalleVenta['id']} \n"
    boleta += f"Cliente: {detalleVenta['cliente']} \n"
    boleta += f"Deglose:\n"
    #boleta += f"\t Juego \t Consola \t Genero \t Cantidad \t Precio Unitario\n"
    boleta += itemString
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
        ventaId= intInputChecker(range(1, ventasCollection[-1]['detalle']['id']+1))
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

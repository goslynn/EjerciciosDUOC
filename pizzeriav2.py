#Recordar
#1. Crear el archivo que guarde las ventas e inicializar el dict en este (json)
#2. Considerar la necesidad de un Id de usuario
#3. Venta y boleta va aparte, supongo que se deberá guardar la venta hasta que se genere boleta
#y en el caso de que ingrese mas ventas sin generar boleta, se deberá guardar en un archivo temporal y cuando genere
#la boleta mostrará todas las boletas pendientes, adicionalmente si hay boleta pendiente y inicia otra venta 
#preguntar si desea hacerlo. 
#4. Al salir sin haber guardado cambios preguntar si desea guardarlos.
#=======================================================================================================
import os
import json
import datetime
import copy

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

directory = os.getcwd()
ventaIdPath = os.path.join(directory, 'ventasId.json')

def loadVentasId():
    try:
        with open(ventaIdPath, 'r') as f:
            ventasId = json.load(f)
    except FileNotFoundError:
        ventasId = 1
    return ventasId

ventasId = loadVentasId()


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
        'id': "",
        'cliente': "",
        'pizza': "",
        'size': [],
        'dcto': [],
        'subtotal': 0,
        'total': 0,
    }
        
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
    #agregar opcion para reiterar la venta. por ahora lo probare como esta
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
        'dcto': [dctoApplied, dctos[dctoApplied]],
        #debe pedir cantidad?
    }
    ventaTracked = ventaTracker(ventaPreeliminar)
    ventasId += 1
    return ventaTracked

#Recoradar ejecutar y guardar en variable. 
def procesoPago(ventaTracked):
    paymentInfo = {
        'subtotal': ventaTracked['size'][1],
        'dcto': round(ventaTracked['dcto'][1]*ventaTracked['size'][1]),
    }
    paymentInfo['total'] = paymentInfo['subtotal'] - (paymentInfo['dcto'])
    print(f"paymentInfo: {paymentInfo}")
    ventaFinal = ventaTracker(paymentInfo)
    return ventaFinal

#Mostrar todas las ventas.
def opt2(): 
    pass

#Buscar ventas por cliente.
def opt3(): 
    pass



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
        ventaCollectionIdString: copy.deepcopy(ventaFinal)
    }
    ventasCollection.append(ventaData)
    
def opt4():
    pass






#Cargar las ventas desde un archivo.
def opt5(): 
    pass

#Generar Boleta.
def opt6(ventaFinal): 
    #Calculando los pagos.
    now = datetime.datetime.now()
    formatted_now = now.strftime("%d/%m/%Y, %H:%M:%S")
    subtotal = ventaFinal['subtotal']
    dcto = ventaFinal['dcto'][1]
    total = ventaFinal['total']
    #Generando la boleta.
    boleta = f"==== BOLETA DE VENTA ==== \n"
    boleta += f"ID: {ventaFinal['id']} \n"
    boleta += f"Cliente: {ventaFinal['cliente']} \n"
    boleta += f"1 : {ventaFinal['pizza']} {ventaFinal['size'][0]} \n"
    boleta += f"-------------------------------- \n"
    boleta += f"SUBTOTAL: {subtotal} \n"
    boleta += f"DESCUENTO: -{subtotal*dcto} \n"
    boleta += f"TOTAL: {total} \n"
    boleta += f"-------------------------------- \n"
    boleta += f"Gracias por su compra! \t\t {formatted_now}"
    print(boleta)

#======= EJECUCION =======
while True:
    choice = menu()
    if choice == 1:
        ventaTracked = opt1() #Inicia la venta capturando los datos pero sin procesar el pago.
        ventaFinal = procesoPago(ventaTracked) #Procesa el pago y genera el objeto ventaFinal.
        addVenta(ventaFinal) #Agrega la venta a la colección de ventas.
        reset(ventaTracked) #Resetea la venta preeliminar, la ventaFinal y la ventaTracked, al ser estas referencias de la una a la otra.
        ventaFinalTemplate = get_ventaFinalTemplate() #Obtiene una nueva plantilla de venta para la siguiente venta.
        input()
        os.system('cls')
        print(f"ventaFinal: {ventaFinal} \n"
              f"ventaTracked: {ventaTracked} \n"
              f"ventaFinalTemplate: {ventaFinalTemplate} \n"
              f"ventasCollection: {ventasCollection} \n")
        input()
    elif choice == 2:
        pass
    elif choice == 3:
        pass
    elif choice == 4: #Hacer que funcione el json
        opt4(ventaFinal)
        reset(ventaFinal,ventaTracked)
        print(f"ventaFinal: {ventaFinal} \n"
              f"ventaTracked: {ventaTracked} \n"
              f"ventasCollection: {ventasCollection} \n")   
        input()
    elif choice == 5: 
        pass
    elif choice == 6: #Replantear como se imprimen las boletas. 
        opt6(ventaFinal)
        input()
    elif choice == 7:
        break

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

directory = os.getcwd()
ventaIdPath = os.path.join(directory, 'ventasId.json')

def loadVentasId():
    try:
        with open(ventaIdPath, 'r') as f:
            ventasId = json.load(f)
    except FileNotFoundError:
        ventasId = 0
    return ventasId

ventasId = loadVentasId()

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


def menu():
    while True:
        os.system('cls')
        print(f"==== PIEZZERIA DUOC ==== \n"
            "1. Vender Pizza \n"
            "2. Mostrar todas las ventas \n"
            "3. Buscar ventas por clientes \n"
            "4. Guardar las ventas \n"
            "5. Cargar todas las ventas \n"
            "6. Generar Boleta \n"
            "7. Salir. \n")
        opciones = [1, 2, 3, 4, 5, 6, 7]
        choice = intInputChecker(opciones)
        return choice

def opt1(): #Venta.
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
        input()
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
    ventasId += 1 #recordar que al escribir la funcion de guardar se deben crear 2 json separados.
    return ventaPreeliminar

def opt2(): #Mostrar todas las ventas.
    pass

def opt3(): #Buscar ventas por cliente.
    pass

def opt4(): #Guardar las ventas.
    pass
 
def opt5(): #Cargar todas las ventas.
    pass

def opt6(ventaPreeliminar): #Generar Boleta.
    #Calculando los pagos.
    now = datetime.datetime.now()
    formatted_now = now.strftime("%d/%m/%Y, %H:%M:%S")
    subtotal = ventaPreeliminar['size'][1]
    dcto = ventaPreeliminar['dcto'][1]
    total = subtotal - (subtotal * dcto)
    #Generando la boleta.
    boleta = f"==== BOLETA DE VENTA ==== \n"
    boleta += f"ID: {ventaPreeliminar['id']} \n"
    boleta += f"Cliente: {ventaPreeliminar['cliente']} \n"
    boleta += f"1 : {ventaPreeliminar['pizza']} {ventaPreeliminar['size'][0]} \n"
    boleta += f"-------------------------------- \n"
    boleta += f"SUBTOTAL: {subtotal} \n"
    boleta += f"DESCUENTO: -{subtotal*dcto} \n"
    boleta += f"TOTAL: {total} \n"
    boleta += f"-------------------------------- \n"
    boleta += f"Gracias por su compra! \t\t {formatted_now}"
    return boleta

#======= EJECUCION =======
while True:
    choice = menu()
    if choice == 1:
        ventaPreeliminar = opt1()
        print(ventaPreeliminar)
    elif choice == 2:
        pass
    elif choice == 3:
        pass
    elif choice == 4:
        pass
    elif choice == 5:
        pass
    elif choice == 6:
        boletaStr = opt6(ventaPreeliminar)
        print(boletaStr)
        input()
    elif choice == 7:
        break

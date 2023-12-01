"""
27/11/2023

Práctica del examen para realizar en casa
-----------------------------------------

* El programa debe estar correctamente documentado.

* Debes intentar ajustarte lo máximo que puedas a lo que se pide en los comentarios TODO.

* Tienes libertad para desarrollar los métodos o funciones que consideres, pero estás obligado a usar como mínimo todos los que se solicitan en los comentarios TODO.

* Además, tu programa deberá pasar correctamente las pruebas unitarias que se adjuntan en el fichero test_agenda.py, por lo que estás obligado a desarrollar los métodos que se importan y prueban en la misma: pedir_email(), validar_email() y validar_telefono()

"""

import os
import pathlib
from os import path

# Constantes globales
RUTA = pathlib.Path(__file__).parent.absolute() 

NOMBRE_FICHERO = 'contactos.csv'

RUTA_FICHERO = path.join(RUTA, NOMBRE_FICHERO)

#TODO: Crear un conjunto con las posibles opciones del menú de la agenda
OPCIONES_MENU = {1,2,3,4,5,6,7,8}
#TODO: Utiliza este conjunto en las funciones agenda() y pedir_opcion()


def borrar_consola():
    """ Limpia la consola
    """
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")
        
def mostrar_menu():
    """Muestra un menú sencillo con las diferentes opciones de la agenda
    """
    print(" AGENDA")
    print("-"*8)
    print("""
    1. Nuevo contacto
    2. Modificar contacto
    3. Eliminar contacto
    4. Vaciar agenda
    5. Cargar agenda inicial
    6. Mostrar contactos por criterio
    7. Mostrar la agenda completa
    8. Salir""")
    
def pedir_opcion():
    """Solicita al usuario que ingrese una opción de 1 al 8 y controla que el usuario ingrese algo que no corresponda
    Retruns:
        opcion (int) -> Retorna un entero como resultado
    """
    try: 
        opcion=int(input(">> Seleccione una opción (1-8): "))
    except ValueError:
        return -1
    else:
        return opcion
    
def cargar_contactos(contactos: list):
    """ Carga los contactos iniciales de la agenda desde un fichero
    Args:
        contactos (list) -> Una lista vacía a la que se le añadirán diccionarios con los datos de los contactos
    Returns:
        emails (list) -> Una lista con los emails de los contactos para comprobar si estos se repetirán posteriormente
        contactos(list) -> La misma lista que toma como argumento, pero ya con los datos 
    """
    #TODO: Controlar los posibles problemas derivados del uso de ficheros...
    emails = []

    with open(RUTA_FICHERO, 'r') as fichero:
        for linea in fichero:
            datos = linea.split(";")
            nombre = datos[0]
            apellidos = datos[1]
            email = datos[2].strip("\n")
            telefonos = []
            for i in range(3, len(datos)):
                telefono = datos[i]
                telefono.split(" ")
                telefonos.append(telefono.replace("\n",""))
            contacto = {'nombre':nombre,'apellido': apellidos,'email':email,'telefonos':telefonos}
            contactos.append(contacto)
            emails.append(email)
    return emails, contactos
    
def agregar_contacto(contactos: list, emails: list):
    """ Función que preguntará al usuario por los campos necesarios para crear un nuevo contacto
    Args:
        contactos (list) -> Una lista anidada con diccionarios con los datos correspondientes de cada contacto
        emails (list) -> Una lista con todos los emails de los usuarios iniciales
    """
    telefonos = []
    valido = False

#Va a pedir 1 por 1 al usuario que ingrese el dato correspondiente y hasta que este no cumpla las condiciones no continua
   
    while valido == False:
        nombre = (input("Ingrese el nombre: ")).title()
        if nombre == "":
            print("Formato de nombre no válido")
        else:
            valido = True
    valido = False

    while valido == False:
        apellidos = (input("Ingrese el apellido: ")).title()
        if apellidos == "":
            print("Formato de apellido no válido")
        else:
            valido = True
    valido = False

    while valido == False:
        try:
            email = pedir_email(emails)
            if email != None:
                emails.append(email)
                valido = True
        except ValueError as e:
            print(e)

    print("Para dejar de introducir teléfonos presione ENTER")
    telefono = (input("Ingrese el teléfono: "))
    if telefono == "":
        telefonos = "Ninguno"
    else:
        while telefono != "":
            validar_telefono(telefono)
            if validar_telefono(telefono) == True:
                telefonos.append(telefono)
            else:
                print("Numero de teléfono no válido")
            telefono = (input("Ingrese el teléfono: "))
    
    datos = {"nombre":nombre,"apellido":apellidos,"email":email,"telefonos":telefonos}
    contactos.append(datos)
    
def validar_telefono(telefono:str):
        """Funcion que va a comprobar si el teléfono introducido por el usuario cumple los requisitos o no
        Args: 
            telefono (str) -> Número de telefono ingresado por el usuario
        Returns:
            bool -> Retorna un booleano en caso de que el teléfono cumpla los requisitos o no
        """
        telefono.strip(" ")
        if "-" in telefono:
            prefijo = telefono.split("-")
            if prefijo[0] != '+34':
                return False
        if "-" not in telefono and "+34" in telefono:
            return True
        if "+" in telefono:
            telefono[1:2].split()
            if telefono[0] != 34:
                return False
            else: 
                return True
        if len(telefono) == 12 or len(telefono) == 9 and telefono != int:
            return True
        else:
            return False
  
def pedir_email(emails: list):
    """Función que pide al usuario que ingrese un email y comprueba su validez.
    Args:
        emails (list) -> lista en la que el programa se va a basar para comprobar si el email es repetido o no
    Returns:
        email (str) -> retorna una cadena con el email del usuario en caso de que sea válido, sino, retornará un booleano indicandolo
    
    """
    valido = False

    while valido ==False:
        email = str(input("Ingrese el email: "))
        validar_email(email, emails)
        if email == "" or email == " ":
            raise ValueError("el email no puede ser una cadena vacía")
        elif "@" not in email:
            raise ValueError("el email no es un correo válido")
        elif email in emails:
            raise ValueError("el email ya existe en la agenda")
        else:
            valido = True
            return email


def validar_email(email:str, emails: list):
    """Funcion que únicamente comprueba la validez de un email
    Args:
        email (str) -> Cadena ingresada por el usuario
        emails (lista) -> Lista de emails ingresados previamente
    Returns:
        bool -> En caso de que el email sea válido
    """
    if email == "" or email == " ":
        raise ValueError("el email no puede ser una cadena vacía")
    elif "@" not in email:
        raise ValueError("el email no es un correo válido")
    elif email in emails:
        raise ValueError("el email ya existe en la agenda") 
    else:
        return email, True
  
def buscar_contacto(contactos:list, email:str):
    """Función que busca a un contacto en función de un email
    Args:
        contactos (list) -> Lista anidada con diccionarios con la información correspondiente de cada contacto
        email (str) -> cadena inngresada por el usuario en función a la cual se va a bucar a un contacto
    Returns:
        pos (int) -> valor posicional de el contacto en la lista contactos
        None -> en caso de que no se ecuentre el contacto
    """
    cont = 0
    for contacto in contactos:
        if contacto["email"] == email:
            pos = cont
            return pos
        cont +=1
    return None

def eliminar_contacto(contactos: list, email:str, emails: list):
    """ Elimina un contacto de la agenda
    Args:
        contactos (list) -> lista con todos los contactos y su información correspondiente
        email (str) -> cadena ingresada por el usuario, la primera ejecución, toma un valor predefinido
        emails (list) -> lista con todos los emails ya ingresados
    """
    try:
        #TODO: Crear función buscar_contacto para recuperar la posición de un contacto con un email determinado
        primera_vez = True
        if primera_vez == False:
            email = str(input("Ingrese el email del contacto a borrar:"))
        pos = buscar_contacto(contactos, email)
        if pos != None:
            emails.remove(email)
            del contactos[pos]
            print("Se eliminó 1 contacto")
            email = ""
            primera_vez = False
    except Exception as e:
        print(f"**Error** {e}")
        print("No se eliminó ningún contacto")

def mostrar_contactos(contactos:list, contactos_ordenados: list):
    """Función qu ese encarga de mostrar los contactos en la consola, llama a ordenar_contactos() en el proceso
    Args:
        contactos (list) -> lista original de contactos con la informacion de los clientes
        contactos_ordenados (list) -> copia de la original (contactos) ordenada alfabéticamente
    """
    contactos_ordenados = ordenar_contactos(contactos)
    for contacto in contactos_ordenados:
        if contacto['telefonos'] == "" or contacto['telefonos'] == [""]:
            contacto['telefonos'] == "Ninguno"
    cantidad_contactos = 0
    for _ in contactos_ordenados:
        cantidad_contactos +=1
    print(f" AGENDA {cantidad_contactos}")
    print("-"*10)
    for contacto in contactos_ordenados:
        print(f"Nombre: {contacto["nombre"]} {contacto["apellido"]}     ({contacto["email"]})", end=("\n"))
        print(f"Teléfonos: {contacto["telefonos"][0:]}")
        print("."*10)

def ordenar_contactos(contactos:list):
    """Función ordenadora alfabeticamente
    Args:
        contactos (list) -> lista anidada con la información de los contactos del usuario
    Returns:
        contactos_ordenados (list) -> copia de la original ordenada alfabéticamente 
    """
    contactos_ordenados = []
    orden = contactos.copy()
    for i in range(0, len(contactos)):
        j = 0
        while j < len(orden):
            if contactos[i]['nombre'] > orden[j]['nombre']:
                contactos_ordenados.append(orden[j])
                del orden[j]
            j += 1
    contactos_ordenados.append(orden[0])
    return contactos_ordenados

def filtrar_contactos(contactos: list):
    """Función encargada de filtrar los contactos en función de una característica concreta decidida por el usuario
    Args: 
        contactos (list) -> lista anidada con la información de los contactos
    """
    #Pide al usuario que ingrese un criterio y compara este criterio con las 4 posible opciones

    criterio = input("Ingrese el criterio de búsqueda; nombre, apellido, email o telefono: ").lower()
    if criterio == 'nombre':
        nombre = input("Ingrese el nombre a buscar: ").title()
        pos = 0
        for contacto in contactos:
            coincidencias = 0
            if contacto['nombre'] == nombre:
                coincidencias += 1
                imprimir_filtrado(contactos, pos, coincidencias)
            else:
                pos += 1
    elif criterio == 'apellido':
            apellido = input("Ingrese el apellido a buscar: ").title()
            pos = 0
            for contacto in contactos:
                coincidencias = 0
                if contacto['apellido'] == apellido:
                    coincidencias += 1
                    imprimir_filtrado(contactos, pos, coincidencias)
                else:
                    pos += 1
    elif criterio == 'email':
            email = input("Ingrese el email a buscar: ")
            pos = 0
            for contacto in contactos:
                coincidencias = 0
                if contacto['email'] == email:
                    coincidencias += 1
                    imprimir_filtrado(contactos, pos, coincidencias)
                else:
                    pos += 1
    elif criterio == 'telefono':
            telefono = input("Ingrese el telefono a buscar: ")
            pos = 0
            for contacto in contactos:
                coincidencias = 0
                if contacto['telefonos'] == telefono:
                    coincidencias += 1
                    imprimir_filtrado(contactos, pos, coincidencias)
                else:
                    pos += 1
    elif criterio not in {'nombre','apellido','email','telefono'}:
        print("--Opción inválida--")
    if coincidencias == 0:
        print("--No se encontraron coincidencias--")

def imprimir_filtrado(contactos: list, pos: int, coincidencias: int):
    """Función que imprime los contactos filtrados en la función anterior
    Args:
        contactos (list) -> lista anidada con la información de los contactos
        pos (int) -> número entero que indica la posición en la que se encontró una coincidencia
        coincidencias (int) -> número entero que indica el número de coincidencias encontradas
    """
    print(f" {coincidencias} Coincidencias ")
    print("-"*17)
    print(f"Nombre: {contactos[pos]["nombre"]} {contactos[pos]["apellido"]}     ({contactos[pos]["email"]})", end=("\n"))
    print(f"Teléfonos: {contactos[pos]["telefonos"][0:]}")
    print("."*10)      

def vaciar_agenda(contactos:list):
    """Vacia la lista contactos por completo"""
    contactos.clear()

def modificar_contacto(contactos:list):
    """Función que pregunra al usuario por el nombre del usuario a modificar y posteriormente por que característica de este desea modificar
    Args:
        contactos (list) -> lista anidada con la información de los contactos del usuario   
    """
    nombre = input("Ingrese el nombre del contacto a modificar: ").title()
    for contacto in contactos:
        if contacto["nombre"] == nombre:
            modificar = True
            while modificar:
                cambio = str(input("Ingrese que es lo que desea modificar, nombre, apellido, email o teléfono: "))
                if cambio == "nombre":
                    contacto["nombre"] = input("Ingrese el nuevo nombre: ").title()
                    usuario = input("¿Desea seguir modificando datos del mismo contacto? (s/n): ")
                    if usuario in {'s','S'}:
                        modificar = True
                    else:
                        modificar = False
                elif cambio == "apellido":
                    contacto['apellido'] = input("Ingrese el nuevo apellido: ").title()
                    usuario = input("¿Desea seguir modificando datos del mismo contacto? (s/n): ")
                    if usuario in {'s','S'}:
                        modificar = True
                    else:
                        modificar = False
                elif cambio == "email":
                    email = input("Ingrese el nuevo email: ")
                    validar_email(email, contactos)
                    if validar_email == True:
                        contacto['email'] = email
                        usuario = input("¿Desea seguir modificando datos del mismo contacto? (s/n): ")
                    if usuario in {'s','S'}:
                        modificar = True
                    else:
                        modificar = False
                elif cambio == "telefono":
                    opcion = input("¿Desea añadir o modificar un número de teléfono? (A/M): ")
                    if opcion in {'a','A'}:
                        telefono = input("Ingrese el numero de teléfono a añadir: ")
                        if validar_telefono(telefono) == True:
                            if contacto['telefonos'] == "":
                                contacto['telefonos'] = telefono
                            else:
                                contacto['telefonos']+=telefono
                        else: 
                            print("Teléfono no válido")
                    elif opcion in {'m','M'}:
                        cual = input(f"Elija uno entre 1 y {len(contacto['telefonos'])}: ")
                        if cual in range(1, len(contacto['telefonos'])):
                            telefono = input("Ingrese el numero de teléfono a añadir: ")
                            contacto['telefonos'][int(cual)-1] = telefono
                    usuario = input("¿Desea seguir modificando datos del mismo contacto? (s/n): ")
                    if usuario in {'s','S'}:
                        modificar = True
                    else:
                        modificar = False
                else:
                    print("Opción no valida")
        else:
            print(f"No hay concidencia en {contacto['nombre']}")

def agenda(contactos: list, contactos_ordenados: list, emails: list):
    """ Ejecuta el menú de la agenda con varias opciones
    Args:
        contactos (list) -> lista anidada con la informacion de los contactos
        contactos_ordenados (list) -> lista ordenada alfabéticamente
        emails (list) -> lista de todos los emails introducidos anteriormente
    """
    #TODO: Crear un bucle para mostrar el menú y ejecutar las funciones necesarias según la opción seleccionada...
    email = "rciruelo@gmail.com"
    contactos_ordenados = []
    opcion = 0
    while opcion != 8:
        mostrar_menu()
        opcion = pedir_opcion()
        #TODO: Se valorará que utilices la diferencia simétrica de conjuntos para comprobar que la opción es un número entero del 1 al 7
        if opcion in OPCIONES_MENU ^ {8}:
            if opcion == 1:
                borrar_consola()
                agregar_contacto(contactos)
            elif opcion == 2:
                borrar_consola()
                modificar_contacto(contactos)
            elif opcion == 3:
                borrar_consola()
                eliminar_contacto(contactos, email, emails)
            elif opcion == 4:
                borrar_consola()
                vaciar_agenda(contactos)
            elif opcion == 5:
                borrar_consola()
                cargar_contactos(contactos)
            elif opcion == 6:
                borrar_consola()
                filtrar_contactos(contactos)
            elif opcion == 7:
                borrar_consola()
                mostrar_contactos(contactos, contactos_ordenados)
            pulse_tecla_para_continuar()
            borrar_consola()
        if opcion == -1:
            borrar_consola()
            print("--Opción no válida-- \n Ingrese otra opción ")
            
def pulse_tecla_para_continuar():
    """ Muestra un mensaje y realiza una pausa hasta que se pulse una tecla
    """
    print("\n")
    os.system("pause")

def main():
    """ Función principal del programa
    """
    borrar_consola()

    #TODO: Asignar una estructura de datos vacía para trabajar con la agenda
    
    contactos = []
    emails, contactos = cargar_contactos(contactos)
    contactos_ordenados = []
    email = "rciruelo@gmail.com"
    #TODO: Modificar la función cargar_contactos para que almacene todos los contactos del fichero en una lista con un diccionario por contacto (claves: nombre, apellido, email y telefonos)
    #TODO: Realizar una llamada a la función cargar_contacto con todo lo necesario para que funcione correctamente.

    #TODO: Crear función para agregar un contacto. Debes tener en cuenta lo siguiente:
    # - El nombre y apellido no pueden ser una cadena vacía o solo espacios y se guardarán con la primera letra mayúscula y el resto minúsculas (ojo a los nombre compuestos)
    # - El email debe ser único en la lista de contactos, no puede ser una cadena vacía y debe contener el carácter @.
    # - El email se guardará tal cuál el usuario lo introduzca, con las mayúsculas y minúsculas que escriba. 
    #  (CORREO@gmail.com se considera el mismo email que correo@gmail.com)
    # - Pedir teléfonos hasta que el usuario introduzca una cadena vacía, es decir, que pulse la tecla <ENTER> sin introducir nada.
    # - Un teléfono debe estar compuesto solo por 9 números, aunque debe permitirse que se introduzcan espacios entre los números.
    # - Además, un número de teléfono puede incluir de manera opcional un prefijo +34.
    # - De igual manera, aunque existan espacios entre el prefijo y los 9 números al introducirlo, debe almacenarse sin espacios.
    # - Por ejemplo, será posible introducir el número +34 600 100 100, pero guardará +34600100100 y cuando se muestren los contactos, el telófono se mostrará como +34-600100100. 
    #TODO: Realizar una llamada a la función agregar_contacto con todo lo necesario para que funcione correctamente.
    agregar_contacto(contactos, emails)

    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Realizar una llamada a la función eliminar_contacto con todo lo necesario para que funcione correctamente, eliminando el contacto con el email rciruelo@gmail.com
    eliminar_contacto(contactos, email, emails)

    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Crear función mostrar_contactos para que muestre todos los contactos de la agenda con el siguiente formato:
    # ** IMPORTANTE: debe mostrarlos ordenados según el nombre, pero no modificar la lista de contactos de la agenda original **
    #
    # AGENDA (6)
    # ------
    # Nombre: Antonio Amargo (aamargo@gmail.com)
    # Teléfonos: niguno
    # ......
    # Nombre: Daniela Alba (danalba@gmail.com)
    # Teléfonos: +34-600606060 / +34-670898934
    # ......
    # Nombre: Laura Iglesias (liglesias@gmail.com)
    # Teléfonos: 666777333 / 666888555 / 607889988
    # ......
    # ** resto de contactos **
    #
    #TODO: Realizar una llamada a la función mostrar_contactos con todo lo necesario para que funcione correctamente.
    mostrar_contactos(contactos, contactos_ordenados)

    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Crear un menú para gestionar la agenda con las funciones previamente desarrolladas y las nuevas que necesitéis:
    # AGENDA
    # ------
    # 1. Nuevo contacto
    # 2. Modificar contacto
    # 3. Eliminar contacto
    # 4. Vaciar agenda
    # 5. Cargar agenda inicial
    # 6. Mostrar contactos por criterio
    # 7. Mostrar la agenda completa
    # 8. Salir
    #
    # >> Seleccione una opción: 
    #
    #TODO: Para la opción 3, modificar un contacto, deberás desarrollar las funciones necesarias para actualizar la información de un contacto.
    #TODO: También deberás desarrollar la opción 6 que deberá preguntar por el criterio de búsqueda (nombre, apellido, email o telefono) y el valor a buscar para mostrar los contactos que encuentre en la agenda.
    agenda(contactos, contactos_ordenados, emails)

if __name__ == "__main__":
    main()
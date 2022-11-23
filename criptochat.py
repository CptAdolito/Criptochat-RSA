
from venv import create
import rsa
import re
import sys
import os
import signal

def signal_handler(signal, frame):
    print('\nSaliendo...\n\n')
    sys.exit(0)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def colored_text(text, r,g,b):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"
def get_entrada(valid_range = None):
    entrada = input("Seleccione una opcion (EXIT para salir): ")
    ok = False
    while not ok:
        entrada = entrada.strip()
        entrada = entrada.upper()
        if entrada == "EXIT":
            ok = True
            exit()
        else:  
            try:
                entrada = int(entrada)
                if valid_range is not None:
                    if entrada in valid_range:
                        ok = True
                        return entrada
                    else:
                        sys.stdout.write("\033[F")
                        entrada = input("Opción no existente. Seleccione una opcion (EXIT para salir): ")
            except:
                sys.stdout.write("\033[F")
                entrada = input("Entrada no válida. Seleccione una opcion (EXIT para salir): ")

def obtener_mi_clave(user_key):
    #Obtengo mi clave privada
    print(f"Su clave privada es: {user_key[2]}")
    print(f"Su nueva clave pública es:\n{user_key[1]} {user_key[0]}")
    input()

def create_contact():
    clear()
    print("Introduzca el nombre del contacto: ")
    nombre = input()
    nombre = re.sub(r'[^a-zA-Z0-9]', '', nombre)
    print("Introduzca la clave pública del contacto: ")
    clave_publica = input()
    clave_publica = re.findall(r'\d+', clave_publica)
    #Agrego el nombre y la clave al archivo de contactos
    with open("contactos.txt", "a") as f:
        f.write(nombre + " " + clave_publica[0] + " " + clave_publica[1] + "\n")
    print(f"Contacto creado con éxito: {nombre} {clave_publica[0]} {clave_publica[1]}")
    return nombre, clave_publica

def create_new_account():
    clear()
    #Crea una nueva clave
    n, e, d = rsa.generar_claves(100, 1000)
    obtener_mi_clave([n, e, d])
    return n, e, d

def login():
    clear()
    ok = False
    print("Introduzca todas sus claves (en orden n e d): ")
    clave_privada = input()
    while not ok:
        clave_privada = re.findall(r'\d+', clave_privada)
        if len(clave_privada) == 3:
            ok = True
        else:
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[F")
            print("Entrada no válida. Introduzca todas sus claves (en orden n e d): ")
            clave_privada = input()

    return clave_privada[0], clave_privada[1], clave_privada[2]

def register_menu():
    clear()
    print("Bienvenido a CriptoChat")
    print("1. Iniciar sesión")
    print("2. Registrarse")
    print("3. Opciones")
    return get_entrada([1,2,3])

def main_menu():
    clear()
    print("Bienvenido a CriptoChat")
    print("Contactos disponibles:")
    #Imprimo los contactos disponibles leyendo el archivo de contactos
    with open("contactos.txt", "r") as f:
        i=0
        for line in f:
            i+=1
            print(f"{i}. {line.split()[0]}")
    print()
    print(f"{i+1}. Crear nuevo contacto")
    print(f"{i+2}. Opciones")
    print(f"{i+3}. Volver")
    return get_entrada([j for j in range(1, i+4)])

def options_menu():
    clear()
    print("Opciones")
    print("1. Cambiar padding")
    print("2. Ver mi clave actual")
    print("3. Volver")
    return get_entrada([1, 2])

def chat_menu(contacto, mensajes):
    clear()
    print(f"Chat con {contacto}")
    print("Mensajes:")
    for mensaje in mensajes:
        print(mensaje)
    print()
    print("1. Enviar mensaje")
    print("2. Leer mensaje")
    print("3. Volver")
    return get_entrada([1, 2, 3])

def main():
    #Set the signal handler
    signal.signal(signal.SIGINT, signal_handler)
    #Inicializo las variables
    user_key = list()
    current_contact = str()
    current_contact_key = list()
    current_contact_messages = list()
    padding = 0
    #Creo el archivo de contactos si no existe
    if not os.path.exists("contactos.txt"):
        with open("contactos.txt", "w") as f:
            pass
    
    #Comienzo el programa
    while True:
        #Si no hay usuario logueado, se muestra el menú de registro
        if len(user_key) == 0:
            opcion = register_menu()
            if opcion == 1: #Iniciar sesión
                user_key = login()
            elif opcion == 2: #Registrarse
                user_key = create_new_account()
            elif opcion == 3: #Opciones
                opcion = options_menu()
                if opcion == 1:
                    print("Introduzca el nuevo padding: ")
                    padding = get_entrada([i for i in range(0, 32)])
                elif opcion == 2:
                    obtener_mi_clave(user_key)
            user_key = [int(i) for i in user_key]
        #Si hay usuario logueado, se muestra el menú principal
        else:
            opcion = main_menu()
            #Si se selecciona una opción de los contactos
            #La longitud del archivo de contactos es igual a la cantidad de contactos
            numero_de_contactos = len(open("contactos.txt").readlines())
            if opcion <= numero_de_contactos: #Si se selecciona un contacto
                #Guardo el contacto seleccionado
                current_contact = open("contactos.txt").readlines()[opcion-1].split()[0]
                #Guardo la clave pública del contacto seleccionado
                current_contact_key = open("contactos.txt").readlines()[opcion-1].split()[1:]
                current_contact_key = [int(i) for i in current_contact_key]
                #Mientras no se seleccione volver, se muestra el menú de chat
                while True:
                    opcion = chat_menu(current_contact, current_contact_messages)
                    if opcion == 1:
                        print("Introduzca el mensaje: ")
                        mensaje = input().strip()
                        #Elimino la linea de entrada
                        sys.stdout.write("\033[F")
                        mensaje_cifrado = rsa.cifrar_cadena_rsa(mensaje, current_contact_key[0], current_contact_key[1], padding)
                        current_contact_messages.append(f"Tu: {mensaje}")
                        print(f"Tu: {mensaje}")
                        #Imprimo el mensaje cifrado de un color diferente
                        current_contact_messages.append(colored_text(f"    {str(mensaje_cifrado)[1:-1]}", 0,0,0))
                        print(colored_text(f"    {str(mensaje_cifrado)[1:-1]}", 0,0,0))
                    elif opcion == 2:
                        print("Introduzca el mensaje: ")
                        mensaje = input()
                        #Elimino la linea de entrada
                        sys.stdout.write("\033[F")
                        mensaje_cifrado = re.findall(r'\d+', mensaje)
                        mensaje_cifrado = [int(i) for i in mensaje_cifrado]
                        mensaje = rsa.descifrar_cadena_rsa(mensaje_cifrado, user_key[2], user_key[0], padding)
                        current_contact_messages.append(f"{current_contact}: {mensaje}")
                        print(f"{current_contact}: {mensaje}")
                        #Imprimo el mensaje cifrado de un color diferente
                        current_contact_messages.append(colored_text(" "*len(current_contact)+f"  {str(mensaje_cifrado)[1:-1]}", 0,0,0))
                        print(colored_text(" "*len(current_contact)+f"  {str(mensaje_cifrado)[1:-1]}", 0,0,0))
                    elif opcion == 3:
                        break
            
            #Si se selecciona la opción de crear nuevo contacto
            elif opcion == numero_de_contactos+1:
                create_contact()
            #Si se selecciona opciones
            elif opcion == numero_de_contactos+2:
                opcion = options_menu()
                if opcion == 1:
                    print("Introduzca el nuevo padding: ")
                    padding = get_entrada([i for i in range(0, 32)])
                elif opcion == 2:
                    obtener_mi_clave(user_key)
            #Si se selecciona volver
            elif opcion == numero_de_contactos+3:
                user_key = list()
                current_contact = str()
                current_contact_key = list()
                current_contact_messages = list()

if __name__ == "__main__":
    main()
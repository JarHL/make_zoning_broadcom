# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 10:02:32 2024

@author: JaredHidalgo

Este script se utiliza para realizar la zonificación de redes de almacenamiento
a través de SSH. El usuario puede obtener información, configurar zonificación
y obtener informes de errores. 
"""

import paramiko

def ssh_command(host, port, username, password, command):
    """
    Ejecuta un comando SSH en un host remoto y devuelve el resultado.
    
    Parámetros:
    - host: dirección IP o nombre de dominio del host.
    - port: número de puerto para la conexión SSH.
    - username: nombre de usuario para autenticación.
    - password: contraseña para autenticación.
    - command: comando que se va a ejecutar en el host remoto.

    Retorna:
    - Salida del comando si no hay errores, de lo contrario devuelve un mensaje de error.
    """
    try:
        # Crear un cliente SSH
        client = paramiko.SSHClient()
        # Configurar para que acepte automáticamente las claves del servidor
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Conectarse al servidor
        client.connect(host, port, username, password)
        
        # Ejecutar el comando
        stdin, stdout, stderr = client.exec_command(command)
        
        # Obtener la salida del comando
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        # Cerrar la conexión
        client.close()
        
        if error:
            return f"Error: {error}"
        else:
            return output
    except Exception as e:
        return str(e)

def obtener_datos_host():
    """
    Solicita al usuario los datos del host y los almacena en un diccionario.
    """
    hostCfg["host"] = input("Introduce el host: ")
    hostCfg["port"] = int(input("Introduce el puerto: "))
    hostCfg["username"] = input("Introduce el username: ")
    hostCfg["password"] = input("Introduce la contraseña: ")

def mostrar_menu():
    """
    Muestra el menú de opciones disponibles y solicita al usuario que seleccione una opción.
    """
    print("Elige una opción:")
    print("1.- Obtener información")
    print("2.- Hacer zoning")
    print("3.- Obtener informe de errores")
    select = input("Seleccione una opción: ")
    return select

def obtener_configuraciones():
    """
    Obtiene las configuraciones actuales de la red utilizando el comando 'cfgshow'.
    """
    command = "cfgshow"
    print(f"Enviando comando: {command}")
    response = ssh_command(hostCfg["host"], hostCfg["port"], hostCfg["username"], hostCfg["password"], command)
    response = response.splitlines()
    palabras_encontradas = []
    for palabra in response:
        if "cfg:" in palabra:
            palabras_encontradas.append(palabra.replace(" cfg: ",""))
    palabras_encontradas = list(set(palabras_encontradas))
    cfgSave["configuraciones"] = palabras_encontradas
    print(" , ".join(cfgSave["configuraciones"]))

def zoning():
    """
    Proceso de creación de zonas mediante la configuración de alias.
    """
    print("=| Creación de zona |=")
    continuar = ""
    while continuar.lower() != "n":
        nameAlias = create_alias()
        if nameAlias:
            cfgSave["aliasGuardados"].append(nameAlias)
            continuar = input("¿Desea añadir otro alias? (y/n): ")
        else:
            print("Ha ocurrido un error, intente nuevamente.")
    create_zone()

def create_zone():
    """
    Crea una zona a partir de los alias guardados y activa la configuración de zona.
    """
    nameZone = input("Ingrese nombre de la zona: ")
    aliases = ';'.join(cfgSave["aliasGuardados"])
    command = f"zonecreate {nameZone}, \"{aliases}\""
    print(f"Enviando comando: {command}")
    response = ssh_command(hostCfg["host"], hostCfg["port"], hostCfg["username"], hostCfg["password"], command)
    if "Error:" in response:
        print(f"Error al crear la zona: {response}")
        return
    print(response)

    if len(cfgSave["configuraciones"]) <= 1:
        activar_zona(cfgSave["configuraciones"][0], nameZone)
    else:
        print("Selecciona una configuración:")
        for idx, cfg in enumerate(cfgSave["configuraciones"]):
            print(f"{idx}.- {cfg}")
        select = input("Elige una configuración: ")
        activar_zona(cfgSave["configuraciones"][int(select)], nameZone)
            
def activar_zona(actualCfg, nameZone):
    """
    Activa la configuración de zona en el dispositivo.

    Parámetros:
    - actualCfg: configuración actual.
    - nameZone: nombre de la zona que se va a activar.
    """
    command = f"cfgadd {actualCfg}, \"{nameZone}\""
    print(f"Enviando comando: {command}")
    response = ssh_command(hostCfg["host"], hostCfg["port"], hostCfg["username"], hostCfg["password"], command)
    print(response)

    command = f"cfgenable {actualCfg}"
    print(f"Enviando comando: {command}")
    response = ssh_command(hostCfg["host"], hostCfg["port"], hostCfg["username"], hostCfg["password"], command)
    print(response)

def create_alias():
    """
    Crea un alias de zona a partir del alias y WWPN proporcionados por el usuario.

    Retorna:
    - El alias si se creó con éxito, False en caso de error.
    """
    alias = input("Ingresa alias de zona: ")
    wwpn = input("Ingresa las WWPN: ")
    wwpn = corregir_wwpn(wwpn)
    command = f"alicreate {alias}, {wwpn}"
    print(f"Enviando comando: {command}")
    response = ssh_command(hostCfg["host"], hostCfg["port"], hostCfg["username"], hostCfg["password"], command)
    if "Error:" in response:
        print(f"Error al crear alias: {response}")
        return False
    return alias

def corregir_wwpn(cadenaWWPN):
    """
    Corrige el formato de las cadenas WWPN proporcionadas por el usuario.

    Parámetros:
    - cadenaWWPN: cadenas WWPN separadas por espacios.

    Retorna:
    - Cadenas WWPN corregidas y separadas por punto y coma.
    """
    arregloCadenas = cadenaWWPN.split()
    wwpnText = "\""
    for i, cadena in enumerate(arregloCadenas):
        nuevacadena = ""
        for j, char in enumerate(cadena):    
            if ((j+1) % 2 == 0) and (j < len(cadena) -1):
                nuevacadena += char + ":"
            else:
                nuevacadena += char
        wwpnText += nuevacadena
        if i < len(arregloCadenas) - 1:      
            wwpnText += ";"
        else:
            wwpnText += "\""
    return wwpnText          

def principal():
    """
    Función principal que inicia la ejecución del programa.
    """
    obtener_datos_host()
    print(hostCfg)
    select = mostrar_menu()
    obtener_configuraciones()
    # Ejecutar la función correspondiente a la opción seleccionada
    dictionaryOptions.get(select, lambda: print("Opción no válida"))()

cfgSave = {
    "aliasGuardados": [],
    "configuraciones": ""
}

hostCfg = {
    "host": "",
    "port": 22,
    "username": "",
    "password": ""
}

dictionaryOptions = {
    "1": obtener_configuraciones,
    "2": zoning,
    # "3": obtener_informe_errores  # Implementar si es necesario
}

simulate = """
Defined configuration:
 cfg: CONFIG1
     ZONA1
     ZONA2

Effective configuration:
 cfg: CONFIG1
     ZONA1
     ZONA2

zones:
 zone: ZONA1
     21:00:00:24:ff:47:35:12
     21:00:00:24:ff:47:35:13
"""

if __name__ == "__main__":
    principal()

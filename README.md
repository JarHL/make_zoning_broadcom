## README: Script de Zonificación de Redes de Almacenamiento a través de SSH

### Descripción

Este script de Python permite la gestión de la zonificación de redes de almacenamiento a través de una conexión SSH. El usuario puede:

- **Obtener información** de las configuraciones actuales.
- **Realizar la zonificación** creando zonas y añadiendo alias.
- **Obtener informes de errores** (opción en desarrollo).

El script está diseñado para interactuar con dispositivos de almacenamiento a través de comandos SSH, utilizando la librería `paramiko` para la conexión remota.

### Requisitos

- Python 3.x
- Librería `paramiko` instalada:

  ```bash
  pip install paramiko
  ```

### Funcionalidades Principales

1. **Obtener información**: Muestra las configuraciones actuales de la red de almacenamiento utilizando el comando `cfgshow`.
2. **Zonificación**: Permite crear alias y zonas, y activa la configuración en el dispositivo.
3. **Error Reporting**: (En desarrollo) Obtener un informe de errores relacionados con la zonificación.

### Uso

#### 1. Clona este repositorio:
```bash
git clone https://github.com/JarHL/make_zoning_broadcom.git
```

#### 2. Configura los datos de conexión:
El usuario debe introducir los detalles de conexión (host, puerto, usuario, contraseña) para conectarse al dispositivo a través de SSH.

#### 3. Ejecuta el script:
```bash
python zonificacion.py
```

#### 4. Interfaz de usuario:
El script presenta un menú interactivo en la consola:
- **Opción 1:** Obtener información de las configuraciones actuales (esta opcion esta siendo actualmente usada como un debug).
- **Opción 2:** Realizar zonificación mediante la creación de alias y zonas.
- **Opción 3:** Obtener informes de errores (próximamente).

### Ejemplo de uso

1. Ejecutar el script.
2. Ingresar los datos del host.
3. Seleccionar la opción deseada:
   - Para obtener configuraciones actuales, elige la opción 1.
   - Para crear alias y zonas, elige la opción 2.

### Estructura del Código

- **`ssh_command`**: Ejecuta comandos remotos a través de SSH.
- **`obtener_configuraciones`**: Muestra las configuraciones actuales del dispositivo.
- **`zoning`**: Permite la creación de alias y zonas para la zonificación.
- **`create_zone`**: Crea y activa una zona.
- **`create_alias`**: Crea un alias basado en el WWPN (World Wide Port Name).
- **`corregir_wwpn`**: Corrige el formato del WWPN para el comando de zonificación.
  
### Personalización

El script está preparado para ser ampliado, por ejemplo, implementando la opción de **informes de errores** o adaptando los comandos a otros entornos de almacenamiento que utilicen diferentes comandos.

### Contribuciones

Las contribuciones son bienvenidas. Si tienes sugerencias o mejoras, no dudes en abrir un issue o enviar un pull request.

### Licencia

Este proyecto está bajo la licencia MIT.

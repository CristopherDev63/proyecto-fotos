# Documentación Mural UPVM 

## Descripción General 
Nuestro proyecto se constituye en plasmar en una sola pagina nuestros compañeros, 
trabajos y lugares relacionados a la universidad politecnica del valle de mexico 

  ██╗   ██╗██████╗ ██╗   ██╗███╗   ███╗
  ██║   ██║██╔══██╗██║   ██║████╗ ████║
  ██║   ██║██████╔╝██║   ██║██╔████╔██║
  ██║   ██║██╔═══╝ ╚██╗ ██╔╝██║╚██╔╝██║
  ╚██████╔╝██║      ╚████╔╝ ██║ ╚═╝ ██║
   ╚═════╝ ╚═╝       ╚═══╝  ╚═╝     ╚═

---

## Propósito y funcionalidades principales 
El proposito del mural es mostrar a los usuarios la diversidad que existe dentro 
de la politecnica.

### funcionalidades
- Tiene un algoritmo de organización de fotografías automático basado en un algoritmo de **lista enlazada**.
- Tiene funcionalidades de categorización de imagenes.
- Contactos de personal para tomar fotografías.

---

## Tecnologías utilizadas

- **Flask**: Framework de python que permite crear un servidor web.
- **sqlite3**: Base de datos que permite almacenar información como las rutas de las imagenes.
- **css**: Permite estilizar el sitio web.
- **html**: Permite crear el sitio web.
- **python**: Lenguaje de programación utilizado para crear el servidor web.

---

## Requisitos e instalación 
Es muy importante tener en dependencias importantes para correr la pagina web con su respectivo front-end y back-end.

### Pasos de instalación 
1. Primero crea un enviroment virtual y activalo.
** Para unix (macOS/Linux)**: 
``` bash 
python3 -m venv env # Crear el entorno virtual.
source venv/vin/active # Activamos el entorno virtual.
```
** Para Windows **
```bash
python -m venv env # Crear el entorno virtual.
venv\Scripts\activate # Activamos el entorno virtual.
```

2. Instalamos los requerimientos de python.
``` bash 
pip install flask 
pip install sqlite3
pip install numpy
pip install typing
```

---

## Como ejecutar la aplicación
Para ejecutar la aplicación, simplemente ejecutamos el archivo app.py 
``` bash
python app.py
```
Y nosotros tendremos un servidor web en el puerto 8000.

---

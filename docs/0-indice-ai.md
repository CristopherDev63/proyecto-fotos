# Indice de documentación 

1. Documentación General (README.md) [[1-documentacion-original.md]]

  - Descripción del proyecto
  - Propósito y funcionalidades principales
  - Tecnologías utilizadas (Flask, SQLite, Python)
  - Requisitos e instalación
  - Cómo ejecutar la aplicación

  2. Arquitectura del Sistema [[]]

  - Diagrama de componentes
  - Flujo de datos entre módulos
  - Patrón de diseño utilizado (MVC-like)

  3. Componentes del Backend (en este orden):

     a. Base de Datos (db_images.py)
  - Clase ImageDatabase
  - Esquema de la tabla images
  - Métodos principales (CRUD)
  - Sistema de escaneo multi-directorio

     b. Estructura de Datos (image_linked_list.py)p
  - Clase ImageNode (nodo individual)
  - Clase ImageLinkedList (lista doblemente enlazada)
  - Clase ImageGalleryManager (administrador principal)
  - Navegación y gestión de imágenes

     c. Aplicación Flask (app.py)
  - Rutas principales (/, /about)
  - APIs REST (/api/mural/refresh, /api/images/scan)
  - Función generate_random_sizes()
  - Manejo de dispositivos móvil/PC

  4. Frontend
as 
  - Estructura de templates (templates/index.html)
  - Estilos CSS (static/css/)
  - Sistema de categorías de imágenes

  5. API Documentation

  - Endpoints disponibles
  - Parámetros y respuestas
  - Ejemplos de uso

  6. Ejemplos de Uso

  - Cómo agregar imágenes
  - Cómo navegar por la galería
  - Cómo refrescar el mural

# Arquitectura del sistema 

## componentes principales del sistema 

- **backend (Python/Flask)**: 
    - `app.py`: Entrada principal del servidor web como las rutas y el endpoint.
    - `db_images.py`: Gestiona la base de datos de las imagenes.
    - `image_linked_list.py`: Gestiona la estructura de datos de la galeria.

- **Estructuras de Datos**
  - ImageNode - Nodo de lista enlazada con configuraciones responsivas
  - ImageLinkedList - Lista enlazada doble para navegación
  - ImageGalleryManager - Administrador que integra BD y lista enlazada

  Frontend

  - templates/index.html - Template principal del mural
  - static/css/ - Estilos CSS
  - static/images/ - Directorio de imágenes

  Base de Datos

  - images.db - SQLite con tabla de imágenes (id, filename, filepath, created_at)

  Funcionalidades Principales

  - Escaneo automático de imágenes
  - Categorización por prefijos en nombres de archivo
  - Tamaños aleatorios responsivos (móvil/PC)
  - API REST para refrescar mural y escanear imágenes
  - Sistema de navegación por lista enlazado 

---

  ┌─────────────────────────────────────────────────────────────────────────┐
  │                         PROYECTO GALERÍA DE FOTOS                        │
  └─────────────────────────────────────────────────────────────────────────┘

                                ┌──────────────┐
                                │   Cliente    │
                                │ (Navegador)  │
                                └──────┬───────┘
                                       │ HTTP Request
                                       ▼a
  ┌────────────────────────────────────────────────────────────────────────┐
  │                          CAPA DE PRESENTACIÓN                          │
  ├────────────────────────────────────────────────────────────────────────┤
  │  ┌──────────────────┐           ┌─────────────────────────────┐       │
  │  │  templates/      │           │      static/                │       │
  │  │                  │           │                             │       │
  │  │  • index.html    │           │  • css/                     │       │
  │  │  • about.html    │           │  • images/                  │       │
  │  └──────────────────┘           └─────────────────────────────┘       │
  └────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
  ┌────────────────────────────────────────────────────────────────────────┐
  │                        CAPA DE APLICACIÓN (Flask)                      │
  ├────────────────────────────────────────────────────────────────────────┤
  │                          app.py (Puerto 5001)                          │
  │                                                                        │
  │  Rutas Web:                        API Endpoints:                     │
  │  • GET  /                          • GET  /api/mural/refresh          │
  │  • GET  /about                     • GET  /api/images/scan            │
  │                                                                        │
  │  Funciones Auxiliares:                                                │
  │  • generate_random_sizes(images, is_mobile)                           │
  │                                                                        │
  └────────┬────────────────────────────────────────────────┬─────────────┘
           │                                                │
           ▼                                                ▼
  ┌─────────────────────────────────┐    ┌──────────────────────────────────┐
  │    CAPA DE LÓGICA DE NEGOCIO    │    │    ESTRUCTURA DE DATOS           │
  │  (image_linked_list.py)         │    │                                  │
  ├─────────────────────────────────┤    ├──────────────────────────────────┤
  │  ImageGalleryManager            │◄───┤  ImageLinkedList                 │
  │  ├─ db: ImageDatabase           │    │  ├─ head: ImageNode              │
  │  ├─ image_list: ImageLinkedList │    │  ├─ tail: ImageNode              │
  │  ├─ max_images_per_dir: int     │    │  ├─ current: ImageNode           │
  │  │                              │    │  ├─ size: int                    │
  │  ├─ load_images()               │    │  │                               │
  │  ├─ reload_images()             │    │  ├─ add_image()                  │
  │  ├─ add_new_image()             │    │  ├─ remove_by_id()               │
  │  ├─ remove_image()              │    │  ├─ find_by_id()                 │
  │  ├─ navigate_next()             │    │  ├─ move_to_next()               │
  │  ├─ navigate_prev()             │    │  ├─ move_to_prev()               │
  │  ├─ scan_for_new_images()       │    │  ├─ get_all_images_info()        │
  │  └─ auto_refresh_images()       │    │  └─ load_from_database()         │
  │                                 │    │                                  │
  └────────┬────────────────────────┘    └──────────────┬───────────────────┘
           │                                            │
           │                             ┌──────────────┴───────────────────┐
           │                             │         ImageNode                │
           │                             │  ├─ image_id: int                │
           │                             │  ├─ filename: str                │
           │                             │  ├─ filepath: str                │
           │                             │  ├─ created_at: str              │
           │                             │  ├─ next: ImageNode              │
           │                             │  ├─ prev: ImageNode              │
           │                             │  ├─ size_config: dict            │
           │                             │  │   ├─ mobile {w,h,max_mb}      │
           │                             │  │   └─ pc {w,h,max_mb}          │
           │                             │  │                               │
           │                             │  ├─ get_size_for_device()        │
           │                             │  └─ update_size_config()         │
           │                             └──────────────────────────────────┘
           ▼
  ┌────────────────────────────────────────────────────────────────────────┐
  │                      CAPA DE ACCESO A DATOS                            │
  │                        (db_images.py)                                  │
  ├────────────────────────────────────────────────────────────────────────┤
  │  ImageDatabase                                                         │
  │  ├─ db_path: str = "images.db"                                         │
  │  │                                                                     │
  │  ├─ init_database()                                                    │
  │  ├─ add_image(filename, filepath)                                      │
  │  ├─ get_all_images()                                                   │
  │  ├─ get_image_by_filename(filename)                                    │
  │  ├─ delete_image(filename)                                             │
  │  ├─ scan_images_directory(directory_path)                              │
  │  ├─ scan_multiple_directories(base_path, max_images_per_dir)           │
  │  ├─ get_total_image_count()                                            │
  │  └─ clear_database()                                                   │
  │                                                                        │
  └────────┬───────────────────────────────────────────────────────────────┘
           │ SQLite3
           ▼
  ┌────────────────────────────────────────────────────────────────────────┐
  │                        CAPA DE PERSISTENCIA                            │
  ├────────────────────────────────────────────────────────────────────────┤
  │                         images.db (SQLite)                             │
  │                                                                        │
  │  Tabla: images                                                         │
  │  ┌────────────┬──────────────┬──────────────┬─────────────────────┐   │
  │  │ id (PK)    │ filename     │ filepath     │ created_at          │   │
  │  │ INTEGER    │ TEXT UNIQUE  │ TEXT UNIQUE  │ TIMESTAMP           │   │
  │  └────────────┴──────────────┴──────────────┴─────────────────────┘   │
  └────────────────────────────────────────────────────────────────────────┘


  ┌────────────────────────────────────────────────────────────────────────┐
  │                         FLUJO DE DATOS PRINCIPAL                       │
  └────────────────────────────────────────────────────────────────────────┘

    Usuario → Flask (/) → ImageGalleryManager.reload_images()
                                │
                                ├→ ImageLinkedList.load_from_database()
                                │         │
                                │         └→ ImageDatabase.get_all_images()
                                │                   │
                                │                   └→ SQLite Query
                                │
                                ├→ ImageLinkedList.get_all_images_info()
                                │
                                └→ generate_random_sizes()
                                          │
                                          └→ Render template con mural_images


    Usuario → API (/api/mural/refresh) → auto_refresh_images()
                                                │
                                                ├→ scan_for_new_images()
                                                │        │
                                                │        └→ scan_multiple_directories()
                                                │
                                                └→ reload_images()

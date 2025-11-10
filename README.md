# 🎓 Collage Universitario

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**Una aplicación web moderna para compartir y preservar los mejores momentos universitarios**

[Demo](#capturas-de-pantalla) • [Instalación](#instalación) • [Documentación](docs/) • [Características](#características)

</div>

---

## 📸 Descripción

**Collage Universitario** es una aplicación web diseñada específicamente para estudiantes que desean crear un espacio visual donde compartir fotografías de su experiencia universitaria. Con un diseño tipo collage que simula fotos pegadas en un tablón, esta herramienta convierte tus recuerdos en una galería interactiva y colorida.

## ✨ Características

- 🎨 **Diseño Tipo Collage**: Las fotos aparecen con rotaciones aleatorias simulando un tablón real
- 🌈 **Estilo Universitario Vibrante**: Gradientes coloridos y diseño juvenil moderno
- 📤 **Subida Fácil**: Sube imágenes con drag & drop o clic
- 🖼️ **Múltiples Formatos**: Soporta JPG, PNG, GIF y WebP
- 📱 **Totalmente Responsive**: Se adapta perfectamente a móviles, tablets y desktop
- ⚡ **Sin Base de Datos**: Simplicidad al máximo para facilitar el aprendizaje
- 🎓 **Educativo**: Código limpio y comentado, ideal para aprender Flask

## 📋 Requisitos

- Python 3.7 o superior
- Flask 3.0.0
- Navegador web moderno

## 🚀 Instalación

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/collage-universitario.git
cd collage-universitario
```

### Paso 2: Crear entorno virtual (recomendado)

```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En Mac/Linux:
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

## 🎯 Uso Rápido

### Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en: **http://localhost:5001**

### Subir imágenes

1. Haz clic en el botón flotante **"📷 Subir Imagen"**
2. Selecciona una foto o arrástrala a la zona indicada
3. Haz clic en **"🎓 Agregar al Collage"**
4. ¡Tu foto aparecerá instantáneamente!

## 📸 Capturas de Pantalla

> **Nota**: Agrega aquí capturas de tu aplicación en funcionamiento

### Vista Principal
![Collage Principal](docs/_static/screenshots/main.png)

### Subir Imagen
![Subir Imagen](docs/_static/screenshots/upload.png)

### Vista Móvil
![Vista Móvil](docs/_static/screenshots/mobile.png)

## 📁 Estructura del Proyecto

```
collage-universitario/
│
├── app.py                      # 🐍 Aplicación Flask principal
├── requirements.txt            # 📦 Dependencias del proyecto
├── README.md                   # 📖 Este archivo
│
├── templates/                  # 🎨 Plantillas HTML
│   ├── index.html             #    └─ Página principal del collage
│   ├── subir.html             #    └─ Formulario de subida
│   └── acerca.html            #    └─ Información del proyecto
│
├── static/                     # 🖼️ Archivos estáticos
│   └── images/                #    └─ Imágenes del collage
│
└── docs/                       # 📚 Documentación Sphinx
    ├── conf.py                #    └─ Configuración Sphinx
    ├── index.rst              #    └─ Página principal docs
    └── _build/                #    └─ Documentación generada
```

## 🎨 Cómo Funciona

### Backend (app.py)

El archivo principal contiene:

- **Clase `Galeria`**: Maneja la lógica de listado de imágenes
- **Rutas Flask**:
  - `GET /` - Muestra el collage principal
  - `GET /subir` - Formulario de subida
  - `POST /subir` - Procesa la imagen subida
  - `GET /acerca` - Información del proyecto

### Frontend (Templates)

- **index.html**: Collage principal con CSS Grid y efectos de rotación
- **subir.html**: Formulario con drag & drop y vista previa
- **acerca.html**: Documentación e información del proyecto

### Validación de Archivos

```python
EXTENSIONES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
```

## ⚙️ Personalización

### Cambiar el puerto

```python
# app.py, última línea
app.run(debug=True, port=5001)  # Cambia a tu puerto preferido
```

### Modificar carpeta de imágenes

```python
# app.py
galeria = Galeria('static/images')  # Cambia la ruta
```

### Ajustar tamaño máximo de archivos

```python
# app.py
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB
```

## 🔧 Solución de Problemas

### No aparecen las imágenes

- ✅ Verifica que estén en `static/images/`
- ✅ Confirma extensiones válidas: `.jpg`, `.png`, `.gif`, `.webp`
- ✅ Recarga la página (F5 o Ctrl+R)
- ✅ Revisa permisos de lectura de la carpeta

### Error al ejecutar

```bash
ModuleNotFoundError: No module named 'flask'
```
**Solución**: Instala Flask con `pip install -r requirements.txt`

### Puerto en uso

```bash
Address already in use
```
**Solución**: Cambia el puerto en `app.py` o mata el proceso:
```bash
# Linux/Mac
lsof -ti:5001 | xargs kill

# Windows
netstat -ano | findstr :5001
taskkill /PID <PID> /F
```

## 📚 Documentación Completa

Para documentación detallada, visita la [documentación Sphinx](docs/_build/html/index.html).

Para generar la documentación:

```bash
cd docs
sphinx-build -b html . _build/html
```

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Uso |
|------------|---------|-----|
| Python | 3.7+ | Lenguaje de programación |
| Flask | 3.0.0 | Framework web backend |
| Jinja2 | Incluido | Motor de plantillas |
| HTML5 | - | Estructura web |
| CSS3 | - | Estilos y animaciones |
| JavaScript | ES6+ | Interactividad (drag & drop) |
| Sphinx | 7.2+ | Generación de documentación |
| Shibuya | 2024.1+ | Tema de documentación |

## 🎓 Ideal Para

- 📚 Proyectos universitarios de programación
- 👥 Grupos de estudio y comunidades estudiantiles
- 🎉 Eventos, graduaciones y celebraciones
- 📖 Aprendizaje de Flask y desarrollo web
- 🏆 Portfolios de programación

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - mira el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**Estudiante de Programación**

- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- Proyecto: [Collage Universitario](https://github.com/tu-usuario/collage-universitario)

## 🌟 Agradecimientos

- Inspirado en la comunidad universitaria
- Desarrollado con fines educativos
- Diseñado para aprender Flask de forma práctica

---

<div align="center">

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub ⭐**

Hecho con ❤️ para estudiantes universitarios

</div>

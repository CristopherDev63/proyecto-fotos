from flask import Flask, render_template, jsonify, request
import db_images
from image_linked_list import ImageGalleryManager
import os
import random

app = Flask(__name__)

# Inicializar el administrador de galería
gallery = ImageGalleryManager()

def generate_random_sizes(images, is_mobile=False):
    """Genera tamaños aleatorios para las imágenes dentro de límites min/max"""
    sized_images = []

    # Definir categorías disponibles
    categorias = [
        'lugares', 'carreras', 'areas-trabajo', 'pasatiempos', 'deportes',
        'tics', 'enfermeria', 'ing-alimentos', 'ing-administracion',
        'ing-mecatronica', 'ing-logistica', 'ing-nanotec'
    ]

    # Definir límites según dispositivo
    if is_mobile:
        min_width, max_width = 150, 300
        min_height, max_height = 150, 300
    else:
        min_width, max_width = 200, 500
        min_height, max_height = 200, 500

    for image in images:
        # Generar tamaño aleatorio
        width = random.randint(min_width, max_width)
        height = random.randint(min_height, max_height)

        # Arreglar la ruta para que funcione en Flask (normalizar)
        clean_filepath = image['filepath'].replace('static/', '').replace('images /', 'images/').replace('\\', '/')

        # Manejar múltiples directorios (images1, images2, etc.)
        if 'images' in clean_filepath and not clean_filepath.startswith('images/'):
            # Normalizar rutas de directorios numerados
            clean_filepath = clean_filepath.replace('\\', '/')

        # Extraer categoría del nombre del archivo
        filename = image['filename'].lower()
        categoria = 'sin-categoria'  # Categoría por defecto

        # Buscar prefijo de categoría en el nombre del archivo
        for cat in categorias:
            if filename.startswith(cat + '-') or filename.startswith(cat + '_'):
                categoria = cat
                break

        sized_image = {
            'id': image['id'],
            'filename': image['filename'],
            'filepath': clean_filepath,  # Ruta limpia para usar con url_for
            'created_at': image['created_at'],
            'width': width,
            'height': height,
            'categoria': categoria
        }
        sized_images.append(sized_image)

    return sized_images

@app.route('/')
def index():
    # Escanear automáticamente por nuevas imágenes antes de mostrar el mural
    gallery.auto_refresh_images()

    # Forzar recarga completa de imágenes desde la base de datos
    gallery.reload_images()

    # Obtener todas las imágenes para el mural
    all_images = gallery.image_list.get_all_images_info()

    # Detectar si es móvil basado en user agent
    user_agent = request.headers.get('User-Agent', '').lower()
    is_mobile = any(mobile in user_agent for mobile in ['mobile', 'android', 'iphone'])

    # Generar tamaños aleatorios para el mural
    mural_images = generate_random_sizes(all_images, is_mobile)

    device_type = 'mobile' if is_mobile else 'pc'
    total_images = len(all_images)

    return render_template('index.html',
                         mural_images=mural_images,
                         total_images=total_images,
                         device_type=device_type)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/mural/refresh')
def refresh_mural():
    """API para refrescar el mural con nuevos tamaños aleatorios"""
    # Primero escanear por nuevas imágenes
    refresh_result = gallery.auto_refresh_images()

    # Forzar recarga completa de imágenes desde la base de datos
    gallery.reload_images()

    all_images = gallery.image_list.get_all_images_info()
    user_agent = request.headers.get('User-Agent', '').lower()
    is_mobile = any(mobile in user_agent for mobile in ['mobile', 'android', 'iphone'])

    mural_images = generate_random_sizes(all_images, is_mobile)

    return jsonify({
        'success': True,
        'images': mural_images,
        'total': len(all_images),
        'new_images_added': refresh_result['new_images_added']
    })

@app.route('/api/images/scan')
def scan_new_images():
    """API para escanear manualmente nuevas imágenes"""
    refresh_result = gallery.auto_refresh_images()

    return jsonify({
        'success': True,
        'new_images_added': refresh_result['new_images_added'],
        'total_images': refresh_result['total_images'],
        'has_images': refresh_result['has_images']
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)

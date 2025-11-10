# conf.py

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# -- Información del Proyecto ---
project = 'Collage Universitario'
copyright = '2025, Tu Nombre'
author = 'Tu Nombre'

# -- Configuración General ---
extensions = [
    'sphinx.ext.autodoc',   # Importa la documentación desde los docstrings.
    'sphinx.ext.viewcode',  # Agrega enlaces al código fuente.
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
language = 'es'

# -- Opciones para la Salida HTML ---
html_theme = 'alabaster'  # Un tema básico y limpio.
html_static_path = ['_static']


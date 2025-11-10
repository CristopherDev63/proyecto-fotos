📖 Guía de Usuario
==================

Esta guía te ayudará a usar todas las funcionalidades de Collage Universitario.

🎯 Navegando por el Collage
----------------------------

Vista Principal
~~~~~~~~~~~~~~~

Al abrir la aplicación verás:

- **Header con título**: Muestra "Collage Universitario" y el total de fotos
- **Banner informativo**: Te da la bienvenida al collage
- **Galería de fotos**: Las imágenes aparecen en una cuadrícula con rotaciones aleatorias
- **Botón flotante**: "📷 Subir Imagen" en la esquina inferior derecha

Interacción con las Fotos
~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Hover**: Al pasar el mouse sobre una foto, esta se eleva y rota a 0°
- **Nombre**: Cada foto muestra su nombre de archivo debajo
- **Efecto collage**: Las fotos tienen rotaciones de -2°, 1° y -1° aleatoriamente

📤 Subiendo Imágenes
--------------------

Método 1: Clic para Seleccionar
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Haz clic en el botón **"📷 Subir Imagen"**
2. Se abrirá la página de subida
3. Haz clic en la zona de carga
4. Selecciona una imagen de tu computadora
5. Verás una vista previa de la imagen
6. Haz clic en **"🎓 Agregar al Collage"**
7. Serás redirigido al collage principal con tu nueva foto

Método 2: Drag & Drop
~~~~~~~~~~~~~~~~~~~~~~

1. Ve a la página de subida
2. Arrastra una imagen desde tu explorador de archivos
3. Suéltala en la zona de carga (se resaltará en rosa)
4. Verás la vista previa
5. Haz clic en **"🎓 Agregar al Collage"**

Formatos Aceptados
~~~~~~~~~~~~~~~~~~

- ✅ JPG / JPEG
- ✅ PNG
- ✅ GIF
- ✅ WebP

Tamaño máximo: **16 MB** por archivo

🎨 Vista en Diferentes Dispositivos
------------------------------------

Desktop (PC)
~~~~~~~~~~~~

- Cuadrícula de 3-4 columnas
- Fotos de 220px de alto
- Efectos de hover completos
- Botón flotante en esquina inferior derecha

Tablet
~~~~~~

- Cuadrícula de 2-3 columnas
- Fotos de 200px de alto
- Efectos táctiles

Móvil
~~~~~

- Cuadrícula de 2 columnas (mínimo 150px)
- Fotos de 150px de alto
- Botón flotante más pequeño
- Interfaz optimizada para touch

🔍 Navegación del Sitio
------------------------

El sitio cuenta con 3 páginas principales:

Página Principal (/)
~~~~~~~~~~~~~~~~~~~~

El collage con todas las fotos subidas.

Página de Subida (/subir)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Formulario para agregar nuevas imágenes.

Página Acerca de (/acerca)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Información sobre el proyecto, características y tecnologías usadas.

💡 Consejos de Uso
------------------

Para Mejores Resultados
~~~~~~~~~~~~~~~~~~~~~~~

- Usa fotos de buena calidad (mínimo 800x600px)
- Evita imágenes muy grandes (>5MB) para mejor rendimiento
- Usa nombres descriptivos para tus archivos
- Las fotos horizontales se ven mejor en el collage

Organización
~~~~~~~~~~~~

- Nombra tus fotos con categorías: ``evento-graduacion-2024.jpg``
- Usa fechas en los nombres: ``2024-03-15-clase.jpg``
- Evita caracteres especiales en los nombres

❓ Preguntas Frecuentes
-----------------------

¿Puedo eliminar una foto?
~~~~~~~~~~~~~~~~~~~~~~~~~~

Actualmente no hay función de eliminación desde la web. Puedes eliminar
archivos directamente de la carpeta ``static/images/`` y recargar la página.

¿Las fotos se guardan en una base de datos?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No, las fotos se guardan como archivos en la carpeta ``static/images/``.
Esto hace el proyecto más simple y fácil de entender.

¿Cuántas fotos puedo subir?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No hay límite técnico, pero considera el espacio en disco disponible.
Cada foto puede pesar hasta 16MB.

¿Puedo cambiar los colores del tema?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sí, puedes editar los archivos HTML en la carpeta ``templates/`` para
personalizar colores y estilos.

🚨 Mensajes del Sistema
-----------------------

Mensajes de Éxito
~~~~~~~~~~~~~~~~~

.. code-block:: text

   Imagen "foto.jpg" subida exitosamente!

Aparece en verde cuando la imagen se sube correctamente.

Mensajes de Error
~~~~~~~~~~~~~~~~~

.. code-block:: text

   Tipo de archivo no permitido. Solo se permiten: PNG, JPG, JPEG, GIF, WEBP

Aparece en rojo cuando:

- El formato no es válido
- No se seleccionó ningún archivo
- El archivo es demasiado grande

🔄 Actualizando el Collage
---------------------------

El collage se actualiza automáticamente al:

- Subir una nueva imagen
- Recargar la página (F5 o Ctrl+R)
- Navegar desde otra página del sitio

No necesitas hacer nada especial para ver las nuevas fotos.

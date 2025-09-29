import sqlite3
import os
from typing import List, Optional

class ImageDatabase:
    def __init__(self, db_path: str = "images.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Inicializa la base de datos y crea la tabla de imágenes si no existe"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS images (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT UNIQUE NOT NULL,
                    filepath TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def add_image(self, filename: str, filepath: str) -> bool:
        """Añade una imagen a la base de datos"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO images (filename, filepath) VALUES (?, ?)",
                    (filename, filepath)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False

    def get_all_images(self) -> List[tuple]:
        """Obtiene todas las imágenes de la base de datos"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, filename, filepath, created_at FROM images")
            return cursor.fetchall()

    def get_image_by_filename(self, filename: str) -> Optional[tuple]:
        """Obtiene una imagen específica por nombre de archivo"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, filename, filepath, created_at FROM images WHERE filename = ?",
                (filename,)
            )
            return cursor.fetchone()

    def delete_image(self, filename: str) -> bool:
        """Elimina una imagen de la base de datos"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM images WHERE filename = ?", (filename,))
            conn.commit()
            return cursor.rowcount > 0

    def scan_multiple_directories(self, base_path: str = "static/images", max_images_per_dir: int = 30) -> int:
        """Escanea múltiples directorios de imágenes y maneja la organización automática"""
        added_count = 0

        # Primero, escanear todos los directorios existentes
        if os.path.exists(base_path):
            added_count += self._scan_single_directory(base_path)

        # Buscar directorios numerados (images1, images2, etc.)
        dir_counter = 1
        while True:
            numbered_dir = f"{base_path}{dir_counter}"
            if os.path.exists(numbered_dir):
                added_count += self._scan_single_directory(numbered_dir)
                dir_counter += 1
            else:
                break

        # Verificar si necesitamos crear un nuevo directorio
        self._manage_directory_creation(base_path, max_images_per_dir)

        return added_count

    def _manage_directory_creation(self, base_path: str, max_images_per_dir: int):
        """Gestiona la creación automática de directorios cuando se alcanza el límite"""
        total_images = self.get_total_image_count()

        # Calcular cuántos directorios completos deberíamos tener
        expected_dirs = (total_images - 1) // max_images_per_dir

        # Verificar directorios existentes
        existing_dirs = 0
        if os.path.exists(base_path):
            existing_dirs = 1

        dir_counter = 1
        while os.path.exists(f"{base_path}{dir_counter}"):
            existing_dirs += 1
            dir_counter += 1

        # Crear directorios faltantes
        while existing_dirs <= expected_dirs:
            new_dir = f"{base_path}{existing_dirs}" if existing_dirs > 0 else f"{base_path}1"
            os.makedirs(new_dir, exist_ok=True)
            print(f"Directorio creado automáticamente: {new_dir}")
            existing_dirs += 1

    def _scan_single_directory(self, directory_path: str) -> int:
        """Escanea un solo directorio de imágenes"""
        if not os.path.exists(directory_path):
            return 0

        added_count = 0
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}

        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)

            if os.path.isfile(file_path):
                _, ext = os.path.splitext(filename.lower())
                if ext in image_extensions:
                    if self.add_image(filename, file_path):
                        added_count += 1
                        print(f"Imagen añadida: {filename} desde {directory_path}")
                    else:
                        print(f"Imagen ya existe en BD: {filename}")

        return added_count

    def get_total_image_count(self) -> int:
        """Obtiene el total de imágenes en la base de datos"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM images")
            return cursor.fetchone()[0]

    def scan_images_directory(self, directory_path: str = "static/images/") -> int:
        """Mantiene compatibilidad con el método original, pero usa el nuevo sistema"""
        return self.scan_multiple_directories("static/images")

    def clear_database(self) -> bool:
        """Limpia todas las entradas de la base de datos"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM images")
            conn.commit()
            return True


def main():
    """Función principal para pruebas"""
    db = ImageDatabase()

    print("Escaneando directorio de imágenes...")
    added = db.scan_images_directory()
    print(f"Se añadieron {added} imágenes nuevas a la base de datos")

    print("\nImágenes en la base de datos:")
    images = db.get_all_images()
    for img in images:
        print(f"ID: {img[0]}, Archivo: {img[1]}, Ruta: {img[2]}, Creado: {img[3]}")


if __name__ == "__main__":
    main()

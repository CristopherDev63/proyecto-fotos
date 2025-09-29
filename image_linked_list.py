from typing import Optional, Dict, Tuple
from db_images import ImageDatabase

class ImageNode:
    """Nodo de la lista enlazada que contiene información de imagen con tamaños para móvil y PC"""

    def __init__(self, image_id: int, filename: str, filepath: str, created_at: str):
        self.image_id = image_id
        self.filename = filename
        self.filepath = filepath
        self.created_at = created_at

        # Configuraciones de tamaño para diferentes dispositivos
        self.size_config = {
            'mobile': {
                'width': 300,
                'height': 400,
                'max_size_mb': 2.0
            },
            'pc': {
                'width': 800,
                'height': 600,
                'max_size_mb': 5.0
            }
        }

        self.next: Optional['ImageNode'] = None
        self.prev: Optional['ImageNode'] = None

    def get_size_for_device(self, device_type: str) -> Dict[str, any]:
        """Obtiene la configuración de tamaño para el tipo de dispositivo especificado"""
        if device_type in self.size_config:
            return self.size_config[device_type]
        return self.size_config['pc']  # Por defecto PC

    def update_size_config(self, device_type: str, width: int, height: int, max_size_mb: float):
        """Actualiza la configuración de tamaño para un dispositivo específico"""
        if device_type not in self.size_config:
            self.size_config[device_type] = {}

        self.size_config[device_type].update({
            'width': width,
            'height': height,
            'max_size_mb': max_size_mb
        })

    def __str__(self):
        return f"ImageNode(id={self.image_id}, filename={self.filename})"


class ImageLinkedList:
    """Lista enlazada doble para manejar imágenes con configuraciones de tamaño responsivo"""

    def __init__(self):
        self.head: Optional[ImageNode] = None
        self.tail: Optional[ImageNode] = None
        self.size = 0
        self.current: Optional[ImageNode] = None  # Para navegación

    def is_empty(self) -> bool:
        """Verifica si la lista está vacía"""
        return self.head is None

    def add_image(self, image_id: int, filename: str, filepath: str, created_at: str) -> ImageNode:
        """Añade una nueva imagen al final de la lista"""
        new_node = ImageNode(image_id, filename, filepath, created_at)

        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1
        return new_node

    def remove_by_id(self, image_id: int) -> bool:
        """Elimina un nodo por ID de imagen y mantiene la funcionalidad de navegación"""
        node_to_remove = self.find_by_id(image_id)

        if node_to_remove is None:
            return False

        # Manejar el nodo actual antes de la eliminación
        if self.current == node_to_remove:
            # Si el nodo actual se va a eliminar, mover a anterior o siguiente
            if node_to_remove.prev:
                self.current = node_to_remove.prev
            elif node_to_remove.next:
                self.current = node_to_remove.next
            else:
                self.current = None

        # Actualizar enlaces
        if node_to_remove.prev:
            node_to_remove.prev.next = node_to_remove.next
        else:
            # Es el primer nodo
            self.head = node_to_remove.next

        if node_to_remove.next:
            node_to_remove.next.prev = node_to_remove.prev
        else:
            # Es el último nodo
            self.tail = node_to_remove.prev

        self.size -= 1
        return True

    def find_by_id(self, image_id: int) -> Optional[ImageNode]:
        """Busca un nodo por ID de imagen"""
        current = self.head
        while current:
            if current.image_id == image_id:
                return current
            current = current.next
        return None

    def find_by_filename(self, filename: str) -> Optional[ImageNode]:
        """Busca un nodo por nombre de archivo"""
        current = self.head
        while current:
            if current.filename == filename:
                return current
            current = current.next
        return None

    def move_to_next(self) -> Optional[ImageNode]:
        """Navega al siguiente nodo en la lista"""
        if self.current and self.current.next:
            self.current = self.current.next
        return self.current

    def move_to_prev(self) -> Optional[ImageNode]:
        """Navega al nodo anterior en la lista"""
        if self.current and self.current.prev:
            self.current = self.current.prev
        return self.current

    def move_to_first(self) -> Optional[ImageNode]:
        """Navega al primer nodo de la lista"""
        self.current = self.head
        return self.current

    def move_to_last(self) -> Optional[ImageNode]:
        """Navega al último nodo de la lista"""
        self.current = self.tail
        return self.current

    def get_current(self) -> Optional[ImageNode]:
        """Obtiene el nodo actual"""
        return self.current

    def get_current_image_for_device(self, device_type: str) -> Optional[Dict]:
        """Obtiene la información de la imagen actual optimizada para el dispositivo"""
        if self.current:
            size_config = self.current.get_size_for_device(device_type)
            return {
                'id': self.current.image_id,
                'filename': self.current.filename,
                'filepath': self.current.filepath,
                'created_at': self.current.created_at,
                'size_config': size_config
            }
        return None

    def get_all_images_info(self) -> list:
        """Obtiene información de todas las imágenes en la lista"""
        images = []
        current = self.head
        while current:
            images.append({
                'id': current.image_id,
                'filename': current.filename,
                'filepath': current.filepath,
                'created_at': current.created_at,
                'size_config': current.size_config
            })
            current = current.next
        return images

    def load_from_database(self, db: ImageDatabase):
        """Carga todas las imágenes desde la base de datos a la lista enlazada"""
        images = db.get_all_images()
        for image in images:
            self.add_image(image[0], image[1], image[2], image[3])

    def update_device_sizes(self, device_configs: Dict[str, Dict]):
        """Actualiza las configuraciones de tamaño para todos los nodos"""
        current = self.head
        while current:
            for device_type, config in device_configs.items():
                current.update_size_config(
                    device_type,
                    config.get('width', 800),
                    config.get('height', 600),
                    config.get('max_size_mb', 5.0)
                )
            current = current.next

    def __len__(self):
        return self.size

    def __str__(self):
        if self.is_empty():
            return "Lista enlazada vacía"

        images = []
        current = self.head
        while current:
            marker = " <- ACTUAL" if current == self.current else ""
            images.append(f"{current}{marker}")
            current = current.next

        return " <-> ".join(images)


class ImageGalleryManager:
    """Administrador principal que combina la base de datos con la lista enlazada"""

    def __init__(self, db_path: str = "images.db", max_images_per_dir: int = 30):
        self.db = ImageDatabase(db_path)
        self.image_list = ImageLinkedList()
        self.max_images_per_dir = max_images_per_dir
        self.load_images()

    def load_images(self):
        """Carga las imágenes de la base de datos a la lista enlazada"""
        self.image_list.load_from_database(self.db)

    def reload_images(self):
        """Recarga las imágenes desde la base de datos"""
        self.image_list = ImageLinkedList()
        self.load_images()

    def add_new_image(self, filename: str, filepath: str) -> bool:
        """Añade una nueva imagen tanto a la BD como a la lista enlazada"""
        if self.db.add_image(filename, filepath):
            # Obtener la imagen recién añadida para obtener su ID
            image_data = self.db.get_image_by_filename(filename)
            if image_data:
                self.image_list.add_image(image_data[0], image_data[1], image_data[2], image_data[3])
                return True
        return False

    def remove_image(self, image_id: int) -> bool:
        """Elimina una imagen tanto de la BD como de la lista enlazada"""
        # Primero obtener la información de la imagen
        node = self.image_list.find_by_id(image_id)
        if node:
            # Eliminar de la lista enlazada
            if self.image_list.remove_by_id(image_id):
                # Eliminar de la base de datos
                return self.db.delete_image(node.filename)
        return False

    def navigate_next(self) -> Optional[Dict]:
        """Navega a la siguiente imagen"""
        next_node = self.image_list.move_to_next()
        return self.get_current_image_info()

    def navigate_prev(self) -> Optional[Dict]:
        """Navega a la imagen anterior"""
        prev_node = self.image_list.move_to_prev()
        return self.get_current_image_info()

    def get_current_image_info(self, device_type: str = 'pc') -> Optional[Dict]:
        """Obtiene la información de la imagen actual"""
        return self.image_list.get_current_image_for_device(device_type)

    def get_gallery_stats(self) -> Dict:
        """Obtiene estadísticas de la galería"""
        return {
            'total_images': len(self.image_list),
            'current_position': self._get_current_position(),
            'has_images': not self.image_list.is_empty()
        }

    def _get_current_position(self) -> int:
        """Obtiene la posición actual en la lista (1-indexed)"""
        if self.image_list.current is None:
            return 0

        position = 1
        current = self.image_list.head
        while current and current != self.image_list.current:
            position += 1
            current = current.next

        return position

    def configure_device_sizes(self, device_configs: Dict[str, Dict]):
        """Configura los tamaños para diferentes dispositivos"""
        self.image_list.update_device_sizes(device_configs)

    def scan_for_new_images(self) -> int:
        """Escanea el directorio de imágenes y añade nuevas imágenes automáticamente"""
        return self.db.scan_images_directory()

    def auto_refresh_images(self) -> Dict:
        """Refresca automáticamente la galería con nuevas imágenes"""
        # Escanear nuevas imágenes
        new_images_count = self.scan_for_new_images()

        if new_images_count > 0:
            # Recargar la lista enlazada con las nuevas imágenes
            self.reload_images()

        return {
            'new_images_added': new_images_count,
            'total_images': len(self.image_list),
            'has_images': not self.image_list.is_empty()
        }


def main():
    """Función de prueba del sistema"""
    print("=== Inicializando ImageGalleryManager ===")
    gallery = ImageGalleryManager()

    print(f"\nEstadísticas: {gallery.get_gallery_stats()}")
    print(f"Lista actual: {gallery.image_list}")

    # Configurar tamaños personalizados
    device_configs = {
        'mobile': {'width': 250, 'height': 350, 'max_size_mb': 1.5},
        'tablet': {'width': 500, 'height': 400, 'max_size_mb': 3.0},
        'pc': {'width': 1000, 'height': 800, 'max_size_mb': 8.0}
    }
    gallery.configure_device_sizes(device_configs)

    print("\n=== Navegación por la galería ===")
    current = gallery.get_current_image_info('mobile')
    if current:
        print(f"Imagen actual (móvil): {current}")

    print("\n=== Navegando hacia adelante ===")
    for i in range(3):
        next_img = gallery.navigate_next()
        if next_img:
            print(f"Siguiente {i+1}: {next_img['filename']} - Tamaño PC: {next_img['size_config']}")

    print("\n=== Probando eliminación ===")
    if gallery.image_list.current:
        id_to_remove = gallery.image_list.current.image_id
        filename_to_remove = gallery.image_list.current.filename
        print(f"Eliminando imagen ID {id_to_remove}: {filename_to_remove}")

        if gallery.remove_image(id_to_remove):
            print("Imagen eliminada exitosamente")
            current_after_delete = gallery.get_current_image_info()
            if current_after_delete:
                print(f"Nueva imagen actual: {current_after_delete['filename']}")
        else:
            print("Error al eliminar imagen")

    print(f"\nEstadísticas finales: {gallery.get_gallery_stats()}")
    print(f"Lista final: {gallery.image_list}")


if __name__ == "__main__":
    main()

from model.Objects.Laptop import Laptop  # Importar la clase Laptop desde la carpeta Objects

class LaptopDAO:
    def __init__(self, database):
        """
        Constructor para la clase LaptopDAO.

        :param database: Objeto de conexión a la base de datos (o Firebase).
        """
        self._database = database
        self._collection = "laptops"  # Nombre de la colección/tabla de laptops en la base de datos
        
    def laptop_exists(self, laptop_id):
        """
        Verifica si ya existe una laptop con el ID dado.

        Args:
            laptop_id: El ID de la laptop a verificar.

        Returns:
            bool: True si la laptop existe, False en caso contrario.
        """
        try:
            doc_ref = self._database.collection(self._collection).document(laptop_id)
            doc = doc_ref.get()
            return doc.exists  # Devuelve True si el documento existe, False si no
        except Exception as e:
            print(f"Error al verificar la existencia de la laptop: {e}")
            return False  # En caso de error, asumimos que no existe (para evitar bloqueos)

    def add_laptop(self, laptop):
        """
        Agrega una nueva laptop a la base de datos.

        :param laptop: Objeto de tipo Laptop.
        :return: True si se agregó correctamente, False en caso contrario.
        """
        try:
            # Convertir el objeto Laptop a un diccionario
            laptop_data = laptop.to_dict()
            # Agregar la laptop a la colección "laptops"
            self._database.collection(self._collection).document(laptop.get_laptop_id()).set(laptop_data)
            return True
        except Exception as e:
            print(f"Error al agregar la laptop: {e}")
            return False

    def get_laptop_by_id(self, laptop_id):
        """
        Obtiene una laptop por su ID.

        :param laptop_id: Identificador único de la laptop.
        :return: Objeto de tipo Laptop si se encuentra, None en caso contrario.
        """
        try:
            # Buscar la laptop por su ID en la colección "laptops"
            doc_ref = self._database.collection(self._collection).document(laptop_id)
            doc = doc_ref.get()

            if doc.exists:
                return Laptop(**doc.to_dict())
            else:
                return None
        except Exception as e:
            print(f"Error al obtener la laptop: {e}")
            return None

    def update_laptop(self, laptop):
        """
        Actualiza una laptop en la base de datos.

        :param laptop: Objeto de tipo Laptop con los datos actualizados.
        :return: True si se actualizó correctamente, False en caso contrario.
        """
        try:
            doc_ref = self._database.collection(self._collection).document(laptop.get_book_id())
            doc_ref.update(laptop.to_dict())
            return True
        except Exception as e:
            print(f"Error al actualizar el libro: {e}")
            return False

    def delete_laptop(self, laptop_id):
        """
        Elimina una laptop de la base de datos.

        :param laptop_id: Identificador único de la laptop.
        :return: True si se eliminó correctamente, False en caso contrario.
        """
        try:
            doc_ref = self._database.collection(self._collection).document(laptop_id)
            doc_ref.delete()
            return True
        except Exception as e:
            print(f"Error al eliminar el libro: {e}")
            return False

    def get_all_laptops(self):
        """
        Obtiene todas las laptops de la base de datos.

        :return: Lista de objetos de tipo Laptop.
        """
        try:
            books_list = []
            docs = self._database.collection(self._collection).stream()

            for doc in docs:
                books_list.append(Laptop(**doc.to_dict()))
            return books_list
        except Exception as e:
            print(f"Error al obtener todos los libros: {e}")
            return []

    def get_available_laptops(self):
        """
        Obtiene todas las laptops disponibles.

        :return: Lista de objetos de tipo Laptop.
        """
        try:
            laptops_list = []
            # Obtener todas las laptops de la colección "laptops"
            laptops = self._database.child(self._collection).get()
            if laptops:
                for key, value in laptops.items():
                    if value["status"] == "available":
                        laptop = Laptop(
                            laptop_id=value["laptop_id"],
                            brand=value["brand"],
                            model=value["model"],
                            status=value["status"]
                        )
                        laptops_list.append(laptop)
            return laptops_list
        except Exception as e:
            print(f"Error al obtener las laptops disponibles: {e}")
            return []
    
    def update_laptop_status(self, loan_id, new_status):
        """Actualiza el estado de un préstamo."""
        try:
            doc_ref = self._database.collection(self._collection).document(loan_id)
            doc_ref.update({"status": new_status})
            return True
        except Exception as e:
            print(f"Error al actualizar el estado del préstamo: {e}")
            return False
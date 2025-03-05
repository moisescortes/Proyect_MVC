from model.Objects.Book import Book
from google.cloud.firestore_v1.base_query import FieldFilter, And  # Importante para búsquedas

class BookDAO:
    def __init__(self, database):
        """
        Constructor para la clase BookDAO.

        :param database: Objeto de conexión a Firestore.
        """
        self._database = database  # Ya recibimos la conexión
        self._collection = "books"
        
    def book_exists(self, book_id):
        """
        Verifica si ya existe un libro con el ID dado.

        Args:
            book_id: El ID del libro a verificar.

        Returns:
            bool: True si el libro existe, False en caso contrario.
        """
        try:
            doc_ref = self._database.collection(self._collection).document(book_id)
            doc = doc_ref.get()
            return doc.exists  # Devuelve True si el documento existe, False si no
        except Exception as e:
            print(f"Error al verificar la existencia del libro: {e}")
            return False  # En caso de error, asumimos que no existe (para evitar bloqueos)
        
    def add_book(self, book):
        """
        Agrega un nuevo libro a Firestore.
        """
        try:
            book_data = book.to_dict()
            self._database.collection(self._collection).document(book.get_book_id()).set(book_data)
            return True
        except Exception as e:
            print(f"Error al agregar el libro: {e}")
            return False

    def get_book_by_id(self, book_id):
        """
        Obtiene un libro por su ID desde Firestore.
        """
        try:
            doc_ref = self._database.collection(self._collection).document(book_id)
            doc = doc_ref.get()

            if doc.exists:
                return Book(**doc.to_dict())
            else:
                return None
        except Exception as e:
            print(f"Error al obtener el libro: {e}")
            return None

    def update_book(self, book):
        """
        Actualiza un libro en Firestore.
        """
        try:
            doc_ref = self._database.collection(self._collection).document(book.get_book_id())
            doc_ref.update(book.to_dict())
            return True
        except Exception as e:
            print(f"Error al actualizar el libro: {e}")
            return False

    def delete_book(self, book_id):
        """
        Elimina un libro de Firestore.
        """
        try:
            doc_ref = self._database.collection(self._collection).document(book_id)
            doc_ref.delete()
            return True
        except Exception as e:
            print(f"Error al eliminar el libro: {e}")
            return False

    def get_all_books(self):
        """
        Obtiene todos los libros de Firestore.
        """
        try:
            books_list = []
            docs = self._database.collection(self._collection).stream()

            for doc in docs:
                books_list.append(Book(**doc.to_dict()))
            return books_list
        except Exception as e:
            print(f"Error al obtener todos los libros: {e}")
            return []


    def search_books(self, criteria):
        """
        Busca libros según los criterios proporcionados (un diccionario).
        """
        try:
            books_list = []
            base_query = self._database.collection(self._collection)
            filters = []

            # Construir filtros para cada criterio
            for field, value in criteria.items():
                filters.append(FieldFilter(field, "==", value))

            # Combinar filtros con AND (si hay más de uno)
            if len(filters) > 1:
                combined_filter = And(*filters)
                query = base_query.where(filter=combined_filter)
            elif len(filters) == 1:
                query = base_query.where(filter=filters[0])
            else:  # No hay criterios
                return []

            docs = query.stream()
            for doc in docs:
                books_list.append(Book(**doc.to_dict()))

            return books_list

        except Exception as e:
            print(f"Error al buscar libros: {e}")
            return []
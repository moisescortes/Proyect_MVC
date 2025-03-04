from model.Objects.Book import Book
from google.cloud.firestore_v1.base_query import FieldFilter

class BookDAO:
    def __init__(self, database):
        """
        Constructor para la clase BookDAO.

        :param database: Objeto de conexión a la base de datos (Firestore).
        """
        self._database = database
        self._collection = "books"

    def add_book(self, book):
        """
        Agrega un nuevo libro a la base de datos Firestore.
        """
        try:
            # Convertir el objeto Book a un diccionario
            book_data = book.to_dict()
            # Agregar el libro a la colección "books".  add() genera el ID automáticamente.
            doc_ref = self._database.collection(self._collection).document(book.get_book_id()).set(book_data)
            return True
        except Exception as e:
            print(f"Error al agregar el libro: {e}")
            return False

    def get_book_by_id(self, book_id):
        """
        Obtiene un libro por su ID desde Firestore.
        """
        try:
            # Obtener una referencia al documento específico.
            doc_ref = self._database.collection(self._collection).document(book_id)
            doc = doc_ref.get()

            if doc.exists:
                # Crear un objeto Book a partir de los datos del documento.
                return Book(**doc.to_dict())
            else:
                return None  # El libro no existe
        except Exception as e:
            print(f"Error al obtener el libro: {e}")
            return None

    def update_book(self, book):
        """
        Actualiza un libro en Firestore.
        """
        try:
            # Obtener una referencia al documento.
            doc_ref = self._database.collection(self._collection).document(book.get_book_id())
            # Actualizar el documento.
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
            # Obtener una referencia al documento y eliminarlo.
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
            # Obtener todos los documentos de la colección.
            docs = self._database.collection(self._collection).stream()

            for doc in docs:
                # Crear un objeto Book para cada documento.
                books_list.append(Book(**doc.to_dict()))
            return books_list
        except Exception as e:
            print(f"Error al obtener todos los libros: {e}")
            return []

    def search_books(self, query):
        """
        Busca libros por título, autor o género en Firestore.
        """
        try:
            books_list = []
            # Realizar consultas separadas para cada campo. Firestore no tiene un operador OR nativo para consultas en diferentes campos.
            #Esto se debe a que, para buscar por título, autor y género con una sola consulta, se debe de crear un index compuesto.

            query = query.lower()

            # Buscar por título
            title_query = self._database.collection(self._collection).where(filter=FieldFilter("title", ">=", query)).where(filter=FieldFilter("title", "<=", query + "\uf8ff")).stream()
            for doc in title_query:
                books_list.append(Book(**doc.to_dict()))

            # Buscar por autor
            author_query = self._database.collection(self._collection).where(filter=FieldFilter("author", ">=", query)).where(filter=FieldFilter("author", "<=", query + "\uf8ff")).stream()
            for doc in author_query:
                # Evitar duplicados si ya se encontró en la consulta por título
                if doc.id not in [b.get_book_id() for b in books_list]:
                    books_list.append(Book(**doc.to_dict()))

            # Buscar por género
            genre_query = self._database.collection(self._collection).where(filter=FieldFilter("genre", ">=", query)).where(filter=FieldFilter("genre", "<=", query + "\uf8ff")).stream()
            for doc in genre_query:
                if doc.id not in [b.get_book_id() for b in books_list]:
                    books_list.append(Book(**doc.to_dict()))

            return books_list
        except Exception as e:
            print(f"Error al buscar libros: {e}")
            return []
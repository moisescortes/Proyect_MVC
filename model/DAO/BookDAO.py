from model.Objects.Book import Book

class BookDAO:
    def __init__(self, database):
        """
        Constructor para la clase BookDAO.

        :param database: Objeto de conexión a la base de datos (o Firebase).
        """
        self._database = database
        self._collection = "books" 

    def add_book(self, book):
        """
        Agrega un nuevo libro a la base de datos.

        :param book: Objeto de tipo Book.
        :return: True si se agregó correctamente, False en caso contrario.
        """
        try:
            # Convertir el objeto Book a un diccionario
            book_data = book.to_dict()
            # Agregar el libro a la colección "books"
            self._database.child(self._collection).push(book_data)
            return True
        except Exception as e:
            print(f"Error al agregar el libro: {e}")
            return False

    def get_book_by_id(self, book_id):
        """
        Obtiene un libro por su ID.

        :param book_id: Identificador único del libro.
        :return: Objeto de tipo Book si se encuentra, None en caso contrario.
        """
        try:
            # Buscar el libro por su ID en la colección "books"
            books = self._database.child(self._collection).get()
            if books:
                for key, value in books.items():
                    if value["book_id"] == book_id:
                        return Book(
                            book_id=value["book_id"],
                            title=value["title"],
                            author=value["author"],
                            genre=value["genre"],
                            status=value["status"]
                        )
            return None
        except Exception as e:
            print(f"Error al obtener el libro: {e}")
            return None

    def update_book(self, book):
        """
        Actualiza un libro en la base de datos.

        :param book: Objeto de tipo Book con los datos actualizados.
        :return: True si se actualizó correctamente, False en caso contrario.
        """
        try:
            # Convertir el objeto Book a un diccionario
            book_data = book.to_dict()
            # Buscar el libro por su ID en la colección "books"
            books = self._database.child(self._collection).get()
            if books:
                for key, value in books.items():
                    if value["book_id"] == book.get_book_id():
                        # Actualizar el libro en la base de datos
                        self._database.child(self._collection).child(key).update(book_data)
                        return True
            return False
        except Exception as e:
            print(f"Error al actualizar el libro: {e}")
            return False

    def delete_book(self, book_id):
        """
        Elimina un libro de la base de datos.

        :param book_id: Identificador único del libro.
        :return: True si se eliminó correctamente, False en caso contrario.
        """
        try:
            # Buscar el libro por su ID en la colección "books"
            books = self._database.child(self._collection).get()
            if books:
                for key, value in books.items():
                    if value["book_id"] == book_id:
                        # Eliminar el libro de la base de datos
                        self._database.child(self._collection).child(key).remove()
                        return True
            return False
        except Exception as e:
            print(f"Error al eliminar el libro: {e}")
            return False

    def get_all_books(self):
        """
        Obtiene todos los libros de la base de datos.

        :return: Lista de objetos de tipo Book.
        """
        try:
            books_list = []
            # Obtener todos los libros de la colección "books"
            books = self._database.child(self._collection).get()
            if books:
                for key, value in books.items():
                    book = Book(
                        book_id=value["book_id"],
                        title=value["title"],
                        author=value["author"],
                        genre=value["genre"],
                        status=value["status"]
                    )
                    books_list.append(book)
            return books_list
        except Exception as e:
            print(f"Error al obtener todos los libros: {e}")
            return []

    def search_books(self, query):
        """
        Busca libros por título, autor o género.

        :param query: Término de búsqueda (título, autor o género).
        :return: Lista de objetos de tipo Book que coinciden con la búsqueda.
        """
        try:
            books_list = []
            # Obtener todos los libros de la colección "books"
            books = self._database.child(self._collection).get()
            if books:
                for key, value in books.items():
                    if (query.lower() in value["title"].lower() or
                        query.lower() in value["author"].lower() or
                        query.lower() in value["genre"].lower()):
                        book = Book(
                            book_id=value["book_id"],
                            title=value["title"],
                            author=value["author"],
                            genre=value["genre"],
                            status=value["status"]
                        )
                        books_list.append(book)
            return books_list
        except Exception as e:
            print(f"Error al buscar libros: {e}")
            return []
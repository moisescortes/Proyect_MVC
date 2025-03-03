from model.DAO.BookDAO import BookDAO
from model.Objects.Book import Book

class BookController:
    def __init__(self, database):
        """
        Constructor para la clase ControladorBook.

        :param database: Objeto de conexión a la base de datos (Firebase).
        """
        self._book_dao = BookDAO(database)  # Crear una instancia de BookDAO

    def agregar_libro(self, book_id, title, author, genre, status="available"):
        """
        Agrega un nuevo libro a la base de datos.

        :param book_id: Identificador único del libro.
        :param title: Título del libro.
        :param author: Autor del libro.
        :param genre: Género del libro.
        :param status: Estado del libro ("available" o "borrowed"), por defecto es "available".
        :return: True si se agregó correctamente, False en caso contrario.
        """
        # Crear un objeto Book
        libro = Book(book_id=book_id, title=title, author=author, genre=genre, status=status)
        # Agregar el libro a la base de datos
        return self._book_dao.add_book(libro)

    def eliminar_libro(self, book_id):
        """
        Elimina un libro de la base de datos.

        :param book_id: Identificador único del libro.
        :return: True si se eliminó correctamente, False en caso contrario.
        """
        return self._book_dao.delete_book(book_id)

    def actualizar_libro(self, book_id, title=None, author=None, genre=None, status=None):
        """
        Actualiza un libro en la base de datos.

        :param book_id: Identificador único del libro.
        :param title: Nuevo título del libro (opcional).
        :param author: Nuevo autor del libro (opcional).
        :param genre: Nuevo género del libro (opcional).
        :param status: Nuevo estado del libro (opcional).
        :return: True si se actualizó correctamente, False en caso contrario.
        """
        # Obtener el libro por su ID
        libro = self._book_dao.get_book_by_id(book_id)
        if libro:
            # Actualizar los campos si se proporcionan nuevos valores
            if title:
                libro.set_title(title)
            if author:
                libro.set_author(author)
            if genre:
                libro.set_genre(genre)
            if status:
                libro.set_status(status)
            # Guardar los cambios en la base de datos
            return self._book_dao.update_book(libro)
        return False

    def buscar_libro_por_id(self, book_id):
        """
        Busca un libro por su ID.

        :param book_id: Identificador único del libro.
        :return: Objeto de tipo Book si se encuentra, None en caso contrario.
        """
        return self._book_dao.get_book_by_id(book_id)

    def buscar_libros_por_titulo(self, titulo):
        """
        Busca libros por título.

        :param titulo: Título o parte del título a buscar.
        :return: Lista de objetos de tipo Book que coinciden con la búsqueda.
        """
        return self._book_dao.search_books(titulo)

    def buscar_libros_por_autor(self, autor):
        """
        Busca libros por autor.

        :param autor: Autor o parte del nombre del autor a buscar.
        :return: Lista de objetos de tipo Book que coinciden con la búsqueda.
        """
        return self._book_dao.search_books(autor)

    def buscar_libros_por_genero(self, genero):
        """
        Busca libros por género.

        :param genero: Género o parte del género a buscar.
        :return: Lista de objetos de tipo Book que coinciden con la búsqueda.
        """
        return self._book_dao.search_books(genero)

    def obtener_todos_los_libros(self):
        """
        Obtiene todos los libros de la base de datos.

        :return: Lista de objetos de tipo Book.
        """
        return self._book_dao.get_all_books()
class Book:
    def __init__(self, book_id, title, author, genre, status="available"):
        """
        Constructor para la clase Book.

        :param book_id: Identificador único del libro.
        :param title: Título del libro.
        :param author: Autor del libro.
        :param genre: Género del libro.
        :param status: Estado del libro ("available" o "borrowed"), por defecto es "available".
        """
        self._book_id = book_id
        self._title = title
        self._author = author
        self._genre = genre
        self._status = status

    # Getters
    def get_book_id(self):
        return self._book_id

    def get_title(self):
        return self._title

    def get_author(self):
        return self._author

    def get_genre(self):
        return self._genre

    def get_status(self):
        return self._status

    # Setters
    def set_book_id(self, book_id):
        self._book_id = book_id

    def set_title(self, title):
        self._title = title

    def set_author(self, author):
        self._author = author

    def set_genre(self, genre):
        self._genre = genre

    def set_status(self, status):
        if status in ["available", "borrowed"]:
            self._status = status
        else:
            raise ValueError("Invalid status. Use 'available' or 'borrowed'.")

    # Método para representar el objeto en formato JSON para Firebase
    def to_dict(self):
        """
        Convierte el objeto Book a un diccionario JSON para almacenar en Firebase.
        """
        return {
            "book_id": self._book_id,
            "title": self._title,
            "author": self._author,
            "genre": self._genre,
            "status": self._status
        }

    # Método especial para representación en string
    def __str__(self):
        return f"Book(ID: {self._book_id}, Title: {self._title}, Author: {self._author}, Genre: {self._genre}, Status: {self._status})"
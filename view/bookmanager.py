from PyQt5 import QtWidgets
from view.ui_bookmanager import Ui_BookManager  # Importa la UI generada por Qt Designer
from model.Objects.Book import Book


class BookManagerView(QtWidgets.QWidget):  # Cambiado a QWidget (o QMainWindow si prefieres)
    def __init__(self):
        super().__init__()
        self.ui = Ui_BookManager()
        self.ui.setupUi(self)
        self.setup_connections() # Conecta las señales a los slots

    def setup_connections(self):
        """
        Conecta las señales (eventos de la UI) a los slots (métodos) que se deben ejecutar.
        Estos slots se implementarán en el BookController.
        """
        self.ui.btn_add.clicked.connect(self.add_book_clicked)
        self.ui.btn_search.clicked.connect(self.search_book_clicked)
        self.ui.btn_update.clicked.connect(self.update_book_clicked)
        self.ui.btn_delete.clicked.connect(self.delete_book_clicked)

    def get_form_data(self):
        """
        Obtiene los datos ingresados en los campos de la interfaz.

        Returns:
            dict: Un diccionario con los datos del formulario.
        """
        book_id = self.ui.txt_book_id.text()
        title = self.ui.txt_title.text()
        author = self.ui.txt_author.text()
        genre = self.ui.txt_genre.text()
        status = self.ui.cmb_status.currentText()  # Obtiene el texto seleccionado del QComboBox
        return {
            "book_id": book_id,
            "title": title,
            "author": author,
            "genre": genre,
            "status": status,
        }
    
    def clear_form(self):
        """Limpia los campos del formulario."""
        self.ui.txt_book_id.clear()
        self.ui.txt_title.clear()
        self.ui.txt_author.clear()
        self.ui.txt_genre.clear()
        # No es necesario limpiar el QComboBox, ya que siempre tiene una opción seleccionada


    def update_table(self, books):
        """
        Actualiza la tabla de libros en la interfaz.

        Args:
            books (list): Una lista de objetos Book.
        """
        self.ui.table_books.clearContents()  # Limpia el contenido actual de la tabla
        self.ui.table_books.setRowCount(0)   # Reinicia el número de filas
        self.ui.table_books.setColumnCount(5)  # Establece el número de columnas (ajusta según tus necesidades)
        self.ui.table_books.setHorizontalHeaderLabels(["ID", "Título", "Autor", "Género", "Estado"])


        for row_number, book in enumerate(books):
            self.ui.table_books.insertRow(row_number)  # Inserta una nueva fila
            self.ui.table_books.setItem(row_number, 0, QtWidgets.QTableWidgetItem(book.get_book_id()))
            self.ui.table_books.setItem(row_number, 1, QtWidgets.QTableWidgetItem(book.get_title()))
            self.ui.table_books.setItem(row_number, 2, QtWidgets.QTableWidgetItem(book.get_author()))
            self.ui.table_books.setItem(row_number, 3, QtWidgets.QTableWidgetItem(book.get_genre()))
            self.ui.table_books.setItem(row_number, 4, QtWidgets.QTableWidgetItem(book.get_status()))

    def show_message(self, title, message, icon=QtWidgets.QMessageBox.Information):
        """Muestra un mensaje al usuario."""
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()
    
    # Señales que se emitirán al controlador.  Estos métodos *no* hacen el trabajo,
    # solo *señalan* que el usuario hizo algo.
    def add_book_clicked(self):
        pass # Se conecta a un slot en el controlador

    def search_book_clicked(self):
        pass # Se conecta a un slot en el controlador

    def update_book_clicked(self):
        pass # Se conecta a un slot en el controlador

    def delete_book_clicked(self):
        pass # Se conecta a un slot en el controlador
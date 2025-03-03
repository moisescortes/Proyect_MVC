from PyQt5.QtWidgets import QMainWindow
from ui_bookmanager import Ui_BookManager
from controllers.BookController import BookController

class BookManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_BookManager()
        self.ui.setupUi(self)
        self.controller = BookController(database="firebase")

        # Conectar botones con funciones
        self.ui.btn_add.clicked.connect(self.add_book)

    def add_book(self):
        book_id = self.ui.txt_book_id.text()
        title = self.ui.txt_title.text()
        author = self.ui.txt_author.text()
        genre = self.ui.txt_genre.text()
        status = self.ui.cmb_status.currentText()

        if self.controller.agregar_libro(book_id, title, author, genre, status):
            print("Libro agregado correctamente")
        else:
            print("Error al agregar el libro")

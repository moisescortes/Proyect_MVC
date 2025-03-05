from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp, Qt

from view.ui_bookmanager import Ui_BookDialog  # Asegúrate de que esta ruta sea correcta
from model.DAO.BookDAO import BookDAO
from model.Objects.Book import Book
from dbConnection.VerifyConnection import VerifyConnection


class BookController(QDialog):
    def __init__(self, database):
        super().__init__()
        self.ui = Ui_BookDialog()
        self.ui.setupUi(self)
        self._book_dao = BookDAO(database)
        self.initializeGUI()
        self.load_books_to_table()  # Cargar libros al iniciar

    def initializeGUI(self):
        self.ui.btn_add.clicked.connect(self.addBook)
        self.ui.btn_update.clicked.connect(self.updateBook)
        self.ui.btn_delete.clicked.connect(self.deleteBook)
        self.ui.btn_search.clicked.connect(self.searchBook)

        # Validadores (permite números y letras, según corresponda)
        self.ui.txt_book_id.setValidator(QRegExpValidator(QRegExp("[0-9]+"), self))  # Solo números para ID
        self.ui.txt_title.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9\\s\\.,:-]+"), self)) # Permitir alfanumerico, espacios, y algunos simbolos.
        self.ui.txt_author.setValidator(QRegExpValidator(QRegExp("[a-zA-Z\\s]+"), self)) # Solo letras y espacios
        self.ui.txt_genre.setValidator(QRegExpValidator(QRegExp("[a-zA-Z\\s]+"), self)) # Solo letras y espacios


        # Conectar el doble clic en la tabla para editar
        self.ui.table_books.itemDoubleClicked.connect(self.load_book_to_edit)


    def _get_form_data(self):
        """Helper function to get form data."""
        return {
            "book_id": self.ui.txt_book_id.text(),
            "title": self.ui.txt_title.text(),
            "author": self.ui.txt_author.text(),
            "genre": self.ui.txt_genre.text(),
            "status": self.ui.cmb_status.currentText(),
        }

    def _validate_form_data(self, book_data):
        """Validates the form data."""
        if not book_data['book_id'] or not book_data['title'] or not book_data['author'] or not book_data['genre']: # CAMBIO AQUÍ: 'id' -> 'book_id'
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return False
        return True

    def load_books_to_table(self):
        """Loads all books from the database into the table."""
        try:
            if VerifyConnection.verify_connection(self):
                books = self._book_dao.get_all_books()
                self.ui.table_books.setRowCount(0)  # Limpiar la tabla
                for book in books:
                    row = self.ui.table_books.rowCount()
                    self.ui.table_books.insertRow(row)
                    self.ui.table_books.setItem(row, 0, QTableWidgetItem(book.get_book_id()))
                    self.ui.table_books.setItem(row, 1, QTableWidgetItem(book.get_title()))
                    self.ui.table_books.setItem(row, 2, QTableWidgetItem(book.get_author()))
                    self.ui.table_books.setItem(row, 3, QTableWidgetItem(book.get_genre()))
                    self.ui.table_books.setItem(row, 4, QTableWidgetItem(book.get_status()))
            else:
                QMessageBox.critical(self, "Error", "No Internet connection.", QMessageBox.Ok)

        except Exception as e:
            print(f"❌ Error al cargar libros: {e}")
            QMessageBox.critical(self, "Error", "Error al cargar libros.", QMessageBox.Ok)

    def addBook(self):
        """Adds a new book to the database."""
        try:
            book_data = self._get_form_data()
            if not self._validate_form_data(book_data):
                return  # Stop if validation fails

            if VerifyConnection.verify_connection(self):
                # Verificar si el libro ya existe
                if self._book_dao.book_exists(book_data["book_id"]):
                    QMessageBox.warning(self, "Error", "Ya existe un libro con ese ID.", QMessageBox.Ok)
                    return  # Detener la operación si el libro ya existe

                new_book = Book(**book_data)

                if self._book_dao.add_book(new_book):
                    QMessageBox.information(self, 'Confirmation', "Libro agregado exitosamente ✔", QMessageBox.Ok)
                    self.clearFields()
                    self.load_books_to_table() # Recargar la tabla
                else:
                    QMessageBox.critical(self, "Error", "Error al agregar el libro.", QMessageBox.Ok)
            else:
                QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)

        except Exception as e:
            print(f"❌ Error : {e}")
            QMessageBox.critical(self, "Error", "Ocurrió un error inesperado.", QMessageBox.Ok)
    
    def load_book_to_edit(self, item):
        """Loads the selected book data into the form for editing."""
        row = item.row()
        book_id = self.ui.table_books.item(row, 0).text()  # Obtener el ID del libro

        if VerifyConnection.verify_connection(self):
            book = self._book_dao.get_book_by_id(book_id)
            if book:
                self.ui.txt_book_id.setText(book.get_book_id())
                self.ui.txt_book_id.setEnabled(False) # Deshabilitar edición del ID
                self.ui.txt_title.setText(book.get_title())
                self.ui.txt_author.setText(book.get_author())
                self.ui.txt_genre.setText(book.get_genre())
                self.ui.cmb_status.setCurrentText(book.get_status())  # Usar setCurrentText
        else:
            QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)
            
    def updateBook(self):
        """Updates an existing book in the database."""
        try:
            book_data = self._get_form_data()  # Obtener datos del formulario
            if not self._validate_form_data(book_data):
                return

            if VerifyConnection.verify_connection(self):
                 # Crear un objeto Book con los datos actualizados
                 updated_book = Book(**book_data)  # Esto ahora funcionará correctamente
                 if self._book_dao.update_book(updated_book):
                    QMessageBox.information(self, 'Confirmation', "Libro actualizado exitosamente ✔", QMessageBox.Ok)
                    self.clearFields()
                    self.load_books_to_table()
                    self.ui.txt_book_id.setEnabled(True)  # Habilitar de nuevo el campo ID
                 else:
                    QMessageBox.critical(self, "Error", "Error al actualizar el libro.", QMessageBox.Ok)
            else:
                QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)

        except Exception as e:
            print(f"❌ Error al actualizar: {e}")
            QMessageBox.critical(self, "Error", "Ocurrió un error inesperado al actualizar.", QMessageBox.Ok)

    def deleteBook(self):
        """Deletes a book from the database."""
        selected_row = self.ui.table_books.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Selecciona un libro para eliminar.")
            return

        book_id = self.ui.table_books.item(selected_row, 0).text()

        # Confirmación
        confirm = QMessageBox.question(self, "Confirmar", f"¿Estás seguro de eliminar el libro con ID '{book_id}'?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                if VerifyConnection.verify_connection(self):
                    if self._book_dao.delete_book(book_id):
                         QMessageBox.information(self, "Confirmación", "Libro eliminado exitosamente.", QMessageBox.Ok)
                         self.load_books_to_table()
                    else:
                         QMessageBox.critical(self, "Error", "Error al eliminar el libro.", QMessageBox.Ok)
                else:
                     QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)

            except Exception as e:
                print(f"❌ Error al eliminar: {e}")
                QMessageBox.critical(self, "Error", "Ocurrió un error inesperado al eliminar.", QMessageBox.Ok)

    def searchBook(self):
        """Searches for books based on criteria entered in the form fields."""
        try:
            if not VerifyConnection.verify_connection(self):
                QMessageBox.critical(self, "Error", "No Internet connection.", QMessageBox.Ok)
                return

            # 1. Recolectar los criterios de búsqueda (que NO estén vacíos)
            search_criteria = {}
            if self.ui.txt_book_id.text().strip():
                search_criteria["book_id"] = self.ui.txt_book_id.text().strip()
            if self.ui.txt_title.text().strip():
                search_criteria["title"] = self.ui.txt_title.text().strip()
            if self.ui.txt_author.text().strip():
                search_criteria["author"] = self.ui.txt_author.text().strip()
            if self.ui.txt_genre.text().strip():
                search_criteria["genre"] = self.ui.txt_genre.text().strip()

            # 2. Si no hay criterios, mostrar todos los libros
            if not search_criteria:
                self.load_books_to_table()
                return

            # 3. Llamar al DAO con los criterios
            results = self._book_dao.search_books(search_criteria)

            # 4. Mostrar resultados
            self.ui.table_books.setRowCount(0)
            for book in results:
                row = self.ui.table_books.rowCount()
                self.ui.table_books.insertRow(row)
                self.ui.table_books.setItem(row, 0, QTableWidgetItem(book.get_book_id()))
                self.ui.table_books.setItem(row, 1, QTableWidgetItem(book.get_title()))
                self.ui.table_books.setItem(row, 2, QTableWidgetItem(book.get_author()))
                self.ui.table_books.setItem(row, 3, QTableWidgetItem(book.get_genre()))
                self.ui.table_books.setItem(row, 4, QTableWidgetItem(book.get_status()))


        except Exception as e:
            print(f"Error en la búsqueda: {e}")
            QMessageBox.critical(self, "Error", "Ocurrió un error en la búsqueda.", QMessageBox.Ok)
    
    
    def clearFields(self):
        """Clears all input fields in the form."""
        self.ui.txt_book_id.clear()
        self.ui.txt_title.clear()
        self.ui.txt_author.clear()
        self.ui.txt_genre.clear()
        self.ui.cmb_status.setCurrentIndex(0)  # Restablecer el ComboBox
        self.ui.txt_book_id.setEnabled(True) # Asegurar que el campo ID esté habilitado

    def showEvent(self, event):
        """Sobreescribimos showEvent para cargar los libros al mostrar el diálogo."""
        super().showEvent(event)  # Llama al método de la clase base
        self.load_books_to_table()
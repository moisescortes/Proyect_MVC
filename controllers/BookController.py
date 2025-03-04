from model.DAO.BookDAO import BookDAO
from model.Objects.Book import Book
from view.bookmanager import BookManagerView  # Importa la vista
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox

class BookController:  # Ya no hereda de QMainWindow
    def __init__(self, database):
        self._database = database  # Usar directamente la conexión
        self._book_dao = BookDAO(self._database)  # Pasar la conexión al DAO
        self.view = BookManagerView()
        self.connect_signals()

    def connect_signals(self):
        """Conecta las señales de la vista a los slots del controlador."""
        self.view.ui.btn_add.clicked.connect(self.add_book)
        self.view.ui.btn_search.clicked.connect(self.search_book)
        self.view.ui.btn_update.clicked.connect(self.update_book)
        self.view.ui.btn_delete.clicked.connect(self.delete_book)
        # Conectar la señal de selección de la tabla
        self.view.ui.table_books.itemSelectionChanged.connect(self.load_selected_book)


    def show_view(self):
        """Muestra la vista."""
        self.view.show()
        self.load_all_books()  # Cargar todos los libros al iniciar


    def load_all_books(self):
        """Carga todos los libros desde la base de datos y actualiza la tabla."""
        books = self._book_dao.get_all_books()
        self.view.update_table(books)
        
    def load_selected_book(self):
        """Carga los datos del libro seleccionado en los campos de texto."""
        selected_items = self.view.ui.table_books.selectedItems()
        if not selected_items:
            return  # No hay nada seleccionado

        # Obtenemos la fila del primer item seleccionado
        row = selected_items[0].row()

        # Obtenemos los datos de la fila.  Asumiendo que el ID está en la columna 0
        book_id = self.view.ui.table_books.item(row, 0).text()
        book = self._book_dao.get_book_by_id(book_id)

        if book:
            # Llenar los campos del formulario
            self.view.ui.txt_book_id.setText(book.get_book_id())
            self.view.ui.txt_title.setText(book.get_title())
            self.view.ui.txt_author.setText(book.get_author())
            self.view.ui.txt_genre.setText(book.get_genre())
            # Seleccionar el estado correcto en el QComboBox
            index = self.view.ui.cmb_status.findText(book.get_status())
            if index >= 0:
                self.view.ui.cmb_status.setCurrentIndex(index)


    def add_book(self):
        """Manejador del evento de clic en el botón 'Agregar'."""
        book_data = self.view.get_form_data()
        try:
            # Validación básica
            if not all([book_data['book_id'], book_data['title'], book_data['author'], book_data['genre']]):
                self.view.show_message("Error", "Por favor, complete todos los campos.", icon=QMessageBox.Warning)
                return
            
            #Intenta convertir el book_id a entero
            try:
                book_id_int = book_data['book_id']
            except ValueError:
                self.view.show_message("Error", "El ID del libro debe ser un número.", icon=QMessageBox.Warning)
                return
            
            #Verifica si el libro ya existe
            if self._book_dao.get_book_by_id(book_data["book_id"]):
                self.view.show_message("Error", "Ya existe un libro con ese ID", icon=QMessageBox.Warning)
                return

            new_book = Book(
                book_data["book_id"],
                book_data["title"],
                book_data["author"],
                book_data["genre"],
                book_data["status"],
            )
            if self._book_dao.add_book(new_book):
                self.view.show_message("Éxito", "Libro agregado correctamente.")
                self.load_all_books()  # Recargar la tabla
                self.view.clear_form() # Limpiar el formulario
            else:
                self.view.show_message("Error", "No se pudo agregar el libro.", icon=QMessageBox.Critical)

        except Exception as e:
            self.view.show_message("Error", f"Error al agregar el libro: {e}", icon=QMessageBox.Critical)

    def search_book(self):
        """Manejador del evento de clic en el botón 'Buscar'."""
        book_data = self.view.get_form_data()  # Obtener los datos del formulario
        query = book_data["book_id"] or book_data["title"] or book_data["author"] or book_data["genre"] # Busca por el criterio que se haya ingresado

        if not query:
            self.view.show_message("Error", "Ingrese un criterio de búsqueda.", icon=QMessageBox.Warning)
            return

        if book_data["book_id"]:
            # Priorizar búsqueda por ID si se proporciona
            book = self._book_dao.get_book_by_id(book_data["book_id"])
            if book:
                self.view.update_table([book])  # Mostrar solo el libro encontrado
            else:
                self.view.show_message("Info", "No se encontró ningún libro con ese ID.", icon=QMessageBox.Information)
                self.load_all_books()

        
        else:
            #Si no hay id, busca por otros criterios
            books = self._book_dao.search_books(query)
            if books:
                self.view.update_table(books)
            else:
                self.view.show_message("Info", "No se encontraron libros con ese criterio de búsqueda.", icon=QMessageBox.Information)
                self.load_all_books()

    def update_book(self):
        """Manejador del evento de clic en el botón 'Actualizar'."""
        book_data = self.view.get_form_data()
        
        if not book_data['book_id']:
            self.view.show_message("Error", "Debe ingresar el ID del libro a actualizar.", icon=QMessageBox.Warning)
            return

        #Verifica que exista
        existing_book = self._book_dao.get_book_by_id(book_data["book_id"])
        if not existing_book:
            self.view.show_message("Error", "No existe un libro con ese ID.", icon=QMessageBox.Warning)
            return


        updated_book = Book(
            book_data["book_id"],
            book_data["title"],
            book_data["author"],
            book_data["genre"],
            book_data["status"],
        )
        if self._book_dao.update_book(updated_book):
            self.view.show_message("Éxito", "Libro actualizado correctamente.")
            self.load_all_books()  # Recargar la tabla
            self.view.clear_form()
        else:
            self.view.show_message("Error", "No se pudo actualizar el libro.", icon=QMessageBox.Critical)

    def delete_book(self):
        """Manejador del evento de clic en el botón 'Eliminar'."""
        book_id = self.view.ui.txt_book_id.text()
        
        if not book_id:
            self.view.show_message("Error", "Debe ingresar el ID del libro a eliminar.", icon=QMessageBox.Warning)
            return

        if not self._book_dao.get_book_by_id(book_id):
            self.view.show_message("Error", "No existe un libro con ese ID.", icon=QMessageBox.Warning)
            return
    
        if self._book_dao.delete_book(book_id):
            self.view.show_message("Éxito", "Libro eliminado correctamente.")
            self.load_all_books()  # Recargar la tabla
            self.view.clear_form()
        else:
            self.view.show_message("Error", "No se pudo eliminar el libro.", icon=QMessageBox.Critical)
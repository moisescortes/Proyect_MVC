from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QDate, Qt
from view.ui_loanmanager import Ui_LoanManagerDialog  # Cambia esto
from model.DAO.LoanDAO import LoanDAO
from model.DAO.LaptopDAO import LaptopDAO
from model.DAO.UserDAO import UserDAO # Para validar el tipo de usuario
from model.Objects.Loan import Loan
from model.Objects.Professor import Professor  # Para validar el tipo de usuario
from dbConnection.VerifyConnection import VerifyConnection
import random
import string
from datetime import datetime, date



class LoanController(QDialog):
    def __init__(self, database):
        super().__init__()
        self.ui = Ui_LoanManagerDialog()
        self.ui.setupUi(self)
        self._loan_dao = LoanDAO(database)
        self._laptop_dao = LaptopDAO(database) # Para interactuar con laptops
        self._user_dao = UserDAO(database) # Para obtener usuarios
        self.initializeGUI()
        self.load_loans_to_table()
        self.load_laptop_loans_to_table()

    def initializeGUI(self):
        self.ui.btn_add_loan.clicked.connect(self.add_book_loan)
        self.ui.btn_update_loan.clicked.connect(self.update_book_loan)
        self.ui.btn_delete_loan.clicked.connect(self.delete_book_loan)
        self.ui.btn_search_loan.clicked.connect(self.search_book_loans)
        self.ui.table_loans.itemDoubleClicked.connect(self.load_book_loan_to_edit)
        # Pestaña de laptops
        self.ui.btn_add_laptop.clicked.connect(self.add_laptop_loan)
        self.ui.btn_update_laptop.clicked.connect(self.update_laptop_loan)
        self.ui.btn_delete_laptop.clicked.connect(self.delete_laptop_loan)
        self.ui.btn_search_laptop.clicked.connect(self.search_laptop_loans)
        self.ui.table_laptops.itemDoubleClicked.connect(self.load_laptop_loan_to_edit)
        # Filtros
        self.ui.cmb_loan_filter.currentIndexChanged.connect(self.filter_book_loans)
        self.ui.cmb_laptop_filter.currentIndexChanged.connect(self.filter_laptop_loans)
        # Fechas (hoy por defecto)
        today = QDate.currentDate()
        self.ui.date_start.setDate(today)
        self.ui.date_end.setDate(today.addDays(14))  # 14 días por defecto
        self.ui.date_start_laptop.setDate(today)
        self.ui.date_end_laptop.setDate(today.addDays(14))  # 14 días por defecto


    def _get_book_loan_form_data(self):
        """Obtiene los datos del formulario de préstamos de libros."""
        return {
            "loan_id": self.ui.txt_loan_id.text(),
            "user_id": self.ui.txt_user_id_loan.text(),
            "item_id": self.ui.txt_book_id_loan.text(),
            "start_date": self.ui.date_start.date().toString(Qt.ISODate),
            "end_date": self.ui.date_end.date().toString(Qt.ISODate),
            "status": self.ui.cmb_status_loan.currentText(),
            "item_type": "book"
        }

    def _get_laptop_loan_form_data(self):
        """Obtiene los datos del formulario de préstamos de laptops."""
        return {
            "loan_id": self.ui.txt_laptop_loan_id.text(),
            "user_id": self.ui.txt_user_id_laptop.text(),
            "item_id": self.ui.txt_laptop_id.text(),
            "start_date": self.ui.date_start_laptop.date().toString(Qt.ISODate),
            "end_date": self.ui.date_end_laptop.date().toString(Qt.ISODate),
            "status": self.ui.cmb_status_laptop.currentText(),
            "item_type": "laptop"
        }

    def _validate_loan_data(self, loan_data):
        """Valida los datos del préstamo (común para libros y laptops)."""
        if not loan_data["user_id"] or not loan_data["item_id"]:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return False

        # Validar formato de fecha (ya hecho por QDateEdit)
        return True

    def _validate_professor(self, user_id):
        """Valida si el usuario es un profesor."""
        user = self._user_dao.get_user_by_id(user_id)
        if user.get_user_type() != 'profesor': 
            return False
        return True
    

    def load_loans_to_table(self):
        """Carga todos los préstamos de libros en la tabla."""
        try:
            if not VerifyConnection.verify_connection(self):
                QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)
                return

            loans = self._loan_dao.get_all_loans()
            self.ui.table_loans.setRowCount(0)
            for loan in loans:
                if loan.get_item_type() == "book":  # Solo préstamos de libros
                    row = self.ui.table_loans.rowCount()
                    self.ui.table_loans.insertRow(row)
                    self.ui.table_loans.setItem(row, 0, QTableWidgetItem(loan.get_loan_id()))
                    self.ui.table_loans.setItem(row, 1, QTableWidgetItem(loan.get_user_id()))
                    self.ui.table_loans.setItem(row, 2, QTableWidgetItem(loan.get_item_id()))
                    self.ui.table_loans.setItem(row, 3, QTableWidgetItem(loan.get_start_date()))
                    self.ui.table_loans.setItem(row, 4, QTableWidgetItem(loan.get_end_date()))
                    self.ui.table_loans.setItem(row, 5, QTableWidgetItem(loan.get_status()))

        except Exception as e:
            print(f"Error al cargar préstamos de libros: {e}")
            QMessageBox.critical(self, "Error", "Error al cargar préstamos de libros.", QMessageBox.Ok)

    def load_laptop_loans_to_table(self):
        """Carga todos los préstamos de laptops en la tabla."""
        try:
            if not VerifyConnection.verify_connection(self):
                QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)
                return

            loans = self._loan_dao.get_all_loans()
            self.ui.table_laptops.setRowCount(0)
            for loan in loans:
                if loan.get_item_type() == "laptop":  # Solo préstamos de laptops
                    row = self.ui.table_laptops.rowCount()
                    self.ui.table_laptops.insertRow(row)
                    self.ui.table_laptops.setItem(row, 0, QTableWidgetItem(loan.get_loan_id()))
                    self.ui.table_laptops.setItem(row, 1, QTableWidgetItem(loan.get_user_id()))
                    self.ui.table_laptops.setItem(row, 2, QTableWidgetItem(loan.get_item_id()))
                    self.ui.table_laptops.setItem(row, 3, QTableWidgetItem(loan.get_start_date()))
                    self.ui.table_laptops.setItem(row, 4, QTableWidgetItem(loan.get_end_date()))
                    self.ui.table_laptops.setItem(row, 5, QTableWidgetItem(loan.get_status()))

        except Exception as e:
            print(f"Error al cargar préstamos de laptops: {e}")
            QMessageBox.critical(self, "Error", "Error al cargar préstamos de laptops.", QMessageBox.Ok)
    
    def add_book_loan(self):
        """Agrega un nuevo préstamo de libro."""
        try:
            loan_data = self._get_book_loan_form_data()
            if not self._validate_loan_data(loan_data):
                return
            
            if not VerifyConnection.verify_connection(self):
                QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)
                return
            
            loan_data["loan_id"] = self._loan_dao._generate_loan_id() # Generar ID
            new_loan = Loan(**loan_data)
            print(new_loan)
            if self._loan_dao.add_loan(new_loan):
                # Actualizar el estado del libro a "Prestado"
                self._book_dao.update_book_status(loan_data["item_id"], "Prestado")
                QMessageBox.information(self, "Confirmación", "Préstamo de libro agregado exitosamente.", QMessageBox.Ok)
                self.clear_book_loan_fields()
                self.load_loans_to_table()
            else:
                QMessageBox.critical(self, "Error", "Error al agregar el préstamo de libro.", QMessageBox.Ok)

        except Exception as e:
            print(f"Error al agregar préstamo de libro: {e}")
            QMessageBox.critical(self, "Error", "Ocurrió un error inesperado.", QMessageBox.Ok)
    
    def add_laptop_loan(self):
        """Agrega un nuevo préstamo de laptop (solo para profesores)."""
        try:
            loan_data = self._get_laptop_loan_form_data()
            if not self._validate_loan_data(loan_data):
                return

            if not VerifyConnection.verify_connection(self):
                QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)
                return

            # Validación de profesor
            if not self._validate_professor(loan_data["user_id"]):
                QMessageBox.warning(self, "Error", "Solo los profesores pueden solicitar préstamos de laptops.", QMessageBox.Ok)
                return
            
            # Verificar disponibilidad de la laptop.
            laptop = self._laptop_dao.get_laptop_by_id(loan_data["item_id"])  # Usar item_id
            if not laptop or laptop.get_status() != "Disponible":
                QMessageBox.warning(self, "Error", "La laptop no está disponible.", QMessageBox.Ok)
                return

            loan_data["loan_id"] = self._loan_dao._generate_loan_id() # Generar el ID
            new_loan = Loan(**loan_data)

            if self._loan_dao.add_loan(new_loan):
                # Actualizar el estado de la laptop a "Prestado"
                self._laptop_dao.update_laptop_status(loan_data["item_id"], "Prestado")
                QMessageBox.information(self, "Confirmación", "Préstamo de laptop agregado exitosamente.", QMessageBox.Ok)
                self.clear_laptop_loan_fields()
                self.load_laptop_loans_to_table()
            else:
                QMessageBox.critical(self, "Error", "Error al agregar el préstamo de laptop.", QMessageBox.Ok)


        except Exception as e:
            print(f"Error al agregar préstamo de laptop: {e}")
            QMessageBox.critical(self, "Error", "Ocurrió un error inesperado.", QMessageBox.Ok)
    
    def load_book_loan_to_edit(self, item):
        """Carga los datos de un préstamo de libro seleccionado para editar."""
        row = item.row()
        loan_id = self.ui.table_loans.item(row, 0).text()

        if not VerifyConnection.verify_connection(self):
             QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)
             return

        loan = self._loan_dao.get_loan_by_id(loan_id)
        if loan:
            self.ui.txt_loan_id.setText(loan.get_loan_id())
            self.ui.txt_user_id_loan.setText(loan.get_user_id())
            self.ui.txt_book_id_loan.setText(loan.get_item_id())
            self.ui.date_start.setDate(QDate.fromString(loan.get_start_date(), Qt.ISODate))
            self.ui.date_end.setDate(QDate.fromString(loan.get_end_date(), Qt.ISODate))
            self.ui.cmb_status_loan.setCurrentText(loan.get_status())

    def load_laptop_loan_to_edit(self, item):
        """Carga los datos de un préstamo de laptop seleccionado para editar."""
        row = item.row()
        loan_id = self.ui.table_laptops.item(row, 0).text()

        if not VerifyConnection.verify_connection(self):
            QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)
            return

        loan = self._loan_dao.get_loan_by_id(loan_id)
        if loan:
            self.ui.txt_laptop_loan_id.setText(loan.get_loan_id())
            self.ui.txt_user_id_laptop.setText(loan.get_user_id())
            self.ui.txt_laptop_id.setText(loan.get_item_id())
            self.ui.date_start_laptop.setDate(QDate.fromString(loan.get_start_date(), Qt.ISODate))
            self.ui.date_end_laptop.setDate(QDate.fromString(loan.get_end_date(), Qt.ISODate))
            self.ui.cmb_status_laptop.setCurrentText(loan.get_status())

    def update_book_loan(self):
        """Actualiza un préstamo de libro existente."""
        try:
            loan_data = self._get_book_loan_form_data()
            if not self._validate_loan_data(loan_data):
                return

            if not VerifyConnection.verify_connection(self):
                QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)
                return

            updated_loan = Loan(**loan_data)
            if self._loan_dao.update_loan(updated_loan):
                QMessageBox.information(self, "Confirmación", "Préstamo de libro actualizado exitosamente.", QMessageBox.Ok)
                self.clear_book_loan_fields()
                self.load_loans_to_table()
            else:
                QMessageBox.critical(self, "Error", "Error al actualizar el préstamo de libro.", QMessageBox.Ok)

        except Exception as e:
            print(f"Error al actualizar préstamo de libro: {e}")
            QMessageBox.critical(self, "Error", "Ocurrió un error inesperado.", QMessageBox.Ok)
    
    def update_laptop_loan(self):
        """Actualiza un préstamo de laptop existente."""
        try:
            loan_data = self._get_laptop_loan_form_data()
            if not self._validate_loan_data(loan_data):
                return

            if not VerifyConnection.verify_connection(self):
                QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)
                return

            # No es necesario validar de nuevo al profesor si ya existe el préstamo.
            updated_loan = Loan(**loan_data)
            if self._loan_dao.update_loan(updated_loan):
                 #Si cambiamos el estado a "Devuelto", liberar la laptop.
                if updated_loan.get_status() == "Devuelto":
                    self._laptop_dao.update_laptop_status(updated_loan.get_item_id(), "Disponible")
                QMessageBox.information(self, "Confirmación", "Préstamo de laptop actualizado exitosamente.", QMessageBox.Ok)
                self.clear_laptop_loan_fields()
                self.load_laptop_loans_to_table()
            else:
                QMessageBox.critical(self, "Error", "Error al actualizar el préstamo de laptop.", QMessageBox.Ok)

        except Exception as e:
            print(f"Error al actualizar préstamo de laptop: {e}")
            QMessageBox.critical(self, "Error", "Ocurrió un error inesperado.", QMessageBox.Ok)
    
    def delete_book_loan(self):
        """Elimina un préstamo de libro."""
        selected_row = self.ui.table_loans.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Selecciona un préstamo de libro para eliminar.")
            return

        loan_id = self.ui.table_loans.item(selected_row, 0).text()

        confirm = QMessageBox.question(self, "Confirmar", f"¿Estás seguro de eliminar el préstamo de libro con ID '{loan_id}'?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                if not VerifyConnection.verify_connection(self):
                    QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)
                    return

                if self._loan_dao.delete_loan(loan_id):
                    QMessageBox.information(self, "Confirmación", "Préstamo de libro eliminado exitosamente.", QMessageBox.Ok)
                    self.load_loans_to_table()
                else:
                    QMessageBox.critical(self, "Error", "Error al eliminar el préstamo de libro.", QMessageBox.Ok)

            except Exception as e:
                print(f"Error al eliminar préstamo de libro: {e}")
                QMessageBox.critical(self, "Error", "Ocurrió un error inesperado.", QMessageBox.Ok)
    
    def delete_laptop_loan(self):
        """Elimina un préstamo de laptop."""
        selected_row = self.ui.table_laptops.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Selecciona un préstamo de laptop para eliminar.")
            return

        loan_id = self.ui.table_laptops.item(selected_row, 0).text()
        confirm = QMessageBox.question(self, "Confirmar", f"¿Estás seguro de eliminar el préstamo de laptop con ID '{loan_id}'?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                if not VerifyConnection.verify_connection(self):
                    QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)
                    return
                
                # Obtener el ID de la laptop antes de eliminar el préstamo
                loan = self._loan_dao.get_loan_by_id(loan_id)
                if not loan:
                    QMessageBox.critical(self, "Error", "Préstamo no encontrado.", QMessageBox.Ok)
                    return
                laptop_id = loan.get_item_id()


                if self._loan_dao.delete_loan(loan_id):
                    # Establecer el estado de la laptop como disponible al eliminar el préstamo.
                    self._laptop_dao.update_laptop_status(laptop_id, "Disponible")  # Usar el laptop_id obtenido
                    QMessageBox.information(self, "Confirmación", "Préstamo de laptop eliminado exitosamente.", QMessageBox.Ok)
                    self.load_laptop_loans_to_table()
                else:
                    QMessageBox.critical(self, "Error", "Error al eliminar el préstamo de laptop.", QMessageBox.Ok)


            except Exception as e:
                print(f"Error al eliminar préstamo de laptop: {e}")
                QMessageBox.critical(self, "Error", "Ocurrió un error inesperado.", QMessageBox.Ok)
                
    def search_book_loans(self):
        """Busca préstamos de libros por ID de préstamo."""
        try:
            if not VerifyConnection.verify_connection(self):
                QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)
                return

            loan_id = self.ui.txt_loan_id.text().strip()
            if not loan_id:
                QMessageBox.warning(self, "Error", "Ingrese un ID de préstamo para buscar.")
                return

            results = self._loan_dao.search_loans(loan_id)  # Pass only the loan_id
            self.ui.table_loans.setRowCount(0)
            for loan in results:
                if loan.get_item_type() == "book": #Important, show only book loans
                    row = self.ui.table_loans.rowCount()
                    self.ui.table_loans.insertRow(row)
                    self.ui.table_loans.setItem(row, 0, QTableWidgetItem(loan.get_loan_id()))
                    self.ui.table_loans.setItem(row, 1, QTableWidgetItem(loan.get_user_id()))
                    self.ui.table_loans.setItem(row, 2, QTableWidgetItem(loan.get_item_id()))
                    self.ui.table_loans.setItem(row, 3, QTableWidgetItem(loan.get_start_date()))
                    self.ui.table_loans.setItem(row, 4, QTableWidgetItem(loan.get_end_date()))
                    self.ui.table_loans.setItem(row, 5, QTableWidgetItem(loan.get_status()))

        except Exception as e:
            print(f"Error en la búsqueda de préstamos de libros: {e}")
            QMessageBox.critical(self, "Error", "Ocurrió un error en la búsqueda.", QMessageBox.Ok)

    def search_laptop_loans(self):
        """Busca préstamos de laptops por ID de préstamo."""
        try:
            if not VerifyConnection.verify_connection(self):
                QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)
                return

            loan_id = self.ui.txt_laptop_loan_id.text().strip()
            if not loan_id:
                QMessageBox.warning(self, "Error", "Ingrese un ID de préstamo para buscar.")
                return

            results = self._loan_dao.search_loans(loan_id)  # Pass only the loan_id
            self.ui.table_laptops.setRowCount(0)
            for loan in results:
                if loan.get_item_type() == "laptop": #Important. show only laptop loans
                    row = self.ui.table_laptops.rowCount()
                    self.ui.table_laptops.insertRow(row)
                    self.ui.table_laptops.setItem(row, 0, QTableWidgetItem(loan.get_loan_id()))
                    self.ui.table_laptops.setItem(row, 1, QTableWidgetItem(loan.get_user_id()))
                    self.ui.table_laptops.setItem(row, 2, QTableWidgetItem(loan.get_item_id()))
                    self.ui.table_laptops.setItem(row, 3, QTableWidgetItem(loan.get_start_date()))
                    self.ui.table_laptops.setItem(row, 4, QTableWidgetItem(loan.get_end_date()))
                    self.ui.table_laptops.setItem(row, 5, QTableWidgetItem(loan.get_status()))

        except Exception as e:
            print(f"Error en la búsqueda de préstamos de laptops: {e}")
            QMessageBox.critical(self, "Error", "Ocurrió un error en la búsqueda.", QMessageBox.Ok)

    def filter_book_loans(self):
        """Filtra los préstamos de libros en la tabla según el estado seleccionado."""
        selected_status = self.ui.cmb_loan_filter.currentText()

        try:
            if not VerifyConnection.verify_connection(self):
                QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)
                return

            loans = self._loan_dao.get_all_loans()
            filtered_loans = []

            for loan in loans:
                if loan.get_item_type() != "book":
                    continue  # Skip non-book loans

                if selected_status == "Todos":
                    filtered_loans.append(loan)
                elif selected_status == "Activos":
                    if loan.get_status() == "Activo" :
                        filtered_loans.append(loan)
                elif selected_status == "Vencidos":
                    # Compare end_date (string) with today's date (string)
                    if loan.get_status() == "Vencido":
                        filtered_loans.append(loan)
                elif selected_status == "Devueltos":
                    if loan.get_status() == "Devuelto":
                        filtered_loans.append(loan)


            self.ui.table_loans.setRowCount(0)
            for loan in filtered_loans:
                row = self.ui.table_loans.rowCount()
                self.ui.table_loans.insertRow(row)
                self.ui.table_loans.setItem(row, 0, QTableWidgetItem(loan.get_loan_id()))
                self.ui.table_loans.setItem(row, 1, QTableWidgetItem(loan.get_user_id()))
                self.ui.table_loans.setItem(row, 2, QTableWidgetItem(loan.get_item_id()))
                self.ui.table_loans.setItem(row, 3, QTableWidgetItem(loan.get_start_date()))
                self.ui.table_loans.setItem(row, 4, QTableWidgetItem(loan.get_end_date()))
                self.ui.table_loans.setItem(row, 5, QTableWidgetItem(loan.get_status()))

        except Exception as e:
            print(f"Error al filtrar préstamos de libros: {e}")
            QMessageBox.critical(self, "Error", "Error al filtrar préstamos.", QMessageBox.Ok)

    def filter_laptop_loans(self):
        """Filtra los préstamos de laptops en la tabla según el estado seleccionado."""
        selected_status = self.ui.cmb_laptop_filter.currentText()

        try:
            if not VerifyConnection.verify_connection(self):
                QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)
                return

            loans = self._loan_dao.get_all_loans()
            filtered_loans = []

            for loan in loans:
                if loan.get_item_type() != "laptop":
                    continue  # Skip non-laptop loans

                if selected_status == "Todos":
                    filtered_loans.append(loan)
                elif selected_status == "Activos":
                    if loan.get_status() == "Activo" :
                        filtered_loans.append(loan)
                elif selected_status == "Vencidos":
                    # Compare end_date (string) with today's date (string)
                    if loan.get_status() == "Vencido":
                        filtered_loans.append(loan)

                elif selected_status == "Devueltos":
                    if loan.get_status() == "Devuelto":
                        filtered_loans.append(loan)

            self.ui.table_laptops.setRowCount(0)
            for loan in filtered_loans:
                row = self.ui.table_laptops.rowCount()
                self.ui.table_laptops.insertRow(row)
                self.ui.table_laptops.setItem(row, 0, QTableWidgetItem(loan.get_loan_id()))
                self.ui.table_laptops.setItem(row, 1, QTableWidgetItem(loan.get_user_id()))
                self.ui.table_laptops.setItem(row, 2, QTableWidgetItem(loan.get_item_id()))
                self.ui.table_laptops.setItem(row, 3, QTableWidgetItem(loan.get_start_date()))
                self.ui.table_laptops.setItem(row, 4, QTableWidgetItem(loan.get_end_date()))
                self.ui.table_laptops.setItem(row, 5, QTableWidgetItem(loan.get_status()))

        except Exception as e:
            print(f"Error al filtrar préstamos de laptops: {e}")
            QMessageBox.critical(self, "Error", "Error al filtrar préstamos.", QMessageBox.Ok)
    
    def clear_book_loan_fields(self):
        """Limpia los campos del formulario de préstamos de libros."""
        self.ui.txt_loan_id.clear()
        self.ui.txt_user_id_loan.clear()
        self.ui.txt_book_id_loan.clear()
        today = QDate.currentDate()
        self.ui.date_start.setDate(today)
        self.ui.date_end.setDate(today.addDays(14))  # Valor por defecto
        self.ui.cmb_status_loan.setCurrentIndex(0)  # "Activo" por defecto

    def clear_laptop_loan_fields(self):
        """Limpia los campos del formulario de préstamos de laptops."""
        self.ui.txt_laptop_loan_id.clear()
        self.ui.txt_user_id_laptop.clear()
        self.ui.txt_laptop_id.clear()
        today = QDate.currentDate()
        self.ui.date_start_laptop.setDate(today)
        self.ui.date_end_laptop.setDate(today.addDays(14))  # Valor por defecto
        self.ui.cmb_status_laptop.setCurrentIndex(0)  # "Activo" por defecto

    def showEvent(self, event):
        """Sobreescribimos showEvent para cargar los prestamos al mostrar el diálogo."""
        super().showEvent(event)
        self.load_loans_to_table()
        self.load_laptop_loans_to_table()
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp, Qt
from view.ui_laptopmanager import Ui_LaptopManagerDialog  # Importa la UI generada
from model.DAO.LaptopDAO import LaptopDAO
from model.Objects.Laptop import Laptop
from dbConnection.VerifyConnection import VerifyConnection


class LaptopController(QDialog):
    def __init__(self, database):
        super().__init__()
        self.ui = Ui_LaptopManagerDialog()
        self.ui.setupUi(self)
        self._laptop_dao = LaptopDAO(database)
        self.initializeGUI()
        self.load_laptops_to_table()

    def initializeGUI(self):
        self.ui.btn_add.clicked.connect(self.add_laptop)
        self.ui.btn_update.clicked.connect(self.update_laptop)
        self.ui.btn_delete.clicked.connect(self.delete_laptop)
        self.ui.btn_search.clicked.connect(self.search_laptop)
        self.ui.table_laptops.itemDoubleClicked.connect(self.load_laptop_to_edit)
        self.ui.cmb_laptop_filter.currentIndexChanged.connect(self.filter_laptops)

        # Validadores (ejemplo, ajusta según tus necesidades)
        self.ui.txt_laptop_id.setValidator(QRegExpValidator(QRegExp("[A-Za-z0-9-]+"), self))  # Alfanumérico + guiones
        self.ui.txt_brand.setValidator(QRegExpValidator(QRegExp("[A-Za-z\\s]+"), self))  # Letras y espacios
        self.ui.txt_model.setValidator(QRegExpValidator(QRegExp("[A-Za-z0-9\\s\\.\\-]+"), self))  # Alfanumérico, espacios, puntos, guiones
        self.ui.txt_serial_number.setValidator(QRegExpValidator(QRegExp("[A-Za-z0-9\\-]+"), self))

    def _get_form_data(self):
        return {
            "laptop_id": self.ui.txt_laptop_id.text(),
            "brand": self.ui.txt_brand.text(),
            "model": self.ui.txt_model.text(),
            "serial_number": self.ui.txt_serial_number.text(),
            "status": self.ui.cmb_status.currentText(),
        }

    def _validate_form_data(self, laptop_data):
      #Agregar validaciones, en caso de que el id ya exista.
        if not all(laptop_data.values()):
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return False
        return True
    
    def load_laptops_to_table(self):
        try:
            if not VerifyConnection.verify_connection(self):
                QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)
                return

            laptops = self._laptop_dao.get_all_laptops()
            self.ui.table_laptops.setRowCount(0)
            for laptop in laptops:
                row = self.ui.table_laptops.rowCount()
                self.ui.table_laptops.insertRow(row)
                self.ui.table_laptops.setItem(row, 0, QTableWidgetItem(laptop.get_laptop_id()))
                self.ui.table_laptops.setItem(row, 1, QTableWidgetItem(laptop.get_brand()))
                self.ui.table_laptops.setItem(row, 2, QTableWidgetItem(laptop.get_model()))
                self.ui.table_laptops.setItem(row, 3, QTableWidgetItem(laptop.get_serial_number()))
                self.ui.table_laptops.setItem(row, 4, QTableWidgetItem(laptop.get_status()))
        except Exception as e:
            print(f"Error al cargar laptops: {e}")
            QMessageBox.critical(self, "Error", "Error al cargar laptops.", QMessageBox.Ok)

    def add_laptop(self):
        try:
            laptop_data = self._get_form_data()
            if not self._validate_form_data(laptop_data):
                return
            
            if not VerifyConnection.verify_connection(self):
                QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)
                return
            
            if self._laptop_dao.laptop_exists(laptop_data["laptop_id"]):
                QMessageBox.warning(self, "Error", "Ya existe una laptop con ese ID.", QMessageBox.Ok)
                return

            new_laptop = Laptop(**laptop_data)
            if self._laptop_dao.add_laptop(new_laptop):
                QMessageBox.information(self, "Confirmación", "Laptop agregada exitosamente.", QMessageBox.Ok)
                self.clear_fields()
                self.load_laptops_to_table()
            else:
                QMessageBox.critical(self, "Error", "Error al agregar la laptop.", QMessageBox.Ok)
        except Exception as e:
            print(f"Error al agregar laptop: {e}")
            QMessageBox.critical(self, "Error", "Ocurrió un error inesperado.", QMessageBox.Ok)

    def load_laptop_to_edit(self, item):
        row = item.row()
        laptop_id = self.ui.table_laptops.item(row, 0).text()

        if not VerifyConnection.verify_connection(self):
            QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)
            return

        laptop = self._laptop_dao.get_laptop_by_id(laptop_id)
        if laptop:
            self.ui.txt_laptop_id.setText(laptop.get_laptop_id())
            self.ui.txt_laptop_id.setEnabled(False) # Deshabilitar edicion
            self.ui.txt_brand.setText(laptop.get_brand())
            self.ui.txt_model.setText(laptop.get_model())
            self.ui.txt_serial_number.setText(laptop.get_serial_number())
            self.ui.cmb_status.setCurrentText(laptop.get_status())

    def update_laptop(self):
        try:
            laptop_data = self._get_form_data()
            if not self._validate_form_data(laptop_data):
                return

            if not VerifyConnection.verify_connection(self):
                QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)
                return

            updated_laptop = Laptop(**laptop_data)
            if self._laptop_dao.update_laptop(updated_laptop):
                QMessageBox.information(self, "Confirmación", "Laptop actualizada exitosamente.", QMessageBox.Ok)
                self.clear_fields()
                self.load_laptops_to_table()
                self.ui.txt_laptop_id.setEnabled(True) #Habilitar campo
            else:
                QMessageBox.critical(self, "Error", "Error al actualizar la laptop.", QMessageBox.Ok)
        except Exception as e:
            print(f"Error al actualizar laptop: {e}")
            QMessageBox.critical(self, "Error", "Ocurrió un error inesperado.", QMessageBox.Ok)

    def delete_laptop(self):
        selected_row = self.ui.table_laptops.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Selecciona una laptop para eliminar.")
            return

        laptop_id = self.ui.table_laptops.item(selected_row, 0).text()
        confirm = QMessageBox.question(self, "Confirmar", f"¿Estás seguro de eliminar la laptop con ID '{laptop_id}'?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                if not VerifyConnection.verify_connection(self):
                    QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)
                    return

                if self._laptop_dao.delete_laptop(laptop_id):
                    QMessageBox.information(self, "Confirmación", "Laptop eliminada exitosamente.", QMessageBox.Ok)
                    self.load_laptops_to_table()
                else:
                    QMessageBox.critical(self, "Error", "Error al eliminar la laptop.", QMessageBox.Ok)
            except Exception as e:
                print(f"Error al eliminar laptop: {e}")
                QMessageBox.critical(self, "Error", "Ocurrió un error inesperado.", QMessageBox.Ok)
    
    def search_laptop(self):
        try:
            if not VerifyConnection.verify_connection(self):
                QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)
                return
            search_criteria = {}
            if self.ui.txt_laptop_id.text().strip():
                search_criteria["laptop_id"] = self.ui.txt_laptop_id.text().strip()
            if self.ui.txt_brand.text().strip():
                search_criteria["brand"] = self.ui.txt_brand.text().strip()
            if self.ui.txt_model.text().strip():
                search_criteria["model"] = self.ui.txt_model.text().strip()
            if self.ui.txt_serial_number.text().strip():
                search_criteria["serial_number"] = self.ui.txt_serial_number.text().strip()
            if self.ui.cmb_status.currentText() != "Todas":
                search_criteria["status"] = self.ui.cmb_status.currentText()
            
            if not search_criteria: #Si no hay criterios, mostrar todas.
                self.load_laptops_to_table()
                return

            results = self._laptop_dao.search_laptops(search_criteria)
            self.ui.table_laptops.setRowCount(0)
            for laptop in results:
                row = self.ui.table_laptops.rowCount()
                self.ui.table_laptops.insertRow(row)
                self.ui.table_laptops.setItem(row, 0, QTableWidgetItem(laptop.get_laptop_id()))
                self.ui.table_laptops.setItem(row, 1, QTableWidgetItem(laptop.get_brand()))
                self.ui.table_laptops.setItem(row, 2, QTableWidgetItem(laptop.get_model()))
                self.ui.table_laptops.setItem(row, 3, QTableWidgetItem(laptop.get_serial_number()))
                self.ui.table_laptops.setItem(row, 4, QTableWidgetItem(laptop.get_status()))
        except Exception as e:
            print(f"Error en la búsqueda: {e}")
            QMessageBox.critical(self, "Error", "Ocurrió un error en la búsqueda.", QMessageBox.Ok)

    def filter_laptops(self):
        selected_status = self.ui.cmb_laptop_filter.currentText()
        if selected_status == "Todas":
            self.load_laptops_to_table()
            return

        try:
            if not VerifyConnection.verify_connection(self):
                QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)
                return
            
            laptops = self._laptop_dao.get_all_laptops()
            filtered_laptops = [laptop for laptop in laptops if laptop.get_status() == selected_status]
            self.ui.table_laptops.setRowCount(0)
            for laptop in filtered_laptops:
                row = self.ui.table_laptops.rowCount()
                self.ui.table_laptops.insertRow(row)
                self.ui.table_laptops.setItem(row, 0, QTableWidgetItem(laptop.get_laptop_id()))
                self.ui.table_laptops.setItem(row, 1, QTableWidgetItem(laptop.get_brand()))
                self.ui.table_laptops.setItem(row, 2, QTableWidgetItem(laptop.get_model()))
                self.ui.table_laptops.setItem(row, 3, QTableWidgetItem(laptop.get_serial_number()))
                self.ui.table_laptops.setItem(row, 4, QTableWidgetItem(laptop.get_status()))
        except Exception as e:
            print(f"Error al filtrar laptops: {e}")
            QMessageBox.critical(self, "Error", "Error al filtrar laptops.", QMessageBox.Ok)

    def clear_fields(self):
        self.ui.txt_laptop_id.clear()
        self.ui.txt_brand.clear()
        self.ui.txt_model.clear()
        self.ui.txt_serial_number.clear()
        self.ui.cmb_status.setCurrentIndex(0)  # Restablecer a "Disponible"
        self.ui.txt_laptop_id.setEnabled(True) # Asegurar que se habilite

    def showEvent(self, event):
        super().showEvent(event)
        self.load_laptops_to_table()
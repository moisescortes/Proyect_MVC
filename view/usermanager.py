from PyQt5 import QtWidgets, QtCore
from view.ui_usermanager import Ui_UserManager  #  Asegúrate de que este nombre sea correcto
from model.Objects.User import User
from model.Objects.Student import Student
from model.Objects.Professor import Professor
from model.Objects.Admin import Admin


class UserManagerView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_UserManager()
        self.ui.setupUi(self)
        self.setup_connections()
        self.hide_role_fields()  # Ocultar campos de rol al inicio

    def setup_connections(self):
        self.ui.btn_add.clicked.connect(self.add_user_clicked)
        self.ui.btn_search.clicked.connect(self.search_user_clicked)
        self.ui.btn_update.clicked.connect(self.update_user_clicked)
        self.ui.btn_delete.clicked.connect(self.delete_user_clicked)
        self.ui.cmb_role.currentIndexChanged.connect(self.show_role_fields)
        self.ui.cmb_role_filter.currentIndexChanged.connect(self.filter_table)
        self.ui.table_users.itemSelectionChanged.connect(self.load_selected_user)


    def get_form_data(self):
        """Obtiene los datos del formulario, incluyendo los campos específicos del rol."""
        role = self.ui.cmb_role.currentText()
        user_id = self.ui.txt_user_id.text()
        name = self.ui.txt_name.text()
        email = self.ui.txt_email.text()
    
        data = {
            "role": role,
            "user_id": user_id,
            "name": name,
            "email": email,
        }
    
        if role == "Estudiante":
            data["major"] = self.ui.txt_major.text()
        elif role == "Profesor":
            data["department"] = self.ui.txt_department.text()
        elif role == "Administrador":
            data["admin_level"] = self.ui.spin_admin_level.value()
    
        return data

    def clear_form(self):
        """Limpia todos los campos del formulario."""
        self.ui.txt_user_id.clear()
        self.ui.txt_name.clear()
        self.ui.txt_email.clear()
        self.ui.txt_major.clear()
        self.ui.txt_department.clear()
        self.ui.spin_admin_level.setValue(1)
        self.ui.cmb_role.setCurrentIndex(0)  # Restablecer la selección del rol


    def show_role_fields(self):
      """Muestra u oculta los campos específicos del rol según la selección."""
      role = self.ui.cmb_role.currentText()
      self.hide_role_fields()  # Ocultar todos primero

      if role == "Estudiante":
          self.ui.student_fields.setVisible(True)
      elif role == "Profesor":
          self.ui.professor_fields.setVisible(True)
      elif role == "Administrador":
          self.ui.admin_fields.setVisible(True)

    def hide_role_fields(self):
        """Oculta todos los campos específicos del rol."""
        self.ui.student_fields.setVisible(False)
        self.ui.professor_fields.setVisible(False)
        self.ui.admin_fields.setVisible(False)

    def update_table(self, users):
        """Actualiza la tabla de usuarios."""
        self.ui.table_users.clearContents()
        self.ui.table_users.setRowCount(0)

        for row_number, user in enumerate(users):
            self.ui.table_users.insertRow(row_number)
            self.ui.table_users.setItem(row_number, 0, QtWidgets.QTableWidgetItem(user.get_user_id()))
            self.ui.table_users.setItem(row_number, 1, QtWidgets.QTableWidgetItem(user.get_name()))
            self.ui.table_users.setItem(row_number, 2, QtWidgets.QTableWidgetItem(user.get_email()))
            self.ui.table_users.setItem(row_number, 3, QtWidgets.QTableWidgetItem(user.get_role()))

            # Añadir campos adicionales si existen
            if user.get_role() == "Estudiante":
                self.ui.table_users.setItem(row_number, 4, QtWidgets.QTableWidgetItem(user.get_major()))
            elif user.get_role() == "Profesor":
                self.ui.table_users.setItem(row_number, 4, QtWidgets.QTableWidgetItem(user.get_department()))
            elif user.get_role() == "Administrador":
                self.ui.table_users.setItem(row_number, 4, QtWidgets.QTableWidgetItem(str(user.get_admin_level())))


    def show_message(self, title, message, icon=QtWidgets.QMessageBox.Information):
        """Muestra un mensaje al usuario."""
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

    def filter_table(self):
        """Emite una señal para filtrar la tabla (se conecta al controlador)."""
        pass  # Se conecta al controlador
    def load_selected_user(self):
        """Carga los datos del libro seleccionado en los campos de texto."""
        pass

    # --- Señales para el controlador ---
    def add_user_clicked(self):
        pass

    def search_user_clicked(self):
        pass

    def update_user_clicked(self):
        pass

    def delete_user_clicked(self):
        pass
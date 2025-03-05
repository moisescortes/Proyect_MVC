from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp, Qt

# Importa tus clases de la UI y de modelo
from view.ui_usermanager import Ui_UserManagerDialog  # Cambia esto por el nombre correcto de tu archivo .ui
from model.DAO.UserDAO import UserDAO
from model.Objects.User import User
from model.Objects.Student import Student
from model.Objects.Professor import Professor
from model.Objects.Admin import Admin
from dbConnection.VerifyConnection import VerifyConnection  # Asumo que tienes esto


class UserController(QDialog):  # Hereda de QDialog
    def __init__(self, database):
        super().__init__()
        self.ui = Ui_UserManagerDialog()  # Usa el nombre de la clase generada por tu .ui
        self.ui.setupUi(self)
        self._user_dao = UserDAO(database)
        self.initializeGUI()
        self.load_users_to_table()

    def initializeGUI(self):
        self.ui.btn_add.clicked.connect(self.addUser)
        self.ui.btn_update.clicked.connect(self.updateUser)
        self.ui.btn_delete.clicked.connect(self.deleteUser)
        self.ui.btn_search.clicked.connect(self.searchUser)
        self.ui.cmb_role.currentIndexChanged.connect(self.toggle_role_fields)
        self.ui.cmb_role_filter.currentIndexChanged.connect(self.filter_by_role)

        # Validadores
        self.ui.txt_user_id.setValidator(QRegExpValidator(QRegExp("[0-9]+"), self))
        self.ui.txt_name.setValidator(QRegExpValidator(QRegExp("[a-zA-Z\\s]+"), self))
        self.ui.txt_email.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}"), self))
        self.ui.txt_major.setValidator(QRegExpValidator(QRegExp("[a-zA-Z\\s]+"), self))  # Para student
        self.ui.txt_department.setValidator(QRegExpValidator(QRegExp("[a-zA-Z\\s]+"), self))  # Para professor

        self.ui.table_users.itemDoubleClicked.connect(self.load_user_to_edit)
        self.toggle_role_fields(0) #Para establecer el rol por defecto.

    def _get_form_data(self):
        """Obtiene los datos del formulario, incluyendo los campos específicos del rol."""
        role = self.ui.cmb_role.currentText()
        data = {
            "user_id": self.ui.txt_user_id.text(),
            "name": self.ui.txt_name.text(),
            "email": self.ui.txt_email.text(),
            "user_type": role.lower(), 
        }
        if role == "Estudiante":
            data["career"] = self.ui.txt_major.text()
        elif role == "Profesor":
            data["department"] = self.ui.txt_department.text()
        elif role == "Administrador":
            pass  # No es necesario agregar campos adicionales
        return data

    def _validate_form_data(self, user_data):
        """Valida los datos del formulario."""
        if not user_data["user_id"] or not user_data["name"] or not user_data["email"]:
            QMessageBox.warning(self, "Error", "ID, Nombre y Correo son obligatorios.")
            return False

        # Aquí podrías agregar más validaciones (ej. formato de correo)
        return True

    def load_users_to_table(self):
        """Carga todos los usuarios de la base de datos en la tabla."""
        try:
            if VerifyConnection.verify_connection(self):
                users = self._user_dao.get_all_users()
                self.ui.table_users.setRowCount(0)
                for user in users:
                    row = self.ui.table_users.rowCount()
                    self.ui.table_users.insertRow(row)
                    self.ui.table_users.setItem(row, 0, QTableWidgetItem(user.get_user_id()))
                    self.ui.table_users.setItem(row, 1, QTableWidgetItem(user.get_name()))
                    self.ui.table_users.setItem(row, 2, QTableWidgetItem(user.get_email()))  # Asumiendo un get_email()
                    # Determinar el tipo de usuario y obtener el rol/especialización.
                    if isinstance(user, Student):
                         self.ui.table_users.setItem(row, 3, QTableWidgetItem("Estudiante"))
                    elif isinstance(user, Professor):
                         self.ui.table_users.setItem(row, 3, QTableWidgetItem("Profesor"))
                    elif isinstance(user, Admin):
                         self.ui.table_users.setItem(row, 3, QTableWidgetItem("Administrador"))
                    else:
                        self.ui.table_users.setItem(row, 3, QTableWidgetItem(user.get_user_type()))

            else:
                QMessageBox.critical(self, "Error", "No Internet connection.", QMessageBox.Ok)
        except Exception as e:
            print(f"❌ Error al cargar usuarios: {e}")
            QMessageBox.critical(self, "Error", "Error al cargar usuarios.", QMessageBox.Ok)

    def addUser(self):
        """Agrega un nuevo usuario a la base de datos."""
        try:
            user_data = self._get_form_data()
            if not self._validate_form_data(user_data):
                return

            if VerifyConnection.verify_connection(self):
                if self._user_dao.user_exists(user_data["user_id"]):
                    QMessageBox.warning(self, "Error", "Ya existe un usuario con ese ID.", QMessageBox.Ok)
                    return

                # Crear la instancia correcta según el tipo de usuario
                if user_data["user_type"] == "student":
                    new_user = Student(user_data["user_id"], user_data["name"], user_data["email"], user_data["career"])
                elif user_data["user_type"] == "professor":
                    new_user = Professor(user_data["user_id"], user_data["name"], user_data["email"], user_data["department"])
                elif user_data["user_type"] == "admin":
                    new_user = Admin(user_data["user_id"], user_data["name"], user_data["email"], user_data["level"])
                else:
                    new_user = User(user_data["user_id"], user_data["name"], user_data["email"], user_data["user_type"])

                if self._user_dao.add_user(new_user):
                    QMessageBox.information(self, 'Confirmation', "Usuario agregado exitosamente ✔", QMessageBox.Ok)
                    self.clearFields()
                    self.load_users_to_table()
                else:
                    QMessageBox.critical(self, "Error", "Error al agregar el usuario.", QMessageBox.Ok)
            else:
                QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)

        except Exception as e:
            print(f"❌ Error : {e}")
            QMessageBox.critical(self, "Error", "Ocurrió un error inesperado.", QMessageBox.Ok)
            
    def filter_by_role(self):
        """Filtra los usuarios en la tabla según el rol seleccionado en cmb_role_filter."""
        selected_role = self.ui.cmb_role_filter.currentText()
        if selected_role == "Todos":
            self.load_users_to_table()
            return

        try:
            if VerifyConnection.verify_connection(self):
                users = self._user_dao.get_all_users()
                filtered_users = [user for user in users if user.get_user_type().lower() == selected_role.lower()]

                self.ui.table_users.setRowCount(0)
                for user in filtered_users:
                    row = self.ui.table_users.rowCount()
                    self.ui.table_users.insertRow(row)
                    self.ui.table_users.setItem(row, 0, QTableWidgetItem(user.get_user_id()))
                    self.ui.table_users.setItem(row, 1, QTableWidgetItem(user.get_name()))
                    self.ui.table_users.setItem(row, 2, QTableWidgetItem(user.get_email()))

                    if isinstance(user, Student):
                        self.ui.table_users.setItem(row, 3, QTableWidgetItem("Estudiante"))
                    elif isinstance(user, Professor):
                        self.ui.table_users.setItem(row, 3, QTableWidgetItem("Profesor"))
                    elif isinstance(user, Admin):
                        self.ui.table_users.setItem(row, 3, QTableWidgetItem("Administrador"))
                    else:
                        self.ui.table_users.setItem(row, 3, QTableWidgetItem(user.get_user_type()))
            else:
                QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)
        except Exception as e:
            print(f"❌ Error al filtrar usuarios: {e}")
            QMessageBox.critical(self, "Error", "Error al filtrar usuarios.", QMessageBox.Ok)
    
    def load_user_to_edit(self, item):
        """Carga los datos del usuario seleccionado en el formulario para editarlo."""
        row = item.row()
        user_id = self.ui.table_users.item(row, 0).text()

        if VerifyConnection.verify_connection(self):
            user = self._user_dao.get_user_by_id(user_id)
            if user:
                self.ui.txt_user_id.setText(user.get_user_id())
                self.ui.txt_user_id.setEnabled(False)  # Deshabilitar edición del ID
                self.ui.txt_name.setText(user.get_name())
                self.ui.txt_email.setText(user.get_email())  # Asumiendo un get_email()

                # Establecer el rol y los campos específicos
                if isinstance(user, Student):
                    self.ui.cmb_role.setCurrentText("Estudiante")
                    self.ui.txt_major.setText(user.get_career())  # Asumiendo get_career()
                elif isinstance(user, Professor):
                    self.ui.cmb_role.setCurrentText("Profesor")
                    self.ui.txt_department.setText(user.get_department())  # Asumiendo get_department()
                elif isinstance(user, Admin):
                    self.ui.cmb_role.setCurrentText("Administrador")
                    self.ui.spin_admin_level.setValue(int(user.get_level())) #Asumiendo un get_level
                else:
                    self.ui.cmb_role.setCurrentText("Usuario") #O establecer un valor por defecto.

        else:
            QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)

    def updateUser(self):
        """Actualiza un usuario existente en la base de datos."""
        try:
            user_data = self._get_form_data()
            if not self._validate_form_data(user_data):
                return

            if VerifyConnection.verify_connection(self):
                # Crear la instancia correcta según el tipo de usuario, pasando argumentos posicionales
                if user_data["user_type"] == "student":
                    updated_user = Student(user_data["user_id"], user_data["name"], user_data["email"], user_data["career"])
                elif user_data["user_type"] == "professor":
                    updated_user = Professor(user_data["user_id"], user_data["name"], user_data["email"], user_data["department"])
                elif user_data["user_type"] == "admin":
                    updated_user = Admin(user_data["user_id"], user_data["name"], user_data["email"], int(user_data["level"]))
                else:
                    updated_user = User(user_data["user_id"], user_data["name"], user_data["email"], user_data["user_type"])


                if self._user_dao.update_user(updated_user):
                    QMessageBox.information(self, 'Confirmation', "Usuario actualizado exitosamente ✔", QMessageBox.Ok)
                    self.clearFields()
                    self.load_users_to_table()
                    self.ui.txt_user_id.setEnabled(True)  # Habilitar de nuevo el campo ID
                else:
                    QMessageBox.critical(self, "Error", "Error al actualizar el usuario.", QMessageBox.Ok)
            else:
                QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)

        except Exception as e:
            print(f"❌ Error al actualizar: {e}")
            QMessageBox.critical(self, "Error", "Ocurrió un error inesperado al actualizar.", QMessageBox.Ok)

    def deleteUser(self):
        """Elimina un usuario de la base de datos."""
        selected_row = self.ui.table_users.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Selecciona un usuario para eliminar.")
            return

        user_id = self.ui.table_users.item(selected_row, 0).text()

        confirm = QMessageBox.question(self, "Confirmar", f"¿Estás seguro de eliminar el usuario con ID '{user_id}'?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                if VerifyConnection.verify_connection(self):
                    if self._user_dao.delete_user(user_id):
                         QMessageBox.information(self, "Confirmación", "Usuario eliminado exitosamente.", QMessageBox.Ok)
                         self.load_users_to_table()
                    else:
                         QMessageBox.critical(self, "Error", "Error al eliminar el usuario.", QMessageBox.Ok)
                else:
                     QMessageBox.critical(self, "Error", "No hay conexión a Internet.", QMessageBox.Ok)

            except Exception as e:
                print(f"❌ Error al eliminar: {e}")
                QMessageBox.critical(self, "Error", "Ocurrió un error inesperado al eliminar.", QMessageBox.Ok)

    def searchUser(self):
        """Busca usuarios basándose en los criterios ingresados en el formulario."""
        try:
            if not VerifyConnection.verify_connection(self):
                QMessageBox.critical(self, "Error", "No Internet connection.", QMessageBox.Ok)
                return

            search_criteria = {}
            if self.ui.txt_user_id.text().strip():
                search_criteria["user_id"] = self.ui.txt_user_id.text().strip()
            if self.ui.txt_name.text().strip():
                search_criteria["name"] = self.ui.txt_name.text().strip()
            if self.ui.txt_email.text().strip():
                search_criteria["email"] = self.ui.txt_email.text().strip()
            #No buscar por rol directamente
            #if self.ui.cmb_role.currentText() != "Todos": #Si se quiere buscar por rol
            #    search_criteria["user_type"] = self.ui.cmb_role.currentText().lower()

            if not search_criteria:
                self.load_users_to_table()
                return

            results = self._user_dao.search_users(search_criteria)
            self.ui.table_users.setRowCount(0)
            for user in results:
                row = self.ui.table_users.rowCount()
                self.ui.table_users.insertRow(row)
                self.ui.table_users.setItem(row, 0, QTableWidgetItem(user.get_user_id()))
                self.ui.table_users.setItem(row, 1, QTableWidgetItem(user.get_name()))
                self.ui.table_users.setItem(row, 2, QTableWidgetItem(user.get_email()))

                if isinstance(user, Student):
                    self.ui.table_users.setItem(row, 3, QTableWidgetItem("Estudiante"))
                elif isinstance(user, Professor):
                    self.ui.table_users.setItem(row, 3, QTableWidgetItem("Profesor"))
                elif isinstance(user, Admin):
                    self.ui.table_users.setItem(row, 3, QTableWidgetItem("Administrador"))
                else:
                    self.ui.table_users.setItem(row, 3, QTableWidgetItem(user.get_user_type()))



        except Exception as e:
            print(f"Error en la búsqueda: {e}")
            QMessageBox.critical(self, "Error", "Ocurrió un error en la búsqueda.", QMessageBox.Ok)

    def clearFields(self):
        """Limpia todos los campos de entrada en el formulario."""
        self.ui.txt_user_id.clear()
        self.ui.txt_name.clear()
        self.ui.txt_email.clear()
        self.ui.txt_major.clear()
        self.ui.txt_department.clear()
        self.ui.spin_admin_level.setValue(1)
        self.ui.cmb_role.setCurrentIndex(0)
        self.ui.txt_user_id.setEnabled(True)


    def toggle_role_fields(self, index):
        """Muestra/oculta los campos específicos del rol seleccionado."""
        role = self.ui.cmb_role.itemText(index)
        if role == "Estudiante":
            self.ui.student_fields.setVisible(True)
            self.ui.professor_fields.setVisible(False)
            self.ui.admin_fields.setVisible(False)
        elif role == "Profesor":
            self.ui.student_fields.setVisible(False)
            self.ui.professor_fields.setVisible(True)
            self.ui.admin_fields.setVisible(False)
        elif role == "Administrador":
            self.ui.student_fields.setVisible(False)
            self.ui.professor_fields.setVisible(False)
            self.ui.admin_fields.setVisible(True)
        else:
            self.ui.student_fields.setVisible(False)
            self.ui.professor_fields.setVisible(False)
            self.ui.admin_fields.setVisible(False)

    def showEvent(self, event):
        """Sobreescribimos showEvent para cargar los libros al mostrar el diálogo."""
        super().showEvent(event)  # Llama al método de la clase base
        self.load_users_to_table()
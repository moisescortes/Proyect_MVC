from model.DAO.UserDAO import UserDAO
from model.Objects.User import User
from model.Objects.Student import Student
from model.Objects.Professor import Professor
from model.Objects.Admin import Admin
from view.usermanager import UserManagerView
from PyQt5.QtWidgets import QMessageBox

class UserController:
    def __init__(self, database):
        self._database = database
        self._user_dao = UserDAO(database)
        self.view = UserManagerView()
        self.connect_signals()

    def connect_signals(self):
        """Conecta las señales de la vista a los slots del controlador."""
        self.view.ui.btn_add.clicked.connect(self.add_user)
        self.view.ui.btn_search.clicked.connect(self.search_user)
        self.view.ui.btn_update.clicked.connect(self.update_user)
        self.view.ui.btn_delete.clicked.connect(self.delete_user)
        self.view.ui.cmb_role_filter.currentIndexChanged.connect(self.filter_table)
        self.view.ui.table_users.itemSelectionChanged.connect(self.load_selected_user)


    def show_view(self):
        self.view.show()
        self.load_all_users()

    def load_all_users(self):
        """Carga todos los usuarios y los muestra en la tabla."""
        users = self._user_dao.get_all_users()
        self.view.update_table(users)

    def add_user(self):
        """Agrega un nuevo usuario."""
        data = self.view.get_form_data()
        # Validación (añade más validaciones según sea necesario)
        if not data["user_id"] or not data["name"] or not data["email"]:
            self.view.show_message("Error", "Por favor, complete todos los campos obligatorios.", icon=QMessageBox.Warning)
            return
        #Verifica que no exista
        if self._user_dao.get_user_by_id(data["user_id"]):
            self.view.show_message("Error", "Ya existe un usuario con ese ID.", icon=QMessageBox.Warning)
            return

        try:
            if data["role"] == "Estudiante":
                new_user = Student(data["user_id"], data["name"], data["email"], data["major"])
            elif data["role"] == "Profesor":
                new_user = Professor(data["user_id"], data["name"], data["email"], data["department"])
            elif data["role"] == "Administrador":
                new_user = Admin(data["user_id"], data["name"], data["email"], data["admin_level"])
            else:
                self.view.show_message("Error", "Rol de usuario inválido.", icon=QMessageBox.Warning)
                return

            if self._user_dao.add_user(new_user):
                self.view.show_message("Éxito", "Usuario agregado correctamente.")
                self.load_all_users()
                self.view.clear_form()
            else:
                self.view.show_message("Error", "No se pudo agregar el usuario.", icon=QMessageBox.Critical)
        except Exception as e:
            self.view.show_message("Error", f"Error al agregar el usuario: {e}", icon=QMessageBox.Critical)

    def search_user(self):
        """Busca un usuario por ID."""
        user_id = self.view.ui.txt_user_id.text()
        if not user_id:
            self.view.show_message("Error", "Ingrese un ID de usuario para buscar.", icon=QMessageBox.Warning)
            return
        user = self._user_dao.get_user_by_id(user_id)

        if user:
            self.view.update_table([user])
        else:
            self.view.show_message("Info", "No se encontró ningún usuario con ese ID.", icon=QMessageBox.Information)
            self.load_all_users()


    def update_user(self):
      """Actualiza un usuario existente."""
      data = self.view.get_form_data()
      if not data["user_id"] or not data["name"] or not data["email"]:
          self.view.show_message("Error", "Por favor, complete todos los campos obligatorios.", icon=QMessageBox.Warning)
          return

      #Verifica si existe
      existing_user = self._user_dao.get_user_by_id(data["user_id"])
      if not existing_user:
            self.view.show_message("Error", "No existe un usuario con ese ID.", icon=QMessageBox.Warning)
            return

      try:
          if data["role"] == "Estudiante":
              updated_user = Student(data["user_id"], data["name"], data["email"], data["major"])
          elif data["role"] == "Profesor":
              updated_user = Professor(data["user_id"], data["name"], data["email"], data["department"])
          elif data["role"] == "Administrador":
              updated_user = Admin(data["user_id"], data["name"], data["email"], data["admin_level"])
          else:
              self.view.show_message("Error", "Rol de usuario inválido.", icon=QMessageBox.Warning)
              return

          if self._user_dao.update_user(updated_user):
              self.view.show_message("Éxito", "Usuario actualizado correctamente.")
              self.load_all_users()
              self.view.clear_form()
          else:
              self.view.show_message("Error", "No se pudo actualizar el usuario.", icon=QMessageBox.Critical)
      except Exception as e:
            self.view.show_message("Error", f"Error al agregar el usuario: {e}", icon=QMessageBox.Critical)

    def delete_user(self):
        """Elimina un usuario."""
        user_id = self.view.ui.txt_user_id.text()
        if not user_id:
            self.view.show_message("Error", "Ingrese un ID de usuario para eliminar.", icon=QMessageBox.Warning)
            return

        #Verifica que el usuario exista
        existing_user = self._user_dao.get_user_by_id(user_id)
        if not existing_user:
            self.view.show_message("Error", "No existe un usuario con ese ID.", icon=QMessageBox.Warning)
            return
        if self._user_dao.delete_user(user_id):
            self.view.show_message("Éxito", "Usuario eliminado correctamente.")
            self.load_all_users()
            self.view.clear_form()

        else:
            self.view.show_message("Error", "No se pudo eliminar el usuario.", icon=QMessageBox.Critical)

    def filter_table(self):
        """Filtra la tabla de usuarios según el rol seleccionado."""
        selected_role = self.view.ui.cmb_role_filter.currentText()
        
        if selected_role == "Todos":
            self.load_all_users()
            return

        filtered_users = self._user_dao.get_users_by_role(selected_role)
        self.view.update_table(filtered_users)
        
    def load_selected_user(self):
        selected_items = self.view.ui.table_users.selectedItems()
        if not selected_items:
            return
        row = selected_items[0].row()
        user_id = self.view.ui.table_users.item(row, 0).text()
        user = self._user_dao.get_user_by_id(user_id)

        if user:
            # Limpiar los campos primero
            self.view.clear_form()

            # Llenar campos comunes
            self.view.ui.txt_user_id.setText(user.get_user_id())
            self.view.ui.txt_name.setText(user.get_name())
            self.view.ui.txt_email.setText(user.get_email())

            # Seleccionar el rol correcto y mostrar campos adicionales
            if user.get_role() == "Estudiante":
                self.view.ui.cmb_role.setCurrentText("Estudiante")
                self.view.show_role_fields()  # Asegurarse de que los campos correctos estén visibles
                self.view.ui.txt_major.setText(user.get_major())
            elif user.get_role() == "Profesor":
                self.view.ui.cmb_role.setCurrentText("Profesor")
                self.view.show_role_fields()
                self.view.ui.txt_department.setText(user.get_department())
            elif user.get_role() == "Administrador":
                self.view.ui.cmb_role.setCurrentText("Administrador")
                self.view.show_role_fields()
                self.view.ui.spin_admin_level.setValue(int(user.get_admin_level()))
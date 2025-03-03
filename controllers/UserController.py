from model.DAO.UserDAO import UserDAO
from model.Objects.User import User

class UserController:
    def __init__(self, database):
        """
        Constructor para la clase UserController.

        :param database: Objeto de conexión a la base de datos (Firebase).
        """
        self._user_dao = UserDAO(database)  # Crear una instancia de UserDAO

    def registrar_usuario(self, user_id, name, email, role):
        """
        Registra un nuevo usuario en la base de datos.

        :param user_id: Identificador único del usuario.
        :param name: Nombre del usuario.
        :param email: Correo electrónico del usuario.
        :param role: Rol del usuario ("student", "teacher", "admin").
        :return: True si se agregó correctamente, False en caso contrario.
        """
        usuario = User(user_id=user_id, name=name, email=email, role=role)
        return self._user_dao.add_user(usuario)

    def eliminar_usuario(self, user_id):
        """
        Elimina un usuario de la base de datos.

        :param user_id: Identificador único del usuario.
        :return: True si se eliminó correctamente, False en caso contrario.
        """
        return self._user_dao.delete_user(user_id)

    def actualizar_usuario(self, user_id, name=None, email=None, role=None):
        """
        Actualiza un usuario en la base de datos.

        :param user_id: Identificador único del usuario.
        :param name: Nuevo nombre del usuario (opcional).
        :param email: Nuevo correo electrónico del usuario (opcional).
        :param role: Nuevo rol del usuario (opcional).
        :return: True si se actualizó correctamente, False en caso contrario.
        """
        usuario = self._user_dao.get_user_by_id(user_id)
        if usuario:
            if name:
                usuario.set_name(name)
            if email:
                usuario.set_email(email)
            if role:
                usuario.set_role(role)
            return self._user_dao.update_user(usuario)
        return False

    def asignar_rol(self, user_id, role):
        """
        Asigna un nuevo rol a un usuario.

        :param user_id: Identificador único del usuario.
        :param role: Nuevo rol a asignar ("student", "teacher", "admin").
        :return: True si se asignó correctamente, False en caso contrario.
        """
        usuario = self._user_dao.get_user_by_id(user_id)
        if usuario:
            usuario.set_role(role)
            return self._user_dao.update_user(usuario)
        return False

    def obtener_todos_los_usuarios(self):
        """
        Obtiene todos los usuarios registrados en la base de datos.

        :return: Lista de objetos de tipo User.
        """
        return self._user_dao.get_all_users()

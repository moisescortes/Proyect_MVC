from model.Objects.User import User
from model.Objects.Student import Student
from model.Objects.Professor import Professor
from model.Objects.Admin import Admin

class UserDAO:
    def __init__(self, database):
        """
        Constructor para la clase UserDAO.

        :param database: Objeto de conexión a la base de datos (o Firebase).
        """
        self._database = database
        self._collection = "users"  # Nombre de la colección/tabla de usuarios en la base de datos

    def add_user(self, user):
        """
        Agrega un nuevo usuario a la base de datos.

        :param user: Objeto de tipo User, Student, Professor o Admin.
        :return: True si se agregó correctamente, False en caso contrario.
        """
        try:
            # Convertir el objeto User a un diccionario
            user_data = user.to_dict()
            # Agregar el usuario a la colección "users"
            self._database.child(self._collection).push(user_data)
            return True
        except Exception as e:
            print(f"Error al agregar el usuario: {e}")
            return False

    def get_user_by_id(self, user_id):
        """
        Obtiene un usuario por su ID.

        :param user_id: Identificador único del usuario.
        :return: Objeto de tipo User, Student, Professor o Admin si se encuentra, None en caso contrario.
        """
        try:
            # Buscar el usuario por su ID en la colección "users"
            users = self._database.child(self._collection).get()
            if users:
                for key, value in users.items():
                    if value["user_id"] == user_id:
                        # Crear el objeto correspondiente según el tipo de usuario
                        if value["user_type"] == "student":
                            return Student(
                                user_id=value["user_id"],
                                name=value["name"],
                                career=value["career"]
                            )
                        elif value["user_type"] == "professor":
                            return Professor(
                                user_id=value["user_id"],
                                name=value["name"],
                                department=value["department"]
                            )
                        elif value["user_type"] == "admin":
                            return Admin(
                                user_id=value["user_id"],
                                name=value["name"]
                            )
                        else:
                            return User(
                                user_id=value["user_id"],
                                name=value["name"],
                                user_type=value["user_type"]
                            )
            return None
        except Exception as e:
            print(f"Error al obtener el usuario: {e}")
            return None

    def update_user(self, user):
        """
        Actualiza un usuario en la base de datos.

        :param user: Objeto de tipo User, Student, Professor o Admin con los datos actualizados.
        :return: True si se actualizó correctamente, False en caso contrario.
        """
        try:
            # Convertir el objeto User a un diccionario
            user_data = user.to_dict()
            # Buscar el usuario por su ID en la colección "users"
            users = self._database.child(self._collection).get()
            if users:
                for key, value in users.items():
                    if value["user_id"] == user.get_user_id():
                        # Actualizar el usuario en la base de datos
                        self._database.child(self._collection).child(key).update(user_data)
                        return True
            return False
        except Exception as e:
            print(f"Error al actualizar el usuario: {e}")
            return False

    def delete_user(self, user_id):
        """
        Elimina un usuario de la base de datos.

        :param user_id: Identificador único del usuario.
        :return: True si se eliminó correctamente, False en caso contrario.
        """
        try:
            # Buscar el usuario por su ID en la colección "users"
            users = self._database.child(self._collection).get()
            if users:
                for key, value in users.items():
                    if value["user_id"] == user_id:
                        # Eliminar el usuario de la base de datos
                        self._database.child(self._collection).child(key).remove()
                        return True
            return False
        except Exception as e:
            print(f"Error al eliminar el usuario: {e}")
            return False

    def get_all_users(self):
        """
        Obtiene todos los usuarios de la base de datos.

        :return: Lista de objetos de tipo User, Student, Professor o Admin.
        """
        try:
            users_list = []
            # Obtener todos los usuarios de la colección "users"
            users = self._database.child(self._collection).get()
            if users:
                for key, value in users.items():
                    if value["user_type"] == "student":
                        user = Student(
                            user_id=value["user_id"],
                            name=value["name"],
                            career=value["career"]
                        )
                    elif value["user_type"] == "professor":
                        user = Professor(
                            user_id=value["user_id"],
                            name=value["name"],
                            department=value["department"]
                        )
                    elif value["user_type"] == "admin":
                        user = Admin(
                            user_id=value["user_id"],
                            name=value["name"]
                        )
                    else:
                        user = User(
                            user_id=value["user_id"],
                            name=value["name"],
                            user_type=value["user_type"]
                        )
                    users_list.append(user)
            return users_list
        except Exception as e:
            print(f"Error al obtener todos los usuarios: {e}")
            return []

    def get_users_by_type(self, user_type):
        """
        Obtiene todos los usuarios de un tipo específico.

        :param user_type: Tipo de usuario ("student", "professor", "admin").
        :return: Lista de objetos de tipo User, Student, Professor o Admin.
        """
        try:
            users_list = []
            # Obtener todos los usuarios de la colección "users"
            users = self._database.child(self._collection).get()
            if users:
                for key, value in users.items():
                    if value["user_type"] == user_type:
                        if user_type == "student":
                            user = Student(
                                user_id=value["user_id"],
                                name=value["name"],
                                career=value["career"]
                            )
                        elif user_type == "professor":
                            user = Professor(
                                user_id=value["user_id"],
                                name=value["name"],
                                department=value["department"]
                            )
                        elif user_type == "admin":
                            user = Admin(
                                user_id=value["user_id"],
                                name=value["name"]
                            )
                        else:
                            user = User(
                                user_id=value["user_id"],
                                name=value["name"],
                                user_type=value["user_type"]
                            )
                        users_list.append(user)
            return users_list
        except Exception as e:
            print(f"Error al obtener los usuarios por tipo: {e}")
            return []
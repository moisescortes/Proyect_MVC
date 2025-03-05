from model.Objects.User import User
from model.Objects.Student import Student
from model.Objects.Professor import Professor
from model.Objects.Admin import Admin
from google.cloud.firestore_v1.base_query import FieldFilter, And


class UserDAO:
    def __init__(self, database):
        self._database = database
        self._collection = "users"

    def add_user(self, user):
        try:
            user_data = user.to_dict()
            self._database.collection(self._collection).document(user.get_user_id()).set(user_data)
            return True
        except Exception as e:
            print(f"Error al agregar el usuario: {e}")
            return False

    def get_user_by_id(self, user_id):
        try:
            doc_ref = self._database.collection(self._collection).document(user_id)
            doc = doc_ref.get()
            if doc.exists:
                user_data = doc.to_dict()
                # Usar el user_type para crear la instancia correcta
                if user_data["user_type"] == "student":
                    return Student(user_data["user_id"], user_data["name"], user_data["email"], user_data["career"])
                elif user_data["user_type"] == "professor":
                    return Professor(user_data["user_id"], user_data["name"], user_data["email"], user_data["department"])
                elif user_data["user_type"] == "admin":
                    return Admin(user_data["user_id"], user_data["name"], user_data["email"], user_data["level"])
                else:
                    return User(user_data["user_id"], user_data["name"], user_data["email"], user_data["user_type"])
            else:
                return None
        except Exception as e:
            print(f"Error al obtener el usuario: {e}")
            return None


    def update_user(self, user):
        try:
            doc_ref = self._database.collection(self._collection).document(user.get_user_id())
            doc_ref.update(user.to_dict())
            return True
        except Exception as e:
            print(f"Error al actualizar el usuario: {e}")
            return False

    def delete_user(self, user_id):
        try:
            doc_ref = self._database.collection(self._collection).document(user_id)
            doc_ref.delete()
            return True
        except Exception as e:
            print(f"Error al eliminar el usuario: {e}")
            return False

    def get_all_users(self):
        try:
            users_list = []
            docs = self._database.collection(self._collection).stream()
            for doc in docs:
                user_data = doc.to_dict()
                if user_data["user_type"] == "student":
                    user = Student(user_data["user_id"], user_data["name"], user_data["email"], user_data["career"])
                elif user_data["user_type"] == "professor":
                    user = Professor(user_data["user_id"], user_data["name"], user_data["email"], user_data["department"])
                elif user_data["user_type"] == "admin":
                    user = Admin(user_data["user_id"], user_data["name"], user_data["email"], user_data["level"])
                else:
                    user = User(user_data["user_id"], user_data["name"], user_data["email"], user_data["user_type"])
                users_list.append(user)
            return users_list
        except Exception as e:
            print(f"Error al obtener todos los usuarios: {e}")
            return []

    def search_users(self, criteria):
        """
        Busca usuarios según los criterios proporcionados (un diccionario).
        """
        try:
            base_query = self._database.collection(self._collection)
            filters = []

            # Construir filtros para cada criterio
            for field, value in criteria.items():
                filters.append(FieldFilter(field, "==", value))

            # Combinar filtros con AND (si hay más de uno)
            if len(filters) > 1:
                combined_filter = And(*filters)
                query = base_query.where(filter=combined_filter)
            elif len(filters) == 1:
                query = base_query.where(filter=filters[0])
            else:  # No hay criterios
                return []

            docs = query.stream()
            users_list = []  # Lista para almacenar los usuarios encontrados
            for doc in docs:
                user_data = doc.to_dict()
                # Crear la instancia de usuario correcta según user_type
                if user_data["user_type"] == "student":
                    user = Student(user_data["user_id"], user_data["name"], user_data["email"], user_data["career"])
                elif user_data["user_type"] == "professor":
                    user = Professor(user_data["user_id"], user_data["name"], user_data["email"], user_data["department"])
                elif user_data["user_type"] == "admin":
                    user = Admin(user_data["user_id"], user_data["name"], user_data["email"], user_data["level"])
                else:
                    user = User(user_data["user_id"], user_data["name"], user_data["email"], user_data["user_type"])
                users_list.append(user)
            return users_list

        except Exception as e:
            print(f"Error al buscar usuarios: {e}")
            return []

    def user_exists(self, user_id):
        """
        Verifica si ya existe un usuario con el ID dado.
        """
        try:
            doc_ref = self._database.collection(self._collection).document(user_id)
            doc = doc_ref.get()
            return doc.exists
        except Exception as e:
            print(f"Error al verificar existencia: {e}")
            return False
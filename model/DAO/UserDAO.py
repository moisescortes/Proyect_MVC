from model.Objects.User import User
from model.Objects.Student import Student
from model.Objects.Professor import Professor
from model.Objects.Admin import Admin
from google.cloud.firestore_v1.base_query import FieldFilter

class UserDAO:
    def __init__(self, database):
        self._database = database
        self._collection = "users"  # Nombre de la colección en Firestore

    def add_user(self, user):
        """Agrega un nuevo usuario a Firestore."""
        try:
            user_data = user.to_dict()
            self._database.collection(self._collection).document(user.get_user_id()).set(user_data)
            return True
        except Exception as e:
            print(f"Error al agregar usuario: {e}")
            return False

    def get_user_by_id(self, user_id):
        """Obtiene un usuario por su ID."""
        try:
            doc_ref = self._database.collection(self._collection).document(user_id)
            doc = doc_ref.get()
            if doc.exists:
                return self._create_user_from_doc(doc)
            else:
                return None
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None

    def update_user(self, user):
        """Actualiza un usuario existente."""
        try:
            user_data = user.to_dict()
            self._database.collection(self._collection).document(user.get_user_id()).update(user_data)
            return True
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            return False

    def delete_user(self, user_id):
        """Elimina un usuario."""
        try:
            self._database.collection(self._collection).document(user_id).delete()
            return True
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            return False

    def get_all_users(self):
        """Obtiene todos los usuarios."""
        try:
            users = []
            docs = self._database.collection(self._collection).stream()
            for doc in docs:
                users.append(self._create_user_from_doc(doc))
            return users
        except Exception as e:
            print(f"Error al obtener todos los usuarios: {e}")
            return []
    
    def get_users_by_role(self, role):
        """Obtiene todos los usuarios filtrados por rol."""
        try:
            users = []
            query = self._database.collection(self._collection).where(filter=FieldFilter("role", "==", role)).stream()
            for doc in query:
                users.append(self._create_user_from_doc(doc))
            return users
        except Exception as e:
            print(f"Error al obtener usuarios por rol: {e}")
            return []

    def _create_user_from_doc(self, doc):
        """Crea un objeto User (o subclase) a partir de un documento de Firestore."""
        data = doc.to_dict()
        role = data.get("role")

        if role == "Estudiante":
            return Student(data["user_id"], data["name"], data["email"], data["major"])
        elif role == "Profesor":
            return Professor(data["user_id"], data["name"], data["email"], data["department"])
        elif role == "Administrador":
            return Admin(data["user_id"], data["name"], data["email"], data["admin_level"])
        else:
            return None
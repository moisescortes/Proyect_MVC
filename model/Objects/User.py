class User:
    def __init__(self, user_id, name, user_type):
        """
        Constructor para la clase User.

        :param user_id: Identificador único del usuario.
        :param name: Nombre del usuario.
        :param user_type: Tipo de usuario ("student", "professor", "admin").
        """
        self._user_id = user_id
        self._name = name
        self._user_type = user_type

    # Getters
    def get_user_id(self):
        return self._user_id

    def get_name(self):
        return self._name

    def get_user_type(self):
        return self._user_type

    # Setters
    def set_user_id(self, user_id):
        self._user_id = user_id

    def set_name(self, name):
        self._name = name

    def set_user_type(self, user_type):
        if user_type in ["student", "professor", "admin"]:
            self._user_type = user_type
        else:
            raise ValueError("Invalid user type. Use 'student', 'professor', or 'admin'.")

    # Método para representar el objeto en formato JSON para Firebase
    def to_dict(self):
        """
        Convierte el objeto User a un diccionario JSON para almacenar en Firebase.
        """
        return {
            "user_id": self._user_id,
            "name": self._name,
            "user_type": self._user_type
        }

    # Método especial para representación en string
    def __str__(self):
        return f"User(ID: {self._user_id}, Name: {self._name}, Type: {self._user_type})"
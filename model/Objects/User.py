class User:
    def __init__(self, user_id, name, email, role):
        self._user_id = user_id
        self._name = name
        self._email = email
        self._role = role

    # Getters
    def get_user_id(self):
        return self._user_id

    def get_name(self):
        return self._name

    def get_email(self):
        return self._email
    def get_role(self):
        return self._role

    # Setters (opcional, si necesitas modificar los datos)
    def set_user_id(self, user_id):
        self._user_id = user_id
    def set_name(self, name):
        self._name = name
    def set_email(self, email):
        self._email = email
    def set_role(self, role):
        self._role = role

    def to_dict(self):
        return {
            "user_id": self._user_id,
            "name": self._name,
            "email": self._email,
            "role": self._role,
        }
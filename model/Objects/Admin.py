from model.Objects.User import User

class Admin(User):
    def __init__(self, user_id, name, email, admin_level):
        super().__init__(user_id, name, email, "Administrador")
        self._admin_level = admin_level

    def get_admin_level(self):
        return self._admin_level

    def set_admin_level(self, admin_level):
        self._admin_level = admin_level

    def to_dict(self):
        user_dict = super().to_dict()
        user_dict["admin_level"] = self._admin_level
        return user_dict
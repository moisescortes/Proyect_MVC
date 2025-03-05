from model.Objects.User import User

class Admin(User):
    def __init__(self, user_id, name, email, level, user_type="admin"):
        super().__init__(user_id, name, email, user_type)
        self._level = level

    def get_level(self):
        return self._level

    def set_level(self, level):
        self._level = level

    def to_dict(self):
        user_dict = super().to_dict()
        user_dict["level"] = self._level
        return user_dict
    def __str__(self):
        return f"Admin(ID: {self.get_user_id()}, Name: {self.get_name()}, Email: {self.get_email()}, Level: {self.get_level()})"
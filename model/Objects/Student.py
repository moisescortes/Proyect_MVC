from model.Objects.User import User

class Student(User):
    def __init__(self, user_id, name, email, career, user_type="student"):
        super().__init__(user_id, name, email, user_type)
        self._career = career

    def get_career(self):
        return self._career

    def set_career(self, career):
        self._career = career

    def to_dict(self):
        user_dict = super().to_dict()
        user_dict["career"] = self._career
        return user_dict

    def __str__(self):
        return f"Student(ID: {self.get_user_id()}, Name: {self.get_name()}, Email: {self.get_email()}, Career: {self._career})"
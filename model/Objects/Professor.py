from model.Objects.User import User

class Professor(User):
    def __init__(self, user_id, name, email, department, user_type="professor"):  
        super().__init__(user_id, name, email, user_type)
        self._department = department

    def get_department(self):
        return self._department

    def set_department(self, department):
        self._department = department

    def to_dict(self):
        user_dict = super().to_dict()
        user_dict["department"] = self._department
        return user_dict
    def __str__(self):
        return f"Professor(ID: {self.get_user_id()}, Name: {self.get_name()}, Email: {self.get_email()}, Department: {self.get_department()})"
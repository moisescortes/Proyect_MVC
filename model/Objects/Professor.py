from model.Objects.User import User

class Professor(User):
    def __init__(self, user_id, name, email, department):
        super().__init__(user_id, name, email, "Profesor")
        self._department = department

    def get_department(self):
      return self._department
    
    def set_department(self, department):
        self._department = department

    def to_dict(self):
        user_dict = super().to_dict()
        user_dict["department"] = self._department
        return user_dict
from model.Objects.User import User
 
class Student(User):
    def __init__(self, user_id, name, email, major):
        super().__init__(user_id, name, email, "Estudiante")  # Llama al constructor de la clase base
        self._major = major

    def get_major(self):
        return self._major

    def set_major(self, major):
        self._major = major
    
    def to_dict(self):
        user_dict = super().to_dict()  # Obtiene el diccionario de la clase base
        user_dict["major"] = self._major  # Agrega los campos específicos de Student
        return user_dict
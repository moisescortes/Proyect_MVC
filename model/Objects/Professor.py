from model.Objects import User

class Professor(User):
    def __init__(self, user_id, name, department):
        """
        Constructor para la clase Professor.

        :param user_id: Identificador único del profesor.
        :param name: Nombre del profesor.
        :param department: Departamento al que pertenece el profesor.
        """
        super().__init__(user_id, name, "professor")  # Llama al constructor de la clase base
        self._department = department

    # Getter y Setter para department
    def get_department(self):
        return self._department

    def set_department(self, department):
        self._department = department

    # Método para representar el objeto en formato JSON para Firebase
    def to_dict(self):
        """
        Convierte el objeto Professor a un diccionario JSON para almacenar en Firebase.
        """
        user_dict = super().to_dict()  # Obtiene el diccionario de la clase base
        user_dict["department"] = self._department  # Agrega el atributo específico de Professor
        return user_dict

    # Método especial para representación en string
    def __str__(self):
        return f"Professor(ID: {self._user_id}, Name: {self._name}, Department: {self._department})"
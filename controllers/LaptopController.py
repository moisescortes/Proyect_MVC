from model.DAO.LaptopDAO import LaptopDAO
from model.Objects.Laptop import Laptop

class LaptopController:
    def __init__(self, database):
        """
        Constructor para la clase LaptopController.

        :param database: Objeto de conexión a la base de datos (Firebase).
        """
        self._laptop_dao = LaptopDAO(database)  # Crear una instancia de LaptopDAO

    def agregar_laptop(self, laptop_id, brand, model, status="available"):
        """
        Agrega una nueva laptop a la base de datos.

        :param laptop_id: Identificador único de la laptop.
        :param brand: Marca de la laptop.
        :param model: Modelo de la laptop.
        :param status: Estado de la laptop ("available" o "borrowed"), por defecto es "available".
        :return: True si se agregó correctamente, False en caso contrario.
        """
        laptop = Laptop(laptop_id=laptop_id, brand=brand, model=model, status=status)
        return self._laptop_dao.add_laptop(laptop)

    def eliminar_laptop(self, laptop_id):
        """
        Elimina una laptop de la base de datos.

        :param laptop_id: Identificador único de la laptop.
        :return: True si se eliminó correctamente, False en caso contrario.
        """
        return self._laptop_dao.delete_laptop(laptop_id)

    def actualizar_laptop(self, laptop_id, brand=None, model=None, status=None):
        """
        Actualiza los datos de una laptop en la base de datos.

        :param laptop_id: Identificador único de la laptop.
        :param brand: Nueva marca de la laptop (opcional).
        :param model: Nuevo modelo de la laptop (opcional).
        :param status: Nuevo estado de la laptop (opcional).
        :return: True si se actualizó correctamente, False en caso contrario.
        """
        laptop = self._laptop_dao.get_laptop_by_id(laptop_id)
        if laptop:
            if brand:
                laptop.set_brand(brand)
            if model:
                laptop.set_model(model)
            if status:
                laptop.set_status(status)
            return self._laptop_dao.update_laptop(laptop)
        return False

    def obtener_todas_las_laptops(self):
        """
        Obtiene todas las laptops de la base de datos.

        :return: Lista de objetos Laptop.
        """
        return self._laptop_dao.get_all_laptops()

from datetime import datetime

class Loan:
    def __init__(self, loan_id, user_id, item_id, start_date, end_date, status, item_type):
        """
        Constructor for the Loan class.

        Args:
            loan_id (str): Unique identifier for the loan.
            user_id (str): Identifier of the user making the loan.
            item_id (str): Identifier of the item being loaned (book or laptop).
            start_date (str): Loan start date in 'YYYY-MM-DD' format.
            end_date (str): Loan end date in 'YYYY-MM-DD' format.
            status (str): Status of the loan ('Activo', 'Vencido', 'Devuelto').
            item_type (str): Type of item ('book' or 'laptop').
        """
        self._loan_id = loan_id
        self._user_id = user_id
        self._item_id = item_id
        self._start_date = start_date  # Store as string
        self._end_date = end_date      # Store as string
        self._status = status
        self._item_type = item_type

    # Getters
    def get_loan_id(self):
        return self._loan_id

    def get_user_id(self):
        return self._user_id

    def get_item_id(self):
        return self._item_id

    def get_start_date(self):
        return self._start_date

    def get_end_date(self):
        return self._end_date

    def get_status(self):
        return self._status

    def get_item_type(self):
        return self._item_type

    # Setters
    def set_status(self, status):
        if status in ["Activo", "Vencido", "Devuelto"]:
            self._status = status
        else:
            raise ValueError("Invalid status. Use 'Activo', 'Vencido', or 'Devuelto'.")

    def set_end_date(self, end_date):
        self._end_date = end_date  # No strptime here

    # No need for is_expired with string dates
    def is_expired(self):
        """
        Verifies if loan is expired
        """
        end_date_obj = datetime.strptime(self._end_date, "%Y-%m-%d")
        return datetime.now() > end_date_obj
    # Firebase-compatible to_dict method
    def to_dict(self):
        """
        Converts the Loan object to a dictionary for Firebase storage.
        """
        return {
            "loan_id": self._loan_id,
            "user_id": self._user_id,
            "item_id": self._item_id,
            "start_date": self._start_date,  # Store as string
            "end_date": self._end_date,      # Store as string
            "status": self._status,
            "item_type": self._item_type,
        }

    def __str__(self):
        return (f"Loan(ID: {self._loan_id}, User ID: {self._user_id}, Item ID: {self._item_id}, "
                f"Start Date: {self._start_date}, End Date: {self._end_date}, "
                f"Status: {self._status}, Item Type: {self._item_type})")
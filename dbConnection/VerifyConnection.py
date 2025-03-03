import socket

class VerifyConnection():

    def verify_connection(self):
        try:
            socket.create_connection(("www.google.com", 80), timeout=5)
            return True  # If the connection is successful
        except OSError:
            return False  # If it cannot connect


# Use the concrete class
connection = VerifyConnection()

if connection.verify_connection():
    print("Internet connection successful ✔")
else:
    print("No Internet connection")

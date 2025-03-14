# MVC Pattern Project

## Overview
This project aims to develop your abstraction and modeling skills by analyzing a UML class diagram and implementing it using the Model-View-Controller (MVC) design pattern. The work will be done in pairs, but each student's individual performance will be assessed separately.

![UML Diagram](uml.png)

## Installation and Setup
To run the program, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/moisescortes/Proyect_MVC
   cd Proyect_MVC
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up Firebase credentials:**
   - You need a JSON file containing Firebase database credentials.
   - Place this JSON file in the project dbConnection directory.
   - Modify `dbConnection.py` to reference the correct file name.

4. **Run the application:**
   ```bash
   python MainApp.py
   ```

## Features
The program allows CRUD (Create, Read, Update, Delete) operations on:
- **Books**
- **Laptops**
- **Users**

Additionally, the system supports **loans**:
- All users can borrow books.
- Users with the "professor" role can also borrow laptops.

The provided GUI is an administrator panel, enabling full management of all operations.

## Team Members
* Sergio Emmanuel Ramírez Anaya
* Moisés Adrián Cortés Ramos

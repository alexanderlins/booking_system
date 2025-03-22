# Booking System v1.2.0
## Overview

The Reservation System is a terminal-based Python application designed to manage room reservations. It provides functionality to:

* **Create new reservations**  
* **Search for reservations**  
* **List or print out existing reservations**  
* **Remove reservations**  
* **Store reservations** (load/save) to a JSON file  
* **Authenticate users** with a secure login system backed by a SQLite database and `bcrypt` password hashing

## Features

### 1. User Authentication
User credentials are stored in a local SQLite database (`bookingsystem.db`). Passwords are hashed with **bcrypt** and salted automatically. Login attempts compare the user’s typed password (also hashed) to the stored hash in the database.

### 2. Reservation Management

- **Make a Reservation**  
  When selecting this option in the main menu, users can pick a room, set an ID for the reservation, and define start/end dates & times. The system checks for time conflicts with the same room or with the user’s other reservations to avoid overlaps.

- **Search for a Reservation**  
  A reservation can be quickly retrieved by searching its Reservation ID (binary search implementation).

- **List/Print Reservations**  
  The system can display all future reservations or filter by room. You can view them in a tabular format or a simple list. For a quick 7-day schedule, there is also a special display option that splits each day into time segments (Early Morning, Morning, Afternoon, Evening).

- **Remove a Reservation**  
  A user can remove only their own reservations by entering the corresponding Reservation ID.

- **Store Reservations to File**  
  All reservations can be loaded from or saved to a JSON file (`reservations.json`). This happens automatically when the program starts and when exiting the application (or by certain menu options). Past reservations (expired) are cleaned up upon each run.

### 3. Room Management
Room objects (e.g., Room ID, name, and whether they are reservable) are created and stored in-memory. By default, there are a handful of rooms added at launch (e.g., `R001`, `R002`, etc.), and you can create more via `ReservationHandler().add_room(...)`.

### 4. User Interface
The application runs in the terminal and presents a straightforward menu after successful login. Options include:
1. **Make Reservation**  
2. **Display Reservations**  
3. **Display 7-day Schedule**  
4. **Search**  
5. **Remove Reservation**  
6. **Exit**  

Selecting one of these leads to a function that handles the request.

## Environment and Tools

- **Programming Language**: Python 3.10+  
- **Operating Systems**: Cross-platform (Windows, Linux, macOS)  
- **Libraries/Modules**:
  - [bcrypt](https://pypi.org/project/bcrypt/) for password hashing  
  - [sqlite3](https://docs.python.org/3/library/sqlite3.html) for database integration  
  - [pytest](https://docs.pytest.org/en/stable/) for testing
- **Development Tools**:
  - Text editors or IDEs (e.g., VS Code, PyCharm)  
  - Git for version control  

## Installation

1.  Ensure Python 3.10 is installed on your system. Higher or lower might not be supported.
2.  Clone the repository: `git clone <repository-url>`
3.  Navigate to the repository directory: `cd <repository-directory>`
4.  Install the dependencies in the requirements.txt file by running `pip install -r requirements.txt`
5.  Run the application: `python booking_system.py`
6.  By running the application for the first time, it will create a new database called `bookingsystem.db`

## Usage

### Login:

*   At startup, you'll see a prompt for choosing either to log in or create a new account.
*   In case you already have an account, you can safely choose that option and write your credentials.

### Create new account

*   At startup, in case you do not have an acccount, you can choose to create a new one.
*   Type in safely the desired username and password
*   You will then be automatically logged in using that account.

### Navigation:

After successful login, the main menu displays options:

* **1 -  Make Reservation**

Choose a Room ID (e.g., R001) from the list.

Enter a unique Reservation ID of your choosing.

Provide a start date/time and duration up to 4 hours.

The system checks for conflicts with your other reservations or with existing ones in the selected room.

* **2 - Display Reservations**

Option 2 shows a table or list of all future reservations, optionally filtered by room.

* **3 - Display 7-day Schedule**

Option 3 (“Display 7-day Schedule”) shows a day-by-day, hour-block schedule for a single room over the next week.

* **4 - Search**

Option 4 lets you quickly find a reservation by typing its ID.

* **5 - Remove Reservation**

Option 5 lists existing reservations and prompts for the ID of the reservation you want to remove.

You can only remove your own reservations (based on your username).

* **X - Exit**

Selecting “X” to exit triggers a save to reservations.json and closes the application.

All in-memory reservations will be restored next time the application starts, except those that have already ended in the past.

## Code Structure

**booking_system.py**

    Main driver code, including menu logic.

    Contains classes Room, Reservation, and ReservationHandler.

    Handles JSON loading/saving of reservation data.

    Includes logic for searching, listing, sorting, and removing reservations.

**database.py**

    Sets up the SQLite database (bookingsystem.db) if it doesn’t exist.

    Contains functions to create new users, login (verifying bcrypt hashes), etc.

**test_booking_system.py**

    A basic pytest test suite to validate certain aspects of room creation, reservation creation, etc.

**requirements.txt**

    Lists Python dependencies (including bcrypt and pytest).

**README.md**

    The documentation you’re currently reading!

## Development History & Updates

v1.0.0

    Initial application structure.

    Basic login system using hashlib.

    Create/search/remove reservations functionality.

    JSON-based saving and loading of reservation data.

v1.2 (internal code version)

    Extended display capabilities (table vs. list, plus 7-day schedule).

    Sorting and conflict checks for reservations.

    Database integration.

    Safer user creation and authentication.

    Automatic cleanup of past reservations on each run.

## People Involved
### Contributors
Contributions are welcome! Please fork the repository and submit a pull request with your improvements, or open an issue to discuss any suggestions.

| Name          | Contribution         |
|---------------|----------------------|
| frst1301      | Original prototype, initial menu flow & JSON saving capabilities. |
| igli2400      | Database integration, user creation, authentication and unit testing |
| anwa2301      | Extended reservation features, visualization and testing |
| anov2400      | Conflict checks, testing, code refactoring & cleanup |

## License
This project is licensed under the MIT License.

## Acknowledgements
Special thanks to all contributors and team members whose feedback and efforts have helped shape this project.

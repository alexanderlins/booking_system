# Booking System v1.0.0
## Overview

The Reservation System is a terminal-based Python application designed to manage room reservations. It provides functionality to:

*   Make a new reservation
*   Change an existing reservation (**TODO**)
*   Print current reservations (**TODO**)
*   Search for reservations by ID
*   Remove reservations
*   Store reservations to a file (**TODO**)

The application uses a simple menu-driven interface and includes user authentication via a secure login system
using salted SHA-256 hashing.

## Features

### User Authentication

Secure login functionality that compares a salted, hashed password against stored credentials. Predefined users
such as `frst1301`, `igli2400`, and others are used for demonstration.

### Reservation Management

*   **Make Reservation**: Create a reservation by selecting a room and entering a reservation ID along with the
start and end times.
*   **Search Reservation**: Quickly find reservations by reservation ID.
*   **Remove Reservation**: Remove an existing reservation through the menu.
*   **Store to File** (**TODO**): Save reservations to a file.

### Room Management

Room objects are created at runtime and stored in an array, allowing the system to manage room availability during application runtime.

### User Interface

A terminal-based main menu guides the user through the available options. Each menu selection triggers a dedicated function that processes the user's request.

## Environment and Tools

*   **Programming Language**: Python 3.10
*   **Operating Systems**: Cross-platform support (Windows, Linux, macOS)
*   **Libraries/Modules**:
    *   Standard libraries: `os`, `platform`, `datetime`, `getpass`, `hashlib`
*   **Development Tools**:
    *   Code editors/IDEs (e.g., Visual Studio Code, PyCharm)
    *   Git for version control
    *   Terminal/Command Prompt for running the application

## Installation

1.  Ensure Python 3.10 is installed on your system. Higher or lower might not be supported.
2.  Clone the repository: `git clone <repository-url>`
3.  Navigate to the repository directory: `cd <repository-directory>`
4.  Run the application: `python booking_system.py`

## Usage

### Login:

When the application starts, it prompts for a username and password. Use one of the predefined accounts (e.g., `frst1301` or `igli2400`). The password is verified by generating a SHA-256 hash with a
unique salt.

### Navigation:

After login, the main menu displays options:

*   **Make Reservation**: Input details such as Room ID, Reservation ID, and the time interval.
*   **Change Reservation** (**TODO**)
*   **Print Reservation(s)** (**TODO**)
*   **Search**: Find reservations quickly by entering a Reservation ID.
*   **Remove Reservation**: Delete a reservation based on its Reservation ID.
*   **Store to File** (**TODO**)
*   **Exit**: Close the application. Select option 7 to exit the program.

## Code Structure

The code is structured into the following components:

*   **Main Script**: Contains the `main()` function that drives the login process and the main menu loop.
*   **Classes**:
    *   `Room`: Represents a room with attributes such as room ID, room name, and reservable status.
    *   `Reservation`: Represents a reservation with attributes such as the associated room, user ID, reservation ID, start time, and end time.
*   **Utility Functions**:
    *   `clear_terminal()`: Clears the terminal window for better menu display.
    *   `display_main_menu()`: Renders the main menu.
    *   `handle_main_menu_selection()`: Routes the user's selection to the corresponding function.

## Development History & Updates

The code has undergone several updates and enhancements, including:

*   Initial template design by frst1301
*   Addition of actual working functionality for making reservations, searching, and removing reservations
*   Conversion of intermediary functions into dedicated action methods

## People Involved
### Contributors
Contributions are welcome! Please fork the repository and submit a pull request with your improvements, or open an issue to discuss any suggestions.

| Name          | Contribution         |
|---------------|----------------------|
| frst1301      | **TODO**. |
| igli2400      | **TODO**. |
| anwa2301      | **TODO**. |
| anov2400      | **TODO**. |

## License
This project is licensed under the MIT License.

## Acknowledgements
Special thanks to all contributors and team members whose feedback and efforts have helped shape this project.
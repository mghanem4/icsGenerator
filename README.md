# ICS Generator

This project provides a graphical user interface (GUI) for creating `.ics` files, which are used to manage schedules in calendar applications like Google Calendar, Outlook, and Apple Calendar. Users can add multiple classes, check for scheduling conflicts, and export a well-structured `.ics` file with recurring events.

---

## Features

- **Add Multiple Classes**: Users can input details for multiple classes, including:
  - Class title
  - Days of the week
  - Start and end times
  - Color (optional)
  - Semester start and end dates
- **Conflict Detection**: Ensures no overlapping class times for the same day.
- **Generate `.ics` File**: Creates a calendar file with recurring events based on user inputs.
- **User-Friendly GUI**: Simple and intuitive interface built with `Tkinter`.

---

## Prerequisites

- Python 3.7 or later
- Required libraries:
  - `tkinter` (included with Python)
  - Custom module: `ics_writer.py`

---

## Project Structure

ics-generator/ ├── 
    main.py 
# Entry point for the application 
    ├── icsWriter.py # Logic for generating .ics files 
    ├── ui.py # GUI logic for the application 
    └── README.md # Project documentation
## Installation

1. Clone the repository or download the source files:
   ```bash
   git clone https://github.com/yourusername/ics-generator.git
   cd ics-generator

# Usage
To run the file:
1- 
```bash
    python main.py
```
Use the GUI to:

2- Input class details (title, days, times, color).
3- Add classes one at a time.
4- Check for conflicts between classes.
5- Specify the semester start and end dates.
6- Click "Generate .ics" to save the schedule as a .ics file.
7- Import the generated .ics file into your preferred calendar application.

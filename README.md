# File Organizer

A simple Python script that organizes files into categorized folders based on their file type. It also provides an undo feature to revert files to their original locations.

## Features
- Automatically categorizes files into folders (e.g., Documents, Images, Videos, etc.).
- Allows users to undo the organization and restore files to their original locations.
- Supports multiple file formats.

## Installation
### Prerequisites
Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Install Dependencies
Run the following command to install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage
To run the file organizer tool, follow these steps:

1. Open a terminal/command prompt in the project folder.
2. Run the script:

```bash
python file_organizer.py
```

3. Follow the on-screen prompts to select the folder you want to organize.
4. The program will automatically organize files into categories like Images, Documents, Videos, etc.
5. You can also undo the organization by clicking the "Undo" button, which will move the files back to their original locations.

## Requirements
The script requires the following Python libraries:
- `plyer==2.1.0`
- `sv-ttk==2.6.0`

These are automatically installed when running `pip install -r requirements.txt`.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

### Author
[arvo101](https://github.com/arvo101)

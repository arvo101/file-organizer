import os
import tkinter
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import sv_ttk
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

source = ""
folder_organized = False

# Define file categories based on their extensions.
file_categories = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".flv"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".csv", ".pptx", ".odt"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Executables": [".exe", ".msi", ".bat", ".sh", ".app"],
    "Code": [".py", ".java", ".cpp", ".js", ".html", ".css", ".php", ".c"]
}

# Function for browsing folders.
def browse():
    global source, folder_organized, moved_files, created_folders

    new_source = filedialog.askdirectory(title="Select a Folder")

    if new_source and new_source != source:
        source = new_source
        folder_label.config(text=f"Selected: {os.path.basename(source)}")
        folder_organized = False
        moved_files = []
        created_folders = []
        undo_button.config(state="disabled")  # Απενεργοποίηση του Undo για νέο φάκελο
        message_label.config(text="")

        organize_button.config(state="normal")
    elif not new_source:
        folder_label.config(text="No folder selected")
        organize_button.config(state="disabled")


# If the file extension matches one of the categories, return the category name.
def get_category(extension):
    for category, extensions in file_categories.items():
        if extension in extensions:
            return category
    return "Others"

# Function to organize the selected folder by categorizing files based on their extensions
# and moving them into subfolders corresponding to their categories (e.g., Images, Videos, etc.)
def organize():
    global folder_organized, moved_files, created_folders

    if folder_organized:
        message_label.config(text="This folder is already organized.", foreground="red")
        undo_button.config(state="normal")
        return
    
    moved_files = []
    created_folders = []

    if not source:
        message_label.config(text="")
        return

    dir_list = os.listdir(source)

    if not any(os.path.isfile(os.path.join(source, item)) for item in dir_list):
        message_label.config(text="No files to organize.", foreground="red")
        return
    
    confirm = messagebox.askyesno("Confirm File Organization", f"Are you sure you want to organize '{os.path.basename(source)}'?\nWarning: You won't be able to undo this if you select a different folder or close the program.")
    if not confirm:
        return
    
    for file in dir_list:
        split = os.path.splitext(file)
        extension = split[1].lower()
        category = get_category(extension)

        # Skip files with no extension, which will be categorized as "Others"
        if category == "Others" and extension == "":
            continue

        # Define destination folder based on the file category
        destination = os.path.join(source, category)
        src_path = os.path.join(source, file)
        dst_path = os.path.join(destination, file)
        # Store the file position in case user wants to undo
        moved_files.append((src_path,dst_path))

        try:
            # Create the category folder if it doesn't already exist
            if not os.path.exists(destination):
                os.mkdir(destination)
            
            created_folders.append(destination)
            
            # Move the file to the destination folder
            os.rename(src_path, dst_path)
        
        except PermissionError:
            message_label.config(text=f"Permission denied while moving {file}.", foreground="red")
            return # Terminates the process if there is no permission to move the file.

        except FileNotFoundError:
            message_label.config(text=f"File {file} not found.", foreground="red")
            return  # Terminates the process if the file is not found.

        except Exception as e:
            message_label.config(text=f"Error moving {file}: {str(e)}", foreground="red")
            return # Terminates the process if an undefined error occurs.
    
    folder_organized = True

    if moved_files:
        undo_button.config(state="normal")

    message_label.config(text=os.path.basename(source) + " was organized.", foreground="green")


# Function to undo the file organization
def undo():
    global moved_files, folder_organized, created_folders

    # Get the old and new path values we stored in the organize() function
    while moved_files:
        old_path, new_path = moved_files.pop()
        destination = created_folders.pop()
        
        try:
            os.rename(new_path, old_path)
            if os.path.exists(destination) and not os.listdir(destination):
                os.rmdir(destination)
        except Exception as e:
            print(f"Error undoing '{new_path}': {e}")
    
    folder_organized = False
    message_label.config(text="Undo completed.", foreground="green")
    undo_button.config(state="disabled")

# Code for GUI (Tkinter)
root = tkinter.Tk()
root.title("File Organizer")
root.geometry("470x250")
root.resizable(False, False)

browse_button = ttk.Button(root, text="Browse Files", command=browse)
browse_button.pack(pady=20)

folder_label = ttk.Label(root, text="No folder selected")
folder_label.pack()

spacer_label = ttk.Label(root, text="")
spacer_label.pack(pady=20)

button_frame = ttk.Frame(root)
button_frame.pack()

organize_button = ttk.Button(button_frame, text="Organize", width=30, command=organize, state="disabled")
organize_button.pack(side="left", padx=5)

undo_button = ttk.Button(button_frame, text="Undo", width=10, command=undo, state="disabled")
undo_button.pack(side="left")

message_label = ttk.Label(root, text="")
message_label.pack(padx=30)

sv_ttk.set_theme("dark")

root.mainloop()
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

desktop_dir = os.path.expanduser("/Users/bechimcut/Desktop")
download_dir = os.path.expanduser("/Users/bechimcut/Downloads")

screenshot_dir = os.path.join(download_dir, "Screenshot")
recording_dir = os.path.join(download_dir, "ScreenRecording")

os.makedirs(screenshot_dir, exist_ok=True)
os.makedirs(recording_dir, exist_ok=True)

def move_file_to_folder(src_path, dest_folder):
    file_name = os.path.basename(src_path)
    
    # Get the creation timestamp of the file
    file_creation_time = os.path.getctime(src_path)
    formatted_date = time.strftime("%y%m%d", time.localtime(file_creation_time))
    
    # Check if the file name already contains a timestamp
    if "_" in file_name and file_name[:6].isdigit():
        # Extract the original timestamp from the file name
        existing_timestamp = file_name[:6]
        # Create a new filename with the existing timestamp, a numeric counter, and the original file extension
        file_extension = os.path.splitext(file_name)[1]
        new_file_name = f"{existing_timestamp}_{get_next_numeric_counter(dest_folder)}{file_extension}"
    else:
        # Create a new filename with the date, a numeric counter, and the original file extension
        file_extension = os.path.splitext(file_name)[1]
        new_file_name = f"{formatted_date}_{get_next_numeric_counter(dest_folder)}{file_extension}"

    dest_path = os.path.join(dest_folder, new_file_name)

    if not os.path.exists(dest_path):
        os.rename(src_path, dest_path)
        print(f"Moved {file_name} to {dest_folder} as {new_file_name}.")
    else:
        print(f"{new_file_name} already exists in {dest_folder}.")

def get_next_numeric_counter(dest_folder):
    # Get a list of files in the destination folder
    existing_files = os.listdir(dest_folder)
    
    # Initialize the counter to 1
    counter = 1
    
    # Check if filenames with numeric counters exist and find the next available counter
    while True:
        new_file_name = f"{counter:02d}"
        if any(new_file_name in file_name for file_name in existing_files):
            counter += 1
        else:
            return new_file_name

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return 
        file_extension = os.path.splitext(event.src_path)[1].lower()

        if file_extension in (".png", ".jpg", ".jpeg"):
            move_file_to_folder(event.src_path, screenshot_dir)
        elif file_extension == ".mov":
            move_file_to_folder(event.src_path, recording_dir) 

observer = Observer()
observer.schedule(FileHandler(), path=desktop_dir, recursive=False)
observer.start()

try:
    print("Monitoring your desktop for new files. Press Ctrl+C to stop.")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join() 

# Function to process existing files on the desktop.
def process_existing_files():
    desktop_files = os.listdir(desktop_dir)
    for file_name in desktop_files:
        file_path = os.path.join(desktop_dir, file_name)
        if os.path.isfile(file_path):
            file_extension = os.path.splitext(file_name)[1].lower()
            
            if file_extension in (".png", ".jpg", ".jpeg"):
                move_file_to_folder(file_path, screenshot_dir)
                print(f"Processed and moved an existing screenshot: {file_path}")
            elif file_extension == ".mov":
                move_file_to_folder(file_path, recording_dir)
                print(f"Processed and moved an existing recording: {file_path}")

process_existing_files()

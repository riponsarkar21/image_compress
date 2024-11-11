import os
from tkinter import Tk, filedialog, Label, Entry, Button, StringVar
from PIL import Image

def select_files():
    global file_paths
    file_paths = filedialog.askopenfilenames(
        title="Select JPG or PNG files",
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )
    lbl_selected_files.config(text=f"Selected {len(file_paths)} files.")

def select_destination_folder():
    global destination_folder
    destination_folder = filedialog.askdirectory(title="Select Destination Folder")
    lbl_destination_folder.config(text=f"Destination: {destination_folder}")

def compress_images():
    prefix = entry_prefix.get()
    suffix = entry_suffix.get()
    max_size_kb = int(entry_max_size.get())
    for file_path in file_paths:
        img = Image.open(file_path)
        filename, ext = os.path.splitext(os.path.basename(file_path))
        new_filename = f"{prefix}{filename}{suffix}{ext}"
        output_path = os.path.join(destination_folder, new_filename)
        
        quality = 95  # Start with high quality and adjust
        img.save(output_path, quality=quality)
        
        # Adjust quality to meet max size
        while os.path.getsize(output_path) > max_size_kb * 1024:
            quality -= 5
            img.save(output_path, quality=quality)
            if quality <= 5:  # Avoid going below too low quality
                break

        print(f"Saved: {output_path} (Size: {os.path.getsize(output_path) / 1024:.2f} KB)")

    lbl_status.config(text="Compression Completed!")

# GUI Setup
root = Tk()
root.title("Image Compressor")

# Variables
file_paths = []
destination_folder = ""
lbl_selected_files = Label(root, text="No files selected.")
lbl_selected_files.pack()

# File selection button
btn_select_files = Button(root, text="Select Images", command=select_files)
btn_select_files.pack()

# Prefix, Suffix, and Max Size Entry
Label(root, text="Prefix:").pack()
entry_prefix = Entry(root)
entry_prefix.pack()

Label(root, text="Suffix:").pack()
entry_suffix = Entry(root)
entry_suffix.pack()

Label(root, text="Max File Size (KB):").pack()
entry_max_size = Entry(root)
entry_max_size.insert(0, "200")  # Default 200 KB
entry_max_size.pack()

# Destination Folder Selection
lbl_destination_folder = Label(root, text="No destination folder selected.")
lbl_destination_folder.pack()

btn_select_destination = Button(root, text="Select Destination Folder", command=select_destination_folder)
btn_select_destination.pack()

# Compress Button
btn_compress = Button(root, text="Compress Images", command=compress_images)
btn_compress.pack()

# Status Label
lbl_status = Label(root, text="")
lbl_status.pack()

root.mainloop()

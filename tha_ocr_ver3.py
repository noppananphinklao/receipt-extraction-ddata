import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import pytesseract
import pyperclip
import os
import numpy as np

class CharacterSelectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Character Selection")
        self.mv_x = 0 
        self.mv_y = 0
        self.not_first_load = True
        screen_width = 720
        screen_height = root.winfo_screenheight()

        self.zoom_factor = 1.0  # Initial zoom factor

        # Create and configure canvas for displaying the image
        self.canvas = tk.Canvas(root, width=screen_width, height=screen_height - 150, bg='black')
        self.canvas.pack()

        # Create buttons
        self.extract_button = tk.Button(root, text="Extract and Copy", command=self.extract_and_copy)
        self.extract_button.pack(side='left')

        # Create Zoom buttons
        self.zoom_in_button = tk.Button(root, text="Zoom In", command=self.zoom_in)
        self.zoom_in_button.pack(side='left')
        self.zoom_out_button = tk.Button(root, text="Zoom Out", command=self.zoom_out)
        self.zoom_out_button.pack(side='left')

        # Create OCR language switch
        self.lang_label = tk.Label(root, text="OCR Language:")
        self.lang_label.pack(side='left')

        self.lang_var = tk.StringVar(value="eng")  # Default language is 'eng'

        self.eng_radio = tk.Radiobutton(root, text="English", variable=self.lang_var, value="eng")
        self.tha_radio = tk.Radiobutton(root, text="Thai", variable=self.lang_var, value="tha")

        self.eng_radio.pack(side='left')
        self.tha_radio.pack(side='left')

        # Initialize image variables
        self.original_image_path = None
        self.image_path = None
        self.original_image = None
        self.image = None
        self.selection_coords = None
        self.selection_rect = None  # To store the reference to the selection rectangle

        # Create Next Image button
        self.next_image_button = tk.Button(root, text="Next Image", command=self.load_next_image)
        self.next_image_button.pack(side='left')

        # Initialize image variables and list of image file paths
        self.original_image_path = None
        self.image_path = None
        self.original_image = None
        self.image = None
        self.selection_coords = None
        self.selection_rect = None
        self.image_files = []  # List to store image file paths
        self.current_image_index = -1  # Index to track the current image

        # Load image files from the folder
        self.load_image_files()

    def load_image_files(self):
        # Prompt the user to select a folder containing image files
        folder_path = filedialog.askdirectory()
        if folder_path:
            # Get a list of image file paths in the folder
            image_extensions = [".png", ".jpg", ".jpeg", ".bmp"]
            self.image_files = [
                os.path.join(folder_path, file)
                for file in os.listdir(folder_path)
                if os.path.isfile(os.path.join(folder_path, file))
                and file.lower().endswith(tuple(image_extensions))
            ]
            if self.image_files:
                # Initialize the current image index
                self.current_image_index = 0
                # Load the first image from the list
                self.load_image()

    def load_image(self):
        # if self.not_first_load:
        #     self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        self.image_path = self.image_files[self.current_image_index]
        if self.image_path:
            self.original_image_path = self.image_path  # Store the original image path
            self.original_image = Image.open(self.image_path)

            # Get the canvas dimensions
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            # Calculate the aspect ratio of the canvas
            canvas_aspect_ratio = canvas_width / canvas_height

            # Get the original image dimensions
            original_width, original_height = self.original_image.size

            # Calculate the new dimensions while preserving the original aspect ratio
            if canvas_aspect_ratio > 1:
                # Canvas is wider than the image
                new_width = int(canvas_height * original_width / original_height)
                new_height = canvas_height
            else:
                # Canvas is taller than the image
                new_width = canvas_width
                new_height = int(canvas_width * original_height / original_width)

            # Resize the original image to fit the canvas while preserving its aspect ratio
            self.image = self.original_image.resize((new_width, new_height), Image.LANCZOS)

            # Clear any existing selection rectangle
            self.clear_selection_rectangle()

            # Calculate the position to center the image on the canvas
            x_position = (canvas_width - new_width) // 2
            y_position = (canvas_height - new_height) // 2

            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(x_position, y_position, anchor=tk.NW, image=self.tk_image)

            # Set the zoom factor to 1.0 and update the image immediately
            self.zoom_factor = 1.0
            self.mv_y = 0
            self.mv_x = 0
            self.update_image()

    def load_next_image(self):
        self.not_first_load = False
        if self.image_files:
            # Increment the current image index
            self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
            # Load the next image from the list
            self.load_image()

    def zoom_in(self):
        self.zoom_factor *= 1.2
        self.update_image()

    def zoom_out(self):
        self.zoom_factor /= 1.2
        self.update_image()

    def update_image(self):
        if self.image is not None:
            # Calculate the new dimensions based on the zoom factor
            new_width = int(self.original_image.width * self.zoom_factor)
            new_height = int(self.original_image.height * self.zoom_factor)

            # Resize the original image with the new dimensions
            self.image = self.original_image.resize((new_width, new_height), Image.LANCZOS)
            # self.image = self.image[:, self.mv_x:, :]

            # Clear any existing selection rectangle
            self.clear_selection_rectangle()

            # Calculate the position to center the image on the canvas
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            x_position = (canvas_width - new_width) // 2
            y_position = (canvas_height - new_height) // 2

            # Update the displayed image
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(x_position + self.mv_x, y_position + self.mv_y, anchor=tk.NW, image=self.tk_image)

    def extract_and_copy(self):
        if self.image is None or self.selection_coords is None:
            messagebox.showerror("Error", "Please load an image and select an area first.")
            return

        left, top, right, bottom = self.selection_coords

        # Adjust the selection coordinates based on the image's position on the canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        image_width = self.image.width
        image_height = self.image.height
        image_x = (canvas_width - image_width) // 2 + self.mv_x  # Include horizontal translation
        image_y = (canvas_height - image_height) // 2 + self.mv_y

        left -= image_x
        top -= image_y
        right -= image_x
        bottom -= image_y

        # Crop the selected portion of the image
        selected_area = self.image.crop((left, top, right, bottom))

        # Perform OCR on the selected area
        extracted_text = pytesseract.image_to_string(selected_area, lang=(self.lang_var.get()))

        # Copy the extracted text to the clipboard
        pyperclip.copy(extracted_text)
        messagebox.showinfo("Information", "Text extracted and copied to clipboard:\n\n" + extracted_text)

    def clear_selection_rectangle(self):
        # Clear the selection rectangle
        if self.selection_rect:
            self.canvas.delete(self.selection_rect)
            self.selection_rect = None

    def draw_selection_rectangle(self):
        if self.selection_coords:
            left, top, right, bottom = self.selection_coords

            # Draw a temporary rectangle with transparent red color
            self.selection_rect = self.canvas.create_rectangle(left, top, right, bottom, outline="red",
                                                              dash=(4, 4), stipple="gray50", width=1)

    def on_mouse_press(self, event):
        self.start_x, self.start_y = event.x, event.y


    def on_mouse_drag(self, event):
        self.end_x, self.end_y = event.x, event.y

        # Store the coordinates of the selected area and draw the rectangle
        self.selection_coords = (
            min(self.start_x, self.end_x),
            min(self.start_y, self.end_y),
            max(self.start_x, self.end_x),
            max(self.start_y, self.end_y)
        )

        # Remove the previous temporary rectangle
        self.clear_selection_rectangle()
        self.draw_selection_rectangle()

    def on_mouse_release(self, event):
        self.end_x, self.end_y = event.x, event.y
        # Store the coordinates of the selected area and draw the final rectangle
        self.selection_coords = (
            min(self.start_x, self.end_x),
            min(self.start_y, self.end_y),
            max(self.start_x, self.end_x),
            max(self.start_y, self.end_y)
        )

        # Remove the previous temporary rectangle
        self.clear_selection_rectangle()
        self.draw_selection_rectangle()

    def on_up_arrow_key(self, event):
        self.mv_y += 20
        self.update_image()

    def on_down_arrow_key(self, event):
        self.mv_y -= 20
        self.update_image()

    def on_right_arrow_key(self, event):
        self.mv_x += 20
        self.update_image()
    
    def on_left_arrow_key(self, event):
        self.mv_x -= 20
        self.update_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = CharacterSelectionApp(root)
    root.bind("<ButtonPress-1>", app.on_mouse_press)
    root.bind("<B1-Motion>", app.on_mouse_drag)
    root.bind("<ButtonRelease-1>", app.on_mouse_release)
    root.bind('<Right>', app.on_right_arrow_key)
    root.bind('<Left>', app.on_left_arrow_key)
    root.bind('<Up>', app.on_up_arrow_key)
    root.bind('<Down>', app.on_down_arrow_key)
    root.mainloop()


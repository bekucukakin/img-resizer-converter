from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkinter import PhotoImage

def resize_image(image_path, output_path, width, height):
    try:
        if not output_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            raise ValueError("Output path must include a valid file name with an image extension (e.g., .jpg, .png).")

        with Image.open(image_path) as img:
            img_resized = img.resize((width, height))
            img_resized.save(output_path)
            messagebox.showinfo("Success", f"Image resized and saved to {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error resizing image: {e}")

def convert_image_format(image_path, output_path, format):
    try:
        with Image.open(image_path) as img:
            img.convert("RGB").save(output_path, format=format)
            messagebox.showinfo("Success", f"Image converted to {format} format and saved to {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error converting image format: {e}")

def open_file():
    return filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])

def save_file():
    return filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("BMP files", "*.bmp"), ("GIF files", "*.gif")])

def resize_gui():
    def perform_resize():
        image_path = open_file()
        if not image_path:
            return
        output_path = save_file()
        if not output_path:
            return
        try:
            width = int(width_entry.get())
            height = int(height_entry.get())
            resize_image(image_path, output_path, width, height)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid width and height values.")

    window = tk.Tk()
    window.title("Image Resizer")
    window.geometry("400x250")
    window.configure(bg="#f5f5f5")

    title_label = tk.Label(window, text="Resize Image", font=("Arial", 16, "bold"), bg="#f5f5f5")
    title_label.pack(pady=10)

    form_frame = tk.Frame(window, bg="#f5f5f5")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Width:", bg="#f5f5f5", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    width_entry = tk.Entry(form_frame, font=("Arial", 12))
    width_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Height:", bg="#f5f5f5", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    height_entry = tk.Entry(form_frame, font=("Arial", 12))
    height_entry.grid(row=1, column=1, padx=10, pady=5)

    resize_button = tk.Button(window, text="Resize Image", command=perform_resize, font=("Arial", 12), bg="#4CAF50", fg="white", padx=20, pady=5)
    resize_button.pack(pady=10)

    window.mainloop()

def convert_gui():
    def perform_conversion(format):
        image_path = open_file()
        if not image_path:
            return
        output_path = save_file()
        if not output_path:
            return
        convert_image_format(image_path, output_path, format)

    window = tk.Tk()
    window.title("Image Format Converter")
    window.geometry("400x300")
    window.configure(bg="#f5f5f5")

    title_label = tk.Label(window, text="Convert Image Format", font=("Arial", 16, "bold"), bg="#f5f5f5")
    title_label.pack(pady=10)

    form_frame = tk.Frame(window, bg="#f5f5f5")
    form_frame.pack(pady=10)

    # Add buttons for different formats
    button_frame = tk.Frame(form_frame, bg="#f5f5f5")
    button_frame.grid(row=0, column=0, padx=10, pady=5)

    def on_format_select(format):
        perform_conversion(format)

    formats = ["JPEG", "PNG", "BMP", "GIF"]
    for i, format in enumerate(formats):
        format_button = tk.Button(button_frame, text=format, command=lambda format=format: on_format_select(format), font=("Arial", 12), bg="#FF5722", fg="white", padx=20, pady=5)
        format_button.grid(row=0, column=i, padx=5, pady=5)

    window.mainloop()

def main():
    root = tk.Tk()
    root.title("Image Resizer and Format Converter")
    root.geometry("400x350")
    root.configure(bg="#f5f5f5")

    title_label = tk.Label(root, text="Image Resizer & Converter", font=("Arial", 18, "bold"), bg="#f5f5f5")
    title_label.pack(pady=20)

    button_frame = tk.Frame(root, bg="#f5f5f5")
    button_frame.pack(pady=10)

    resize_button = tk.Button(button_frame, text="Resize Image", command=resize_gui, font=("Arial", 14), bg="#2196F3", fg="white", padx=20, pady=10)
    resize_button.grid(row=0, column=0, padx=20, pady=10)

    convert_button = tk.Button(button_frame, text="Convert Format", command=convert_gui, font=("Arial", 14), bg="#FF5722", fg="white", padx=20, pady=10)
    convert_button.grid(row=0, column=1, padx=20, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()

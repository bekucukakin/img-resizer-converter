from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def resize_and_convert_image(image_path, output_path, width, height, output_format):
    try:
        with Image.open(image_path) as img:
            img_resized = img.resize((width, height))
            img_resized.save(output_path, format=output_format)
            messagebox.showinfo("Success", f"Image resized, converted, and saved to {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error resizing and converting image: {e}")

def open_file():
    return filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])

def save_file(output_format):
    default_extension = f".{output_format.lower()}"
    return filedialog.asksaveasfilename(defaultextension=default_extension,
                                        filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"),
                                                  ("BMP files", "*.bmp"), ("GIF files", "*.gif")])

def show_selection_screen():
    def on_resize_select():
        window.destroy()
        resize_gui()

    def on_convert_select():
        window.destroy()
        convert_gui()

    window = tk.Tk()
    window.title("Choose Action")
    window.geometry("500x300")
    window.configure(bg="#2c3e50")  # Dark background for modern look

    # Title Label
    label = ttk.Label(window, text="Choose an option:", font=("Helvetica", 18, "bold"), foreground="white", background="#2c3e50")
    label.pack(pady=30)

    # Buttons with ttk for modern design
    resize_button = ttk.Button(window, text="Resize Image", command=on_resize_select, width=20)
    resize_button.pack(pady=10)

    convert_button = ttk.Button(window, text="Convert Image Format", command=on_convert_select, width=20)
    convert_button.pack(pady=10)

    window.mainloop()

def resize_gui():
    def perform_resize():
        if not image_path:
            return
        output_format = format_var.get()
        output_path = save_file(output_format)
        if not output_path:
            return
        try:
            width = int(width_entry.get())
            height = int(height_entry.get())
            resize_and_convert_image(image_path, output_path, width, height, output_format)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid width and height values.")

    def update_preview():
        try:
            if not image_path:
                return
            width = int(width_entry.get())
            height = int(height_entry.get())

            with Image.open(image_path) as img:
                img_resized = img.resize((width, height))
                img_tk = ImageTk.PhotoImage(img_resized)
                canvas.image = img_tk
                canvas.delete("all")
                canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
                canvas.config(scrollregion=canvas.bbox("all"))
                canvas.config(width=width, height=height)
        except Exception as e:
            print(f"Error updating preview: {e}")

    image_path = open_file()
    if not image_path:
        return

    window = tk.Tk()
    window.title("Image Resizer with Preview")
    window.geometry("800x600")
    window.configure(bg="#34495e")

    # Title Label
    title_label = ttk.Label(window, text="Resize Image with Preview", font=("Helvetica", 16, "bold"), foreground="white", background="#34495e")
    title_label.pack(pady=20)

    # Form Frame with ttk styling
    form_frame = ttk.Frame(window)
    form_frame.pack(pady=10)

    ttk.Label(form_frame, text="Width:", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=5)
    width_entry = ttk.Entry(form_frame, font=("Helvetica", 12))
    width_entry.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(form_frame, text="Height:", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=5)
    height_entry = ttk.Entry(form_frame, font=("Helvetica", 12))
    height_entry.grid(row=1, column=1, padx=10, pady=5)

    # Format selection for conversion
    ttk.Label(form_frame, text="Select Format:", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=5)
    format_var = tk.StringVar(value="JPEG")
    format_menu = ttk.Combobox(form_frame, textvariable=format_var, values=["JPEG", "PNG", "BMP", "GIF"], state="readonly", width=10)
    format_menu.grid(row=2, column=1, padx=10, pady=5)

    # Update preview button with modern style
    update_button = ttk.Button(form_frame, text="Update Preview", command=update_preview, width=20)
    update_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Canvas for preview
    canvas_frame = ttk.Frame(window)
    canvas_frame.pack(pady=10)
    canvas = tk.Canvas(canvas_frame, width=400, height=300, bg="#ecf0f1")
    canvas.pack()

    # Load initial preview
    with Image.open(image_path) as img:
        img.thumbnail((400, 300))
        img_tk = ImageTk.PhotoImage(img)
        canvas.image = img_tk
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        canvas.config(scrollregion=canvas.bbox("all"))

    # Resize button
    resize_button = ttk.Button(window, text="Resize Image", command=perform_resize, width=20)
    resize_button.pack(pady=10)

    # Back to main menu button
    back_button = ttk.Button(window, text="Back to Main Menu", command=show_selection_screen, width=20)
    back_button.pack(pady=10)

    window.mainloop()

def convert_gui():
    def perform_conversion():
        if not image_path:
            return
        output_format = format_var.get()
        output_path = save_file(output_format)
        if not output_path:
            return
        try:
            with Image.open(image_path) as img:
                img.save(output_path, format=output_format)
            messagebox.showinfo("Success", f"Image converted and saved to {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error converting image: {e}")

    image_path = open_file()
    if not image_path:
        return

    window = tk.Tk()
    window.title("Convert Image Format")
    window.geometry("800x400")
    window.configure(bg="#34495e")

    title_label = ttk.Label(window, text="Convert Image Format", font=("Helvetica", 16, "bold"), foreground="white", background="#34495e")
    title_label.pack(pady=20)

    form_frame = ttk.Frame(window)
    form_frame.pack(pady=10)

    ttk.Label(form_frame, text="Select Format:", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=5)
    format_var = tk.StringVar(value="JPEG")
    format_menu = ttk.Combobox(form_frame, textvariable=format_var, values=["JPEG", "PNG", "BMP", "GIF"], state="readonly", width=10)
    format_menu.grid(row=0, column=1, padx=10, pady=5)

    convert_button = ttk.Button(window, text="Convert Image", command=perform_conversion, width=20)
    convert_button.pack(pady=20)

    back_button = ttk.Button(window, text="Back to Main Menu", command=show_selection_screen, width=20)
    back_button.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    show_selection_screen()

from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

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
    # Generate default file name with the selected format
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
    window.geometry("400x200")
    window.configure(bg="#f5f5f5")

    label = tk.Label(window, text="Choose an option:", font=("Arial", 16, "bold"), bg="#f5f5f5")
    label.pack(pady=20)

    resize_button = tk.Button(window, text="Resize Image", command=on_resize_select, font=("Arial", 12), bg="#4CAF50", fg="white", padx=20, pady=10)
    resize_button.pack(pady=10)

    convert_button = tk.Button(window, text="Convert Image Format", command=on_convert_select, font=("Arial", 12), bg="#2196F3", fg="white", padx=20, pady=10)
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
                canvas.image = img_tk  # Referansı tutuyoruz
                canvas.delete("all")  # Eski resmi temizliyoruz
                canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
                canvas.config(scrollregion=canvas.bbox("all"))
                canvas.config(width=width, height=height)  # Dynamically adjust canvas size
        except Exception as e:
            print(f"Error updating preview: {e}")

    image_path = open_file()
    if not image_path:
        return

    window = tk.Tk()
    window.title("Image Resizer with Preview")
    window.geometry("800x600")
    window.configure(bg="#f5f5f5")

    title_label = tk.Label(window, text="Resize Image with Preview", font=("Arial", 16, "bold"), bg="#f5f5f5")
    title_label.pack(pady=10)

    form_frame = tk.Frame(window, bg="#f5f5f5")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Width:", bg="#f5f5f5", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    width_entry = tk.Entry(form_frame, font=("Arial", 12))
    width_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Height:", bg="#f5f5f5", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    height_entry = tk.Entry(form_frame, font=("Arial", 12))
    height_entry.grid(row=1, column=1, padx=10, pady=5)

    # Format selection for conversion
    tk.Label(form_frame, text="Select Format:", bg="#f5f5f5", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
    format_var = tk.StringVar(value="JPEG")
    format_menu = tk.OptionMenu(form_frame, format_var, "JPEG", "PNG", "BMP", "GIF")
    format_menu.grid(row=2, column=1, padx=10, pady=5)

    # Update preview button
    update_button = tk.Button(form_frame, text="Update Preview", command=update_preview, font=("Arial", 12),
                               bg="#2196F3", fg="white", padx=10, pady=5)
    update_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Canvas for preview
    canvas_frame = tk.Frame(window, bg="#f5f5f5")
    canvas_frame.pack(pady=10)
    canvas = tk.Canvas(canvas_frame, width=400, height=300, bg="#e0e0e0")
    canvas.pack()

    # Load initial preview
    with Image.open(image_path) as img:
        img.thumbnail((400, 300))
        img_tk = ImageTk.PhotoImage(img)
        canvas.image = img_tk  # Referansı tutuyoruz
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        canvas.config(scrollregion=canvas.bbox("all"))

    resize_button = tk.Button(window, text="Resize Image", command=perform_resize, font=("Arial", 12), bg="#4CAF50",
                               fg="white", padx=20, pady=5)
    resize_button.pack(pady=10)

    # Back to main menu button
    back_button = tk.Button(window, text="Back to Main Menu", command=show_selection_screen, font=("Arial", 12), bg="#f44336", fg="white", padx=20, pady=5)
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
    window.configure(bg="#f5f5f5")

    title_label = tk.Label(window, text="Convert Image Format", font=("Arial", 16, "bold"), bg="#f5f5f5")
    title_label.pack(pady=10)

    form_frame = tk.Frame(window, bg="#f5f5f5")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Select Format:", bg="#f5f5f5", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    format_var = tk.StringVar(value="JPEG")
    format_menu = tk.OptionMenu(form_frame, format_var, "JPEG", "PNG", "BMP", "GIF")
    format_menu.grid(row=0, column=1, padx=10, pady=5)

    convert_button = tk.Button(window, text="Convert Image", command=perform_conversion, font=("Arial", 12), bg="#4CAF50",
                               fg="white", padx=20, pady=5)
    convert_button.pack(pady=20)

    # Back to main menu button
    back_button = tk.Button(window, text="Back to Main Menu", command=show_selection_screen, font=("Arial", 12), bg="#f44336", fg="white", padx=20, pady=5)
    back_button.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    show_selection_screen()

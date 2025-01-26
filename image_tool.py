import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageEnhance
import traceback

# --------------------------
# Global Configuration
# --------------------------
APP_NAME = "Image-Resizer-Converter"
VERSION = "2.2.2"
DEFAULT_SIZE = 400
MIN_SIZE = 100
MAX_SIZE = 4000
ASPECT_RATIO_LOCK = False  # Future feature placeholder

# --------------------------
# Global State Management
# --------------------------
class AppState:
    """Manages application state and image editing parameters"""
    def __init__(self):
        self.preview_canvas = None
        self.tk_image = None
        self.image_path = None
        self.edit_window = None
        self.editing_params = {
            "width": DEFAULT_SIZE,
            "height": DEFAULT_SIZE,
            "rotation": 0,
            "crop": None,
            "brightness": 1.0,
            "contrast": 1.0
        }
        self.crop_data = {
            "start_x": 0,
            "start_y": 0,
            "current_rect": None,
            "crop_rect": None,
            "img_x": 0,
            "img_y": 0,
            "img_width": 0,
            "img_height": 0
        }

app_state = AppState()

# --------------------------
# Core Image Operations
# --------------------------
def apply_image_operations(image):
    """
    Applies all active editing operations to the image
    Args:
        image: PIL.Image object to process
    Returns:
        Processed PIL.Image object
    """
    # Validate dimensions
    width = max(MIN_SIZE, app_state.editing_params["width"])
    height = max(MIN_SIZE, app_state.editing_params["height"])
    
    # Apply rotation
    if app_state.editing_params["rotation"] != 0:
        image = image.rotate(app_state.editing_params["rotation"] % 360, expand=True)
    
    # Apply cropping
    if app_state.editing_params["crop"]:
        try:
            image = image.crop(app_state.editing_params["crop"])
        except Exception as e:
            print(f"Crop Error: {str(e)}")
    
    # Apply color adjustments
    image = ImageEnhance.Brightness(image).enhance(
        max(0.1, min(app_state.editing_params["brightness"], 3.0))
    )
    image = ImageEnhance.Contrast(image).enhance(
        max(0.1, min(app_state.editing_params["contrast"], 3.0))
    )
    
    return image.resize((width, height))

# --------------------------
# Preview Management
# --------------------------
def update_image_preview():
    """Updates the canvas with current image and edits"""
    if not all([app_state.preview_canvas, app_state.image_path]):
        return

    try:
        with Image.open(app_state.image_path) as original_img:
            # Process image with current parameters
            processed_img = apply_image_operations(original_img)
            
            # Calculate canvas dimensions
            canvas_width = max(MIN_SIZE, app_state.preview_canvas.winfo_width())
            canvas_height = max(MIN_SIZE, app_state.preview_canvas.winfo_height())
            
            # Create thumbnail for preview
            processed_img.thumbnail(
                (canvas_width - 20, canvas_height - 20),
                Image.Resampling.LANCZOS
            )
            
            # Update canvas display
            app_state.tk_image = ImageTk.PhotoImage(processed_img)
            app_state.preview_canvas.delete("all")
            
            # Calculate positioning
            img_w, img_h = processed_img.size
            img_x = (canvas_width - img_w) // 2
            img_y = (canvas_height - img_h) // 2
            
            # Update state tracking
            app_state.crop_data.update({
                "img_x": img_x,
                "img_y": img_y,
                "img_width": img_w,
                "img_height": img_h
            })
            
            # Draw centered image
            app_state.preview_canvas.create_image(
                img_x + (img_w // 2),
                img_y + (img_h // 2),
                anchor=tk.CENTER,
                image=app_state.tk_image
            )
            app_state.preview_canvas.update_idletasks()

    except Exception as e:
        print(f"Preview Error: {str(e)}")
        traceback.print_exc()

# --------------------------
# Crop Operations
# --------------------------
def start_crop(event):
    """Initialize cropping operation"""
    if (app_state.crop_data["img_x"] < event.x < app_state.crop_data["img_x"] + app_state.crop_data["img_width"] and 
        app_state.crop_data["img_y"] < event.y < app_state.crop_data["img_y"] + app_state.crop_data["img_height"]):
        app_state.crop_data.update({
            "start_x": app_state.preview_canvas.canvasx(event.x),
            "start_y": app_state.preview_canvas.canvasy(event.y)
        })
        app_state.crop_data["current_rect"] = app_state.preview_canvas.create_rectangle(
            app_state.crop_data["start_x"], 
            app_state.crop_data["start_y"], 
            app_state.crop_data["start_x"], 
            app_state.crop_data["start_y"],
            outline="#ff0000", 
            width=2, 
            dash=(5,5)
        )

def update_crop_selection(event):
    """Update cropping rectangle during mouse movement"""
    if app_state.crop_data["current_rect"]:
        cur_x = max(app_state.crop_data["img_x"], 
                   min(app_state.preview_canvas.canvasx(event.x), 
                       app_state.crop_data["img_x"] + app_state.crop_data["img_width"]))
        cur_y = max(app_state.crop_data["img_y"], 
                   min(app_state.preview_canvas.canvasy(event.y), 
                       app_state.crop_data["img_y"] + app_state.crop_data["img_height"]))
        
        app_state.preview_canvas.coords(
            app_state.crop_data["current_rect"],
            app_state.crop_data["start_x"],
            app_state.crop_data["start_y"],
            cur_x,
            cur_y
        )

def finalize_crop(event):
    """Finalize cropping coordinates"""
    if app_state.crop_data["current_rect"]:
        # Calculate final coordinates
        end_x = max(app_state.crop_data["img_x"], 
                   min(app_state.preview_canvas.canvasx(event.x), 
                       app_state.crop_data["img_x"] + app_state.crop_data["img_width"]))
        end_y = max(app_state.crop_data["img_y"], 
                   min(app_state.preview_canvas.canvasy(event.y), 
                       app_state.crop_data["img_y"] + app_state.crop_data["img_height"]))
        
        # Convert to image coordinates
        with Image.open(app_state.image_path) as img:
            scale_x = img.width / max(1, app_state.crop_data["img_width"])
            scale_y = img.height / max(1, app_state.crop_data["img_height"])
            
            app_state.editing_params["crop"] = (
                int((min(app_state.crop_data["start_x"], end_x) - app_state.crop_data["img_x"]) * scale_x),
                int((min(app_state.crop_data["start_y"], end_y) - app_state.crop_data["img_y"]) * scale_y),
                int((max(app_state.crop_data["start_x"], end_x) - app_state.crop_data["img_x"]) * scale_x),
                int((max(app_state.crop_data["start_y"], end_y) - app_state.crop_data["img_y"]) * scale_y)
            )
        
        # Cleanup temporary drawing
        app_state.preview_canvas.delete(app_state.crop_data["current_rect"])
        app_state.crop_data["current_rect"] = None
        update_image_preview()

# --------------------------
# File Operations
# --------------------------
def open_image_file():
    """Handle image file selection and initialization"""
    file_types = [
        ("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.webp"),
        ("All Files", "*.*")
    ]
    
    app_state.image_path = filedialog.askopenfilename(filetypes=file_types)
    if not app_state.image_path:
        return

    try:
        # Verify image format
        with Image.open(app_state.image_path) as img:
            if img.format not in ["JPEG", "PNG", "BMP", "GIF", "WEBP"]:
                raise ValueError(f"Unsupported format: {img.format}")
                
        create_editor_window()
        update_image_preview()
        
    except Exception as e:
        error_msg = f"Failed to open image:\n{str(e)}\n\nDetails:\n{traceback.format_exc()}"
        messagebox.showerror("Initialization Error", error_msg)

def save_processed_image(output_format):
    """Save processed image with selected format"""
    if not app_state.image_path:
        messagebox.showerror("Error", "No image selected!")
        return

    try:
        output_path = filedialog.asksaveasfilename(
            defaultextension=f".{output_format.lower()}",
            filetypes=[(f"{output_format} Files", f"*.{output_format.lower()}")]
        )
        if not output_path:
            return

        with Image.open(app_state.image_path) as img:
            edited_img = apply_image_operations(img)
            edited_img.save(output_path, format=output_format, quality=95)
            
        messagebox.showinfo("Success", f"Image saved successfully:\n{output_path}")

    except Exception as e:
        messagebox.showerror("Save Error", f"Failed to save image:\n{str(e)}")

# --------------------------
# GUI Components
# --------------------------
def create_editor_window():
    """Create main image editing window"""
    if app_state.edit_window and app_state.edit_window.winfo_exists():
        app_state.edit_window.destroy()

    app_state.edit_window = tk.Toplevel()
    app_state.edit_window.title(f"{APP_NAME} - Editor")
    app_state.edit_window.geometry("1000x800")
    app_state.edit_window.minsize(800, 600)
    
    # Configure main container
    main_container = ttk.Frame(app_state.edit_window)
    main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Create preview canvas
    canvas_frame = ttk.Frame(main_container)
    canvas_frame.pack(fill=tk.BOTH, expand=True)
    
    app_state.preview_canvas = tk.Canvas(
        canvas_frame, 
        bg="#2e2e2e",
        highlightthickness=0,
        relief="flat"
    )
    app_state.preview_canvas.pack(fill=tk.BOTH, expand=True)
    
    # Configure mouse bindings
    app_state.preview_canvas.bind("<ButtonPress-1>", start_crop)
    app_state.preview_canvas.bind("<B1-Motion>", update_crop_selection)
    app_state.preview_canvas.bind("<ButtonRelease-1>", finalize_crop)
    app_state.preview_canvas.bind("<Configure>", lambda e: update_image_preview())
    
    # Create control panel
    control_panel = ttk.Frame(main_container)
    control_panel.pack(fill=tk.X, pady=10)
    
    # Parameter adjustment controls
    ttk.Label(control_panel, text="Width:").grid(row=0, column=0, padx=5)
    width_control = ttk.Scale(
        control_panel, 
        from_=MIN_SIZE, 
        to=MAX_SIZE,
        command=lambda v: update_parameter("width", v)
    )
    width_control.set(DEFAULT_SIZE)
    width_control.grid(row=0, column=1, padx=5)

    ttk.Label(control_panel, text="Height:").grid(row=0, column=2, padx=5)
    height_control = ttk.Scale(
        control_panel, 
        from_=MIN_SIZE, 
        to=MAX_SIZE,
        command=lambda v: update_parameter("height", v)
    )
    height_control.set(DEFAULT_SIZE)
    height_control.grid(row=0, column=3, padx=5)

    ttk.Label(control_panel, text="Rotation (°):").grid(row=1, column=0, padx=5)
    rotation_control = ttk.Scale(
        control_panel, 
        from_=-180, 
        to=180,
        command=lambda v: update_parameter("rotation", v)
    )
    rotation_control.grid(row=1, column=1, columnspan=3, sticky="ew", padx=5)

    ttk.Label(control_panel, text="Brightness:").grid(row=2, column=0, padx=5)
    brightness_control = ttk.Scale(
        control_panel, 
        from_=0.1, 
        to=3.0,
        command=lambda v: update_parameter("brightness", v)
    )
    brightness_control.set(1.0)
    brightness_control.grid(row=2, column=1, padx=5)

    ttk.Label(control_panel, text="Contrast:").grid(row=2, column=2, padx=5)
    contrast_control = ttk.Scale(
        control_panel, 
        from_=0.1, 
        to=3.0,
        command=lambda v: update_parameter("contrast", v)
    )
    contrast_control.set(1.0)
    contrast_control.grid(row=2, column=3, padx=5)

    # Crop management
    crop_management = ttk.Frame(control_panel)
    crop_management.grid(row=3, column=0, columnspan=4, pady=10)
    ttk.Button(
        crop_management, 
        text="Reset Crop", 
        command=lambda: [
            app_state.editing_params.update({"crop": None}),
            update_image_preview()
        ]
    ).pack(side=tk.LEFT)

    # Save controls
    save_panel = ttk.Frame(control_panel)
    save_panel.grid(row=4, column=0, columnspan=4, pady=10)
    format_selector = ttk.Combobox(
        save_panel, 
        values=["JPEG", "PNG", "BMP", "GIF"], 
        state="readonly"
    )
    format_selector.set("PNG")
    format_selector.pack(side=tk.LEFT)
    
    ttk.Button(
        save_panel, 
        text="Export", 
        command=lambda: save_processed_image(format_selector.get())
    ).pack(side=tk.LEFT, padx=5)

def update_parameter(param, value):
    """Update editing parameters with validation"""
    try:
        if param in ["width", "height"]:
            app_state.editing_params[param] = max(MIN_SIZE, int(float(value)))
        elif param == "rotation":
            app_state.editing_params[param] = int(float(value)) % 360
        elif param in ["brightness", "contrast"]:
            app_state.editing_params[param] = max(0.1, min(float(value), 3.0))
        
        update_image_preview()
    except ValueError:
        pass

# --------------------------
# Application Initialization
# --------------------------
def initialize_application():
    """Initialize main application window"""
    root = tk.Tk()
    root.title(APP_NAME)
    root.geometry("400x200")
    
    # Configure styling
    style = ttk.Style()
    style.configure("TButton", padding=6, font=("Segoe UI", 10))
    style.configure("TLabel", font=("Segoe UI", 9))
    
    # Create main container
    main_container = ttk.Frame(root)
    main_container.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
    
    # Application branding
    ttk.Label(
        main_container, 
        text=f"{APP_NAME} {VERSION}", 
        font=("Segoe UI", 14, "bold")
    ).pack(pady=20)
    
    # Primary action button
    ttk.Button(
        main_container, 
        text="Open Image", 
        command=open_image_file
    ).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    initialize_application()
from PIL import Image
import os

def resize_image(image_path, output_path, width, height):
    try:
        with Image.open(image_path) as img:
            img_resized = img.resize((width, height))
            img_resized.save(output_path)
            print(f"Image resized and saved to {output_path}")
    except Exception as e:
        print(f"Error resizing image: {e}")

def convert_image_format(image_path, output_path, format):
    try:
        with Image.open(image_path) as img:
            img.convert("RGB").save(output_path, format=format)
            print(f"Image converted to {format} format and saved to {output_path}")
    except Exception as e:
        print(f"Error converting image format: {e}")

def main():
    print("Welcome to the Image Resizer and Format Converter!")
    print("Choose an option:")
    print("1. Resize an image")
    print("2. Convert image format")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        image_path = input("Enter the path of the image to resize: ")
        output_path = input("Enter the output path for the resized image: ")
        width = int(input("Enter the new width: "))
        height = int(input("Enter the new height: "))
        resize_image(image_path, output_path, width, height)

    elif choice == "2":
        image_path = input("Enter the path of the image to convert: ")
        output_path = input("Enter the output path for the converted image: ")
        format = input("Enter the new format (e.g., JPEG, PNG): ")
        convert_image_format(image_path, output_path, format)

    else:
        print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main()

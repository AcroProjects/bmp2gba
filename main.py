import tkinter as tk
from tkinter import filedialog
import cv2
import pyperclip
from PIL import Image, ImageTk

# Image's hex array
hex_array = []

def color_to_gba(pixel):
    B, G, R = pixel

    color_hex = "#{:02x}{:02x}{:02x}".format(R, G, B)

    # Remove '#' if present
    color_hex = color_hex.lstrip('#')

    # Convert hexadecimal color string to RGB values
    R = int(color_hex[0:2], 16)
    G = int(color_hex[2:4], 16)
    B = int(color_hex[4:6], 16)

    # Map RGB values to the BGR555 format
    # BGR555 is the appropriate color format for the GBA
    bgr555_value = (R >> 3) | ((G >> 3) << 5) | ((B >> 3) << 10)

    # Convert the BGR555 value to a string representation
    bgr555_str = format(bgr555_value, '04x')

    return "0x" + bgr555_str.upper()

def show_image(filepath):
    img = cv2.imread(filepath)
    height, width = img.shape[:2]

    screen_height = 720

    aspect_ratio = width / height

    screen_width = int(screen_height * aspect_ratio)

    resized_img = cv2.resize(img, (screen_width, screen_height),interpolation=cv2.INTER_NEAREST)

    # Convert image to proper size for window
    img_rgb = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)

    # Update the label with the image
    label.config(image=img_tk)
    label.image = img_tk  # Keep a reference to avoid garbage collection

    # Resize window
    window.geometry(f"{img_pil.width}x{img_pil.height}")

def convert_image_data(filepath):
    # Read image file
    img = cv2.imread(filepath)

    if img is None:
        return

    # Grab the image height and width
    columns, rows = img.shape[:2]

    # Make hex array empty for the image's hex values
    global hex_array
    hex_array = []

    # Loop through every row of pixels
    for x in range(rows):
        # Loop through every column of pixels
        for y in range(columns):
            # Grab a pixel of the image file, convert its RGB values to its BGR555 hex value, and append that to the hex array
            hex_array.append(color_to_gba(img[x,y]))

    show_image(filepath)

def get_filepath():
    filepath = filedialog.askopenfilename()
    convert_image_data(filepath)

def copy_hex_values():
    # Text that will be copied for the use to paste in their projects
    copied_text = ""

    values_added = 0

    # Loop through all the values in the hex array
    for value in hex_array:
        values_added += 1
        # Add hex value to the copied_text string
        copied_text += str(value) + ","
        if values_added == 8:
            copied_text += "\n"
            values_added = 0

    copied_text = copied_text[:-1]

    pyperclip.copy(copied_text)

window = tk.Tk()
window.title("BMP Image To GBA Hex")
window.geometry("450x250")

button = tk.Button(text="Open Image", command=get_filepath)
button.pack()

button2 = tk.Button(text="Copy GBA Hex Values", command=copy_hex_values)
button2.pack()

label = tk.Label(window)
label.pack()

window.mainloop()


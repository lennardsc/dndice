import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from roll import roll

def roll_dice():
    roll_input = entry.get()
    result, rolls = roll(roll_input)
    if result is not None:
        messagebox.showinfo("Roll Result", f"Rolls: {', '.join(map(str, rolls))}\nTotal: {result}")
    else:
        messagebox.showerror("Error", f"An error occurred: {rolls}")

# Create main window
root = tk.Tk()
root.title("Dice Roller")

# Create label
label = tk.Label(root, text="Enter dice roll (e.g. 2d6):")
label.pack()

# Load and display image
image = Image.open("assets/dice_elf.png")
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(root, image=photo)
image_label.image = photo  # to keep reference
image_label.pack(side=tk.LEFT)

# Create entry
entry = tk.Entry(root, width=20)
entry.pack(side=tk.LEFT)

# Create roll button
roll_button = tk.Button(root, text="Roll", command=roll_dice)
roll_button.pack()

# Run the main event loop
root.mainloop()

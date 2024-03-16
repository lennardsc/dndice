import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from roll import roll
from storage import DiceRollStorage

def roll_dice():
    roll_input = entry.get()
    result, rolls = roll(roll_input)
    if result is not None:
        if result == 1:
            sad_image = Image.open("assets/dice_elf_sad.png")
            sad_photo = ImageTk.PhotoImage(sad_image)
            sad_label = tk.Label(root, image=sad_photo)
            sad_label.image = sad_photo
            sad_label.pack(side=tk.LEFT)
        elif result == 20:
            happy_image = Image.open("assets/dice_elf_happy.png")
            happy_photo = ImageTk.PhotoImage(happy_image)
            happy_label = tk.Label(root, image=happy_photo)
            happy_label.image = happy_photo
            happy_label.pack(side=tk.LEFT)

        messagebox.showinfo("Roll Result", f"Rolls: {', '.join(map(str, rolls))}\nTotal: {result}")
        storage.insert_roll(roll_input, result)
    else:
        messagebox.showerror("Error", f"An error occurred: {rolls}")


# Create main window
root = tk.Tk()
root.title("Dice Roller")

# Connect to database
storage = DiceRollStorage("dice_rolls.db")

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

# Close database connection
storage.close_connection()

import tkinter as tk
from tkinter import messagebox
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

# Create entry
entry = tk.Entry(root, width=20)
entry.pack()

# Create roll button
roll_button = tk.Button(root, text="Roll", command=roll_dice)
roll_button.pack()

# Run the main event loop
root.mainloop()

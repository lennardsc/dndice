import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from roll import roll
from storage import DiceRollStorage
from analysis import RollAnalysis
import tkinter.scrolledtext as scrolledtext
import requests

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
        elif result == 69:
            result69_image = Image.open("assets/dice_elf_69.png")
            result69_photo = ImageTk.PhotoImage(result69_image)
            result69_label = tk.Label(root, image=result69_photo)
            result69_label.image = result69_photo
            result69_label.pack(side=tk.LEFT)
        elif result == 42:
            result42_image = Image.open("assets/dice_elf_42.png")
            result42_photo = ImageTk.PhotoImage(result42_image)
            result42_label = tk.Label(root, image=result42_photo)
            result42_label.image = result42_photo
            result42_label.pack(side=tk.LEFT)

        messagebox.showinfo("Roll Result", f"Rolls: {', '.join(map(str, rolls))}\nTotal: {result}")
        storage.insert_roll(roll_input, result)
    else:
        messagebox.showerror("Error", f"An error occurred: {rolls}")

def analyze():
    analysis = RollAnalysis("dice_rolls.db")
    analysis.highest_lowest_median_by_day()
    analysis.count_median_1_by_day()
    analysis.count_20_by_day()
    analysis.close_connection()

def view_license():
    license_url = "https://codeberg.org/lennardsc/dndice/raw/commit/33ab768ab57d3f6af621a9acdca5f79d107f6fd1/LICENSE"
    response = requests.get(license_url)

    if response.status_code == 200:
        license_content = response.text

        # Create a new Toplevel window to display the license
        license_window = tk.Toplevel(root)
        license_window.title("License")

        # Create a scrolled text widget to display the license content
        license_text = scrolledtext.ScrolledText(license_window, wrap=tk.WORD, width=80, height=30)
        license_text.insert(tk.END, license_content)
        license_text.pack(expand=True, fill=tk.BOTH)

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

# Create analyze button
analyze_button = tk.Button(root, text="Analyze", command=analyze)
analyze_button.pack()

view_license_button = tk.Button(root, text="View License", command=view_license)
view_license_button.pack()

# Run the main event loop
root.mainloop()

# Close database connection
storage.close_connection()

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import tkinter.scrolledtext as scrolledtext
from roll import roll
from storage import DiceRollStorage
from analysis import RollAnalysis
from charaktersheet import CharacterSheet

def roll_dice():
    """Rolls the dice based on user input and displays the result."""
    roll_input = entry.get()
    result, rolls = roll(roll_input)

    # Display dice elf image based on result
    if result == 1:
        image_path = "assets/dice_elf_sad.png"
    elif result == 20:
        image_path = "assets/dice_elf_happy.png"
    elif result == 69:
        image_path = "assets/dice_elf_69.png"
    elif result == 42:
        image_path = "assets/dice_elf_42.png"
    elif result == 21:
        image_path = "assets/dice_elf_21.png"
    elif result == 18:
        image_path = "assets/dice_elf_18.png"
    else:
        image_path = "assets/dice_elf.png"

    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    image_label.configure(image=photo)
    image_label.image = photo

    # Show roll result
    if result is not None:
        messagebox.showinfo("Roll Result", f"Rolls: {', '.join(map(str, rolls))}\nTotal: {result}")
        storage.insert_roll(roll_input, result)
    else:
        messagebox.showerror("Error", f"An error occurred: {rolls}")

def analyze():
    """Performs analysis on dice rolls and displays the results."""
    analysis = RollAnalysis("dice_rolls.db")
    analysis.highest_lowest_median_by_day()
    analysis.count_median_1_by_day()
    analysis.count_20_by_day()
    analysis.close_connection()

def view_license():
    """Displays the license text in a new window."""
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
def open_charaktersheets():
    char_sheet_window = tk.Toplevel(root)
    char_sheet_window.title("Character Sheets")

    char_sheet_app = CharacterSheet(char_sheet_window)

# Create main window
root = tk.Tk()
root.title("DNDICE")

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

charaktersheets_button = tk.Button(root, text="Character Sheets", command=open_charaktersheets)
charaktersheets_button.pack()

# Create view license button
view_license_button = tk.Button(root, text="View License", command=view_license)
view_license_button.pack()


# Run the main event loop
root.mainloop()

# Close database connection
storage.close_connection()

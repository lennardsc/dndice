import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import json

# Charakterdaten speichern
character = {"Stärke": 0, "Geschicklichkeit": 0, "Intelligenz": 0}

def roll_dice():
    try:
        # Würfeltyp und Anzahl der Würfe abrufen
        dice_type = int(dice_type_entry.get())
        rolls = int(rolls_entry.get())
        attribute = attribute_var.get()

        if dice_type <= 0 or rolls <= 0:
            raise ValueError("Die Werte müssen positive ganze Zahlen sein!")

        # Attributsbonus abrufen
        bonus = character.get(attribute, 0)

        # Würfeln
        results = [random.randint(1, dice_type) + bonus for _ in range(rolls)]
        total = sum(results)

        # Ergebnisse anzeigen
        results_text.set(f"Ergebnisse: {results}")
        total_text.set(f"Gesamtsumme (mit Bonus): {total}")

    except ValueError:
        messagebox.showerror("Fehler", "Bitte geben Sie gültige positive ganze Zahlen ein!")

def update_character():
    try:
        character["Stärke"] = int(strength_entry.get())
        character["Geschicklichkeit"] = int(dexterity_entry.get())
        character["Intelligenz"] = int(intelligence_entry.get())
        messagebox.showinfo("Charakter-Update", "Charakterwerte wurden aktualisiert!")
    except ValueError:
        messagebox.showerror("Fehler", "Bitte geben Sie gültige Werte für die Attribute ein!")

def save_character():
    with open("character.json", "w") as file:
        json.dump(character, file)
    messagebox.showinfo("Speichern", "Charakter gespeichert!")

def load_character():
    global character
    try:
        with open("character.json", "r") as file:
            character = json.load(file)
        strength_entry.delete(0, tk.END)
        dexterity_entry.delete(0, tk.END)
        intelligence_entry.delete(0, tk.END)
        strength_entry.insert(0, character["Stärke"])
        dexterity_entry.insert(0, character["Geschicklichkeit"])
        intelligence_entry.insert(0, character["Intelligenz"])
        messagebox.showinfo("Laden", "Charakter geladen!")
    except FileNotFoundError:
        messagebox.showerror("Fehler", "Keine gespeicherte Datei gefunden!")

# Hauptfenster erstellen
root = tk.Tk()
root.title("DnD-Würfel-Simulator mit Hintergrundbild")
root.geometry("800x600")

# Hintergrundbild laden
background_image = Image.open("dndice.jpg")  # Bilddatei angeben
background_image = background_image.resize((800, 600))  # Bildgröße anpassen
background_photo = ImageTk.PhotoImage(background_image)

# Hintergrundbild als Label
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Charakter-Frame
character_frame = tk.Frame(root, bg="#f3e5ab", padx=10, pady=10)
character_frame.place(x=10, y=10, width=250, height=250)

tk.Label(character_frame, text="Charakterwerte", font=("Arial", 14), bg="#f3e5ab").pack()
tk.Label(character_frame, text="Stärke:", bg="#f3e5ab").pack()
strength_entry = tk.Entry(character_frame)
strength_entry.pack()
tk.Label(character_frame, text="Geschicklichkeit:", bg="#f3e5ab").pack()
dexterity_entry = tk.Entry(character_frame)
dexterity_entry.pack()
tk.Label(character_frame, text="Intelligenz:", bg="#f3e5ab").pack()
intelligence_entry = tk.Entry(character_frame)
intelligence_entry.pack()

update_button = tk.Button(character_frame, text="Charakter aktualisieren", command=update_character)
update_button.pack(pady=5)
save_button = tk.Button(character_frame, text="Charakter speichern", command=save_character)
save_button.pack(pady=5)
load_button = tk.Button(character_frame, text="Charakter laden", command=load_character)
load_button.pack(pady=5)

# Würfel-Frame
dice_frame = tk.Frame(root, bg="#f3e5ab", padx=20, pady=20)
dice_frame.place(x=300, y=10, width=480, height=200)

tk.Label(dice_frame, text="Würfeltyp (z.B. 6 für d6):", bg="#f3e5ab").grid(row=0, column=0, sticky="w")
dice_type_entry = tk.Entry(dice_frame)
dice_type_entry.grid(row=0, column=1)

tk.Label(dice_frame, text="Anzahl der Würfe:", bg="#f3e5ab").grid(row=1, column=0, sticky="w")
rolls_entry = tk.Entry(dice_frame)
rolls_entry.grid(row=1, column=1)

tk.Label(dice_frame, text="Attribut auswählen:", bg="#f3e5ab").grid(row=2, column=0, sticky="w")
attribute_var = tk.StringVar(value="Stärke")
attribute_menu = tk.OptionMenu(dice_frame, attribute_var, "Stärke", "Geschicklichkeit", "Intelligenz")
attribute_menu.grid(row=2, column=1)

roll_button = tk.Button(dice_frame, text="Würfeln", command=roll_dice)
roll_button.grid(row=3, column=0, pady=10)

# Ergebnisse
results_text = tk.StringVar()
total_text = tk.StringVar()

tk.Label(dice_frame, textvariable=results_text, bg="#f3e5ab", fg="blue").grid(row=4, column=0, columnspan=2, sticky="w")
tk.Label(dice_frame, textvariable=total_text, bg="#f3e5ab", fg="green").grid(row=5, column=0, columnspan=2, sticky="w")

# Hauptschleife starten
root.mainloop()

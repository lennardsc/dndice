import tkinter as tk
from tkinter import messagebox
import random
import json

# Globale Variablen
characters = {}
current_character = None

def roll_dice():
    try:
        if not current_character:
            raise ValueError("Kein Charakter ausgewählt!")

        # Würfeltyp und Anzahl der Würfe abrufen
        dice_type = int(dice_type_entry.get())
        rolls = int(rolls_entry.get())
        attribute = attribute_var.get()

        if dice_type <= 0 or rolls <= 0:
            raise ValueError("Die Werte müssen positive ganze Zahlen sein!")

        # Attributsbonus abrufen
        bonus = characters[current_character].get(attribute, 0)

        # Würfeln
        results = [random.randint(1, dice_type) + bonus for _ in range(rolls)]
        total = sum(results)

        # Ergebnisse anzeigen
        results_text.set(f"Ergebnisse: {results}")
        total_text.set(f"Gesamtsumme (mit Bonus): {total}")

    except ValueError as e:
        messagebox.showerror("Fehler", str(e))

def update_character():
    global characters
    try:
        if not current_character:
            raise ValueError("Kein Charakter ausgewählt!")

        characters[current_character]["Stärke"] = int(strength_entry.get())
        characters[current_character]["Geschicklichkeit"] = int(dexterity_entry.get())
        characters[current_character]["Intelligenz"] = int(intelligence_entry.get())
        messagebox.showinfo("Charakter-Update", f"{current_character} wurde aktualisiert!")
    except ValueError:
        messagebox.showerror("Fehler", "Bitte geben Sie gültige Werte für die Attribute ein!")

def save_characters():
    with open("characters.json", "w") as file:
        json.dump(characters, file)
    messagebox.showinfo("Speichern", "Alle Charaktere wurden gespeichert!")

def load_characters():
    global characters, current_character
    try:
        with open("characters.json", "r") as file:
            characters = json.load(file)
        if characters:
            current_character = list(characters.keys())[0]  # Wähle den ersten Charakter
            update_character_display()
            update_character_dropdown()
            messagebox.showinfo("Laden", "Charaktere wurden geladen!")
        else:
            messagebox.showinfo("Laden", "Keine gespeicherten Charaktere gefunden!")
    except FileNotFoundError:
        messagebox.showinfo("Laden", "Keine gespeicherten Charaktere gefunden!")

def add_character():
    global characters, current_character
    new_name = new_character_entry.get().strip()
    if new_name in characters or not new_name:
        messagebox.showerror("Fehler", "Ungültiger oder bereits vorhandener Charaktername!")
        return
    characters[new_name] = {"Stärke": 0, "Geschicklichkeit": 0, "Intelligenz": 0}
    current_character = new_name
    update_character_display()
    update_character_dropdown()
    messagebox.showinfo("Charakter hinzufügen", f"{new_name} wurde hinzugefügt!")

def delete_character():
    global characters, current_character
    if not current_character:
        messagebox.showerror("Fehler", "Kein Charakter ausgewählt!")
        return
    del characters[current_character]
    if characters:
        current_character = list(characters.keys())[0]  # Wähle den nächsten Charakter
    else:
        current_character = None
    update_character_display()
    update_character_dropdown()
    messagebox.showinfo("Charakter löschen", "Charakter wurde gelöscht!")

def update_character_display():
    if current_character:
        strength_entry.delete(0, tk.END)
        strength_entry.insert(0, characters[current_character]["Stärke"])
        dexterity_entry.delete(0, tk.END)
        dexterity_entry.insert(0, characters[current_character]["Geschicklichkeit"])
        intelligence_entry.delete(0, tk.END)
        intelligence_entry.insert(0, characters[current_character]["Intelligenz"])
        character_label.set(f"Aktueller Charakter: {current_character}")
    else:
        strength_entry.delete(0, tk.END)
        dexterity_entry.delete(0, tk.END)
        intelligence_entry.delete(0, tk.END)
        character_label.set("Kein Charakter ausgewählt")

def update_character_dropdown():
    character_dropdown["menu"].delete(0, "end")
    for char in characters:
        character_dropdown["menu"].add_command(label=char, command=lambda c=char: select_character(c))
    if characters:
        current_character_var.set(current_character)
    else:
        current_character_var.set("")

def select_character(name):
    global current_character
    current_character = name
    update_character_display()

# Hauptfenster erstellen
root = tk.Tk()
root.title("DnD-Würfel-Simulator mit Charakterverwaltung")
root.geometry("800x600")

# Charakter-Frame
character_frame = tk.Frame(root, padx=10, pady=10)
character_frame.pack(side="left", fill="y")

character_label = tk.StringVar(value="Kein Charakter ausgewählt")
tk.Label(character_frame, textvariable=character_label, font=("Arial", 14)).pack()

tk.Label(character_frame, text="Stärke:").pack()
strength_entry = tk.Entry(character_frame)
strength_entry.pack()
tk.Label(character_frame, text="Geschicklichkeit:").pack()
dexterity_entry = tk.Entry(character_frame)
dexterity_entry.pack()
tk.Label(character_frame, text="Intelligenz:").pack()
intelligence_entry = tk.Entry(character_frame)
intelligence_entry.pack()

update_button = tk.Button(character_frame, text="Charakter aktualisieren", command=update_character)
update_button.pack(pady=5)

tk.Label(character_frame, text="Neuer Charaktername:").pack()
new_character_entry = tk.Entry(character_frame)
new_character_entry.pack()
add_button = tk.Button(character_frame, text="Charakter hinzufügen", command=add_character)
add_button.pack(pady=5)
delete_button = tk.Button(character_frame, text="Charakter löschen", command=delete_character)
delete_button.pack(pady=5)

save_button = tk.Button(character_frame, text="Charaktere speichern", command=save_characters)
save_button.pack(pady=5)
load_button = tk.Button(character_frame, text="Charaktere laden", command=load_characters)
load_button.pack(pady=5)

# Dropdown-Menü für Charaktere
current_character_var = tk.StringVar(value="")
character_dropdown = tk.OptionMenu(character_frame, current_character_var, "")
character_dropdown.pack()

# Würfel-Frame
dice_frame = tk.Frame(root, padx=20, pady=20)
dice_frame.pack(side="right", fill="both", expand=True)

tk.Label(dice_frame, text="Würfeltyp (z.B. 6 für d6):").grid(row=0, column=0, sticky="w")
dice_type_entry = tk.Entry(dice_frame)
dice_type_entry.grid(row=0, column=1)

tk.Label(dice_frame, text="Anzahl der Würfe:").grid(row=1, column=0, sticky="w")
rolls_entry = tk.Entry(dice_frame)
rolls_entry.grid(row=1, column=1)

tk.Label(dice_frame, text="Attribut auswählen:").grid(row=2, column=0, sticky="w")
attribute_var = tk.StringVar(value="Stärke")
attribute_menu = tk.OptionMenu(dice_frame, attribute_var, "Stärke", "Geschicklichkeit", "Intelligenz")
attribute_menu.grid(row=2, column=1)

roll_button = tk.Button(dice_frame, text="Würfeln", command=roll_dice)
roll_button.grid(row=3, column=0, pady=10)

# Ergebnisse
results_text = tk.StringVar()
total_text = tk.StringVar()

tk.Label(dice_frame, textvariable=results_text, fg="blue").grid(row=4, column=0, columnspan=2, sticky="w")
tk.Label(dice_frame, textvariable=total_text, fg="green").grid(row=5, column=0, columnspan=2, sticky="w")

# Hauptschleife starten
load_characters()  # Charaktere beim Start laden
root.mainloop()

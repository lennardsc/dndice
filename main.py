import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Für erweiterte Bildunterstützung
import random

def roll_dice():
    try:
        # Würfeltyp und Anzahl der Würfe abrufen
        dice_type = int(dice_type_entry.get())
        rolls = int(rolls_entry.get())

        if dice_type <= 0 or rolls <= 0:
            raise ValueError("Die Werte müssen positive ganze Zahlen sein!")

        # Würfeln
        results = [random.randint(1, dice_type) for _ in range(rolls)]
        total = sum(results)

        # Ergebnisse anzeigen
        results_text.set(f"Ergebnisse: {results}")
        total_text.set(f"Gesamtsumme: {total}")

    except ValueError:
        messagebox.showerror("Fehler", "Bitte geben Sie gültige positive ganze Zahlen ein!")

def reset_fields():
    # Eingabefelder und Ergebnisfelder zurücksetzen
    dice_type_entry.delete(0, tk.END)
    rolls_entry.delete(0, tk.END)
    results_text.set("")
    total_text.set("")

# Hauptfenster erstellen
root = tk.Tk()
root.title("DnD-Würfel-Simulator")

# Fenstergröße festlegen
root.geometry("800x600")

# Hintergrundbild laden
background_image = Image.open("dndice.jpg")  # Bilddatei angeben
background_image = background_image.resize((800, 600))  # Größe anpassen
background_photo = ImageTk.PhotoImage(background_image)

# Hintergrundbild in das Fenster einfügen
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Haupt-Frame für die Eingaben und Ergebnisse
frame = tk.Frame(root, bg="#f3e5ab", padx=20, pady=20, relief=tk.RAISED)
frame.place(relx=0.5, rely=0.5, anchor="center")  # Zentriert

# Eingabefelder
tk.Label(frame, text="Würfeltyp (z.B. 6 für d6, 20 für d20):", bg="#f3e5ab").grid(row=0, column=0, sticky="w")
dice_type_entry = tk.Entry(frame, width=10)
dice_type_entry.grid(row=0, column=1)

tk.Label(frame, text="Anzahl der Würfe:", bg="#f3e5ab").grid(row=1, column=0, sticky="w")
rolls_entry = tk.Entry(frame, width=10)
rolls_entry.grid(row=1, column=1)

# Buttons
roll_button = tk.Button(frame, text="Würfeln", command=roll_dice)
roll_button.grid(row=2, column=0, pady=10)

reset_button = tk.Button(frame, text="Zurücksetzen", command=reset_fields)
reset_button.grid(row=2, column=1, pady=10)

# Ergebnisse
results_text = tk.StringVar()
total_text = tk.StringVar()

tk.Label(frame, textvariable=results_text, bg="#f3e5ab", fg="blue").grid(row=3, column=0, columnspan=2, sticky="w")
tk.Label(frame, textvariable=total_text, bg="#f3e5ab", fg="green").grid(row=4, column=0, columnspan=2, sticky="w")

# Hauptschleife starten
root.mainloop()

import tkinter as tk
from tkinter import messagebox

class CharacterSheet:
    def __init__(self, root):
        self.root = root
        self.charakter_sheets = {}

    def create_charakter_sheet(self, name):
        if name in self.charakter_sheets:
            messagebox.showwarning("Warning", "Character sheet already exists.")
        else:
            self.charakter_sheets[name] = {
                "Name": name,
                "Class": "",
                "Race": "",
                "Level": 1,
                "Attributes": {
                    "Strength": 10,
                    "Dexterity": 10,
                    "Constitution": 10,
                    "Intelligence": 10,
                    "Wisdom": 10,
                    "Charisma": 10
                }
                # Add more fields as needed
            }
            messagebox.showinfo("Success", f"Character sheet '{name}' created successfully.")

    def view_charakter_sheet(self, name):
        if name in self.charakter_sheets:
            sheet_info = "\n".join([f"{key}: {value}" for key, value in self.charakter_sheets[name].items()])
            messagebox.showinfo("Character Sheet", sheet_info)
        else:
            messagebox.showerror("Error", "Character sheet not found.")

    def edit_charakter_sheet(self, name, attribute, value):
        if name in self.charakter_sheets:
            if attribute in self.charakter_sheets[name]:
                self.charakter_sheets[name][attribute] = value
                messagebox.showinfo("Success", f"Character sheet '{name}' updated successfully.")
            else:
                messagebox.showerror("Error", f"Attribute '{attribute}' not found in character sheet.")
        else:
            messagebox.showerror("Error", "Character sheet not found.")

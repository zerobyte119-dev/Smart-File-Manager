import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

class AdvancedOrganizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pro File Master v2.0")
        self.root.geometry("450x350")
        
        # State: Start with Dark Mode
        self.dark_mode = True
        
        # Theme Colors
        self.colors = {
            'dark':  {'bg': "#2c3e50", 'fg': "#ecf0f1", 'btn': "#e74c3c", 'lbl': "#bdc3c7"},
            'light': {'bg': "#f5f5f5", 'fg': "#2c3e50", 'btn': "#3498db", 'lbl': "#7f8c8d"}
        }

        self.categories = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif'],
            'Docs': ['.pdf', '.docx', '.txt', '.xlsx'],
            'Media': ['.mp4', '.mov', '.mp3'],
            'Archives': ['.zip', '.rar']
        }

        self.setup_ui()

    def setup_ui(self):
        self.apply_theme()

    def apply_theme(self):
        theme = self.colors['dark'] if self.dark_mode else self.colors['light']
        self.root.configure(bg=theme['bg'])

        # Clear existing widgets to redraw
        for widget in self.root.winfo_children():
            widget.destroy()

        # Theme Toggle Button (Top Right)
        mode_text = "🌙 Dark" if self.dark_mode else "☀️ Light"
        tk.Button(self.root, text=mode_text, command=self.toggle_theme,
                  bg=theme['bg'], fg=theme['fg'], bd=1).pack(anchor="ne", padx=10, pady=5)

        # Header
        tk.Label(self.root, text="PRO FILE MASTER", 
                 fg=theme['fg'], bg=theme['bg'], font=("Arial", 18, "bold")).pack(pady=10)

        # Description
        tk.Label(self.root, text="Select a folder to organize instantly", 
                 fg=theme['lbl'], bg=theme['bg']).pack()

        # Main Button
        tk.Button(self.root, text="ORGANIZE NOW", command=self.start_process,
                  bg=theme['btn'], fg="white", font=("Arial", 12, "bold"),
                  padx=30, pady=15, relief="flat", cursor="hand2").pack(pady=40)

        # Footer
        tk.Label(self.root, text=f"Last Log: {datetime.now().strftime('%H:%M')}", 
                 fg=theme['lbl'], bg=theme['bg'], font=("Arial", 8)).pack(side="bottom", pady=10)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def start_process(self):
        target_path = filedialog.askdirectory()
        if not target_path: return

        try:
            count = 0
            for filename in os.listdir(target_path):
                filepath = os.path.join(target_path, filename)
                if os.path.isdir(filepath): continue

                file_ext = os.path.splitext(filename)[1].lower()
                for category, exts in self.categories.items():
                    if file_ext in exts:
                        dest_folder = os.path.join(target_path, category)
                        os.makedirs(dest_folder, exist_ok=True)
                        shutil.move(filepath, os.path.join(dest_folder, filename))
                        count += 1
                        break
            
            messagebox.showinfo("Success", f"Moved {count} files!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedOrganizer(root)
    root.mainloop()
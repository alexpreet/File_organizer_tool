import os
import shutil
import customtkinter as ctk
from tkinter import filedialog, scrolledtext

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx"],
    "Audio": [".mp3", ".wav"],
    "Archives": [".zip", ".rar"],
    "Code": [".py", ".js", ".html", ".css"]
}

class FileOrganizerApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("File Organizer Tool")
        self.geometry("600x700")
        self.resizable(True, True)

        self.folder_path = ctk.StringVar()

        ctk.CTkLabel(self, text="File Organizer Tool",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=15)

        self.entry = ctk.CTkEntry(self, textvariable=self.folder_path, width=400)
        self.entry.pack(pady=10)

        ctk.CTkButton(self, text="Browse Folder", command=self.select_folder).pack(pady=5)

        self.organize_btn = ctk.CTkButton(
            self, text="Organize Files", command=self.organize_files
        )
        self.organize_btn.pack(pady=15)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=10)

        # Add scrolled text area to show detailed file movements
        ctk.CTkLabel(self, text="Organization Details:",
                     font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=15)
        
        self.output_text = scrolledtext.ScrolledText(
            self, height=15, width=70, bg="#1a1a1a", fg="#ffffff", 
            font=("Courier", 9), wrap="word"
        )
        self.output_text.pack(padx=15, pady=10, fill="both", expand=True)
        self.output_text.config(state="disabled")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
            self.status_label.configure(text="Folder selected.")

    def organize_files(self):
        folder = self.folder_path.get()
        if not folder:
            self.status_label.configure(text="Please select a folder first.")
            return

        try:
            # Track organization statistics
            category_stats = {cat: 0 for cat in FILE_TYPES}
            category_stats["Others"] = 0
            total_files = 0
            moved_files = []

            self.status_label.configure(text="Organizing files... ⏳")
            self.update()

            for file in os.listdir(folder):
                path = os.path.join(folder, file)
                if os.path.isfile(path):
                    total_files += 1
                    ext = os.path.splitext(file)[1].lower()
                    moved = False

                    # Try to match file to a category
                    for category, extensions in FILE_TYPES.items():
                        if ext in extensions:
                            dest = os.path.join(folder, category)
                            os.makedirs(dest, exist_ok=True)
                            shutil.move(path, os.path.join(dest, file))
                            category_stats[category] += 1
                            moved_files.append(f"✓ {file} → {category}/")
                            moved = True
                            break

                    # Move unmatched files to Others
                    if not moved:
                        other = os.path.join(folder, "Others")
                        os.makedirs(other, exist_ok=True)
                        shutil.move(path, os.path.join(other, file))
                        category_stats["Others"] += 1
                        moved_files.append(f"✓ {file} → Others/")

            # Build detailed report
            report = f"{'='*60}\n"
            report += f"FILE ORGANIZATION REPORT\n"
            report += f"{'='*60}\n\n"
            report += f"Folder: {folder}\n"
            report += f"Total files organized: {total_files}\n\n"
            report += f"SUMMARY BY CATEGORY:\n"
            report += f"{'-'*60}\n"
            for cat, count in category_stats.items():
                if count > 0:
                    report += f"{cat}: {count} file(s)\n"
            report += f"\n{'-'*60}\n"
            report += f"DETAILED FILE MOVEMENTS:\n"
            report += f"{'-'*60}\n"
            for entry in moved_files:
                report += f"{entry}\n"
            report += f"{'='*60}\n"

            # Display in text area
            self.output_text.config(state="normal")
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", report)
            self.output_text.config(state="disabled")

            self.status_label.configure(text=f"✅ Organized {total_files} files successfully!")

        except Exception as e:
            self.status_label.configure(text=f"Error: {e}")
            self.output_text.config(state="normal")
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", f"Error during organization:\n{str(e)}")
            self.output_text.config(state="disabled")

if __name__ == "__main__":
    app = FileOrganizerApp()
    app.mainloop()

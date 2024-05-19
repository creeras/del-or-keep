import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import pygame

class FileReviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Review App")
        self.root.geometry("800x500")
        self.root.resizable(False, False)  # 창 크기 고정

        self.folder_path = ""
        self.files = []
        self.current_file_index = 0

        pygame.init()
        self.music_player = pygame.mixer.music

        self.label = tk.Label(root, text="Select a folder to start", font=("Helvetica", 32))
        self.label.place(relx=0.5, rely=0.1, anchor="center")

        self.select_folder_button = tk.Button(root, text="Select Folder", command=self.select_folder, font=("Helvetica", 24))
        self.select_folder_button.place(relx=0.5, rely=0.2, anchor="center")

        self.file_label = tk.Label(root, text="", font=("Helvetica", 28), wraplength=700, justify="center")
        self.file_label.place(relx=0.5, rely=0.5, anchor="center")

        button_frame = tk.Frame(root)
        button_frame.place(relx=0.5, rely=0.8, anchor="center")

        self.keep_button = tk.Button(button_frame, text="Keep", command=self.keep_file, state=tk.DISABLED, font=("Helvetica", 24), width=10, height=2, bg="blue")
        self.keep_button.grid(row=0, column=0, padx=20)

        self.music_button = tk.Button(button_frame, text="Play Music", command=self.toggle_music, state=tk.DISABLED, font=("Helvetica", 24), width=10, height=2, bg="green")
        self.music_button.grid(row=0, column=1, padx=20)

        self.delete_button = tk.Button(button_frame, text="Delete", command=self.delete_file, state=tk.DISABLED, font=("Helvetica", 24), width=10, height=2, bg="red")
        self.delete_button.grid(row=0, column=2, padx=20)

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.files = os.listdir(self.folder_path)
            self.files = [f for f in self.files if os.path.isfile(os.path.join(self.folder_path, f))]
            self.current_file_index = 0
            if self.files:
                self.update_file_label()
                self.keep_button.config(state=tk.NORMAL)
                self.music_button.config(state=tk.NORMAL)
                self.delete_button.config(state=tk.NORMAL)
            else:
                messagebox.showinfo("Info", "The selected folder is empty.")

    def update_file_label(self):
        if self.current_file_index < len(self.files):
            current_file = self.files[self.current_file_index]
            self.file_label.config(text=f"File: {current_file}")
        else:
            self.file_label.config(text="No more files.")
            self.keep_button.config(state=tk.DISABLED)
            self.music_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)

    def keep_file(self):
        self.current_file_index += 1
        self.update_file_label()

    def toggle_music(self):
        current_file = self.files[self.current_file_index]
        file_path = os.path.join(self.folder_path, current_file)
        if self.music_player.get_busy():
            self.music_player.stop()
            self.music_button.config(text="Play Music", bg="green")
        else:
            self.music_player.load(file_path)
            self.music_player.play()
            self.music_button.config(text="Stop Music", bg="orange")

    def delete_file(self):
        if self.music_player.get_busy():
            self.music_player.stop()
        current_file = self.files[self.current_file_index]
        file_path = os.path.join(self.folder_path, current_file)
        self.music_player.unload() # 파일 재생을 중지하고 파일을 닫음
        os.remove(file_path)
        self.current_file_index += 1
        self.update_file_label()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileReviewApp(root)
    root.mainloop()

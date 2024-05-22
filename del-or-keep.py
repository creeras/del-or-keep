import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

class FileReviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Del or Keep")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        self.folder_path = ""
        self.files = []
        self.current_file_index = 0

        pygame.init()
        self.music_player = pygame.mixer.music

        self.label = tk.Label(root, text="Select a folder to start", font=("Helvetica", 32))
        self.label.place(relx=0.5, rely=0.05, anchor="center")

        self.select_folder_button = tk.Button(root, text="Select Folder", command=self.select_folder, font=("Helvetica", 20), width=15)
        self.select_folder_button.place(relx=0.5, rely=0.15, anchor="center")

        self.separator = tk.Frame(root, height=2, bd=1, relief="groove")
        self.separator.place(relx=0.5, rely=0.25, anchor="center", relwidth=0.9)

        self.previous_button = tk.Button(root, text="Previous File", command=self.go_back, state=tk.DISABLED, font=("Helvetica", 20), width=15)
        self.previous_button.place(relx=0.5, rely=0.35, anchor="center")

        self.file_label = tk.Label(root, text="", font=("Helvetica", 28), wraplength=700, justify="center")
        self.file_label.place(relx=0.5, rely=0.55, anchor="center")

        self.artist_label = tk.Label(root, text="", font=("Helvetica", 20), wraplength=700, justify="center", fg="gray")
        self.artist_label.place(relx=0.5, rely=0.65, anchor="center")

        button_frame = tk.Frame(root)
        button_frame.place(relx=0.5, rely=0.8, anchor="center")

        self.keep_button = tk.Button(button_frame, text="Keep", command=self.keep_file, state=tk.DISABLED, font=("Helvetica", 20), width=10, height=2, bg="blue")
        self.keep_button.grid(row=0, column=0, padx=20)

        self.music_button = tk.Button(button_frame, text="Play Music", command=self.toggle_music, state=tk.DISABLED, font=("Helvetica", 20), width=10, height=2, bg="green")
        self.music_button.grid(row=0, column=1, padx=20)

        self.delete_button = tk.Button(button_frame, text="Delete", command=self.delete_file, state=tk.DISABLED, font=("Helvetica", 20), width=10, height=2, bg="red")
        self.delete_button.grid(row=0, column=2, padx=20)

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.label.config(text=self.folder_path)  # 선택된 폴더 이름으로 라벨 텍스트 변경
            self.files = os.listdir(self.folder_path)
            self.files = [f for f in self.files if os.path.isfile(os.path.join(self.folder_path, f))]
            self.current_file_index = 0
            if self.files:
                self.update_file_label()
                self.keep_button.config(state=tk.NORMAL)
                self.music_button.config(state=tk.NORMAL)
                self.delete_button.config(state=tk.NORMAL)
                self.previous_button.config(state=tk.DISABLED if self.current_file_index == 0 else tk.NORMAL)
            else:
                messagebox.showinfo("Info", "The selected folder is empty.")

    def update_file_label(self):
        if self.current_file_index < len(self.files):
            current_file = self.files[self.current_file_index]
            self.file_label.config(text=f"File: {current_file}")
            artist = self.get_artist_info(current_file)
            if artist:
                self.artist_label.config(text=f"Artist: {artist}", font=("Helvetica", int(28 * 0.7)))
            else:
                self.artist_label.config(text="")
        else:
            self.file_label.config(text="No more files.")
            self.artist_label.config(text="")
            self.keep_button.config(state=tk.DISABLED)
            self.music_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)
            self.previous_button.config(state=tk.DISABLED)

    def get_artist_info(self, filename):
        file_path = os.path.join(self.folder_path, filename)
        if filename.lower().endswith('.mp3'):
            try:
                audio = EasyID3(file_path)
                return audio.get('artist', [None])[0]
            except ID3NoHeaderError:
                return None
        return None

    def keep_file(self):
        self.current_file_index += 1
        self.update_file_label()
        self.previous_button.config(state=tk.DISABLED if self.current_file_index == 0 else tk.NORMAL)

    def go_back(self):
        if self.current_file_index > 0:
            self.current_file_index -= 1
            self.update_file_label()
        self.previous_button.config(state=tk.DISABLED if self.current_file_index == 0 else tk.NORMAL)
        self.keep_button.config(state=tk.NORMAL)
        self.music_button.config(state=tk.NORMAL)
        self.delete_button.config(state=tk.NORMAL)

    def toggle_music(self):
        current_file = self.files[self.current_file_index]
        file_path = os.path.join(self.folder_path, current_file)
        if self.music_player.get_busy():
            self.music_player.stop()
            self.music_player.unload()
            self.music_button.config(text="Play Music", bg="green")
        else:
            self.music_player.load(file_path)
            self.music_player.play()
            self.music_button.config(text="Stop Music", bg="orange")

    def delete_file(self):
        current_file = self.files[self.current_file_index]
        file_path = os.path.join(self.folder_path, current_file)
        if self.music_player.get_busy():
            self.music_player.stop()
            self.music_player.unload()
        try:
            os.remove(file_path)
            self.files.pop(self.current_file_index)
            self.update_file_label()
            self.previous_button.config(state=tk.DISABLED if self.current_file_index == 0 else tk.NORMAL)
        except PermissionError as e:
            messagebox.showerror("Error", f"Failed to delete file: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileReviewApp(root)
    root.mainloop()

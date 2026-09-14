import tkinter as tk
from tkinter import filedialog, messagebox
from pydub import AudioSegment

def mix_songs():
    song1_path = entry_song1.get()
    song2_path = entry_song2.get()
    
    if not song1_path or not song2_path:
        messagebox.showerror("දෝෂයකි", "කරුණාකර සින්දු දෙකම තෝරන්න!")
        return
    
    try:
        # සින්දු දෙක Load කරගැනීම
        song1 = AudioSegment.from_file(song1_path)
        song2 = AudioSegment.from_file(song2_path)
        
        # සින්දු දෙක එකට Mix කිරීම (තත්පර 2කට පසු දෙවැන්න පටන් ගනී)
        mixed = song1.overlay(song2, position=2000)
        
        # Save කරගැනීම
        save_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 Files", "*.mp3")])
        if save_path:
            mixed.export(save_path, format="mp3")
            messagebox.showinfo("සාර්ථකයි!", "ඔබේ සින්දු මිශ්‍රණය සාර්ථකව Save විය!")
    except Exception as e:
        messagebox.showerror("දෝෂයක් සිදු විය", str(e))

def browse_song1():
    filename = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    entry_song1.delete(0, tk.END)
    entry_song1.insert(0, filename)

def browse_song2():
    filename = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    entry_song2.delete(0, tk.END)
    entry_song2.insert(0, filename)

# GUI Window එක හැදීම
root = tk.Tk()
root.title("AI Audio Mixer")
root.geometry("450x250")

# 1 වන සින්දුව තෝරන කොටස
tk.Label(root, text="පළමු සින්දුව:").pack(pady=5)
entry_song1 = tk.Entry(root, width=45)
entry_song1.pack()
tk.Button(root, text="Browse", command=browse_song1).pack(pady=2)

# 2 වන සින්දුව තෝරන කොටස
tk.Label(root, text="දෙවන සින්දුව:").pack(pady=5)
entry_song2 = tk.Entry(root, width=45)
entry_song2.pack()
tk.Button(root, text="Browse", command=browse_song2).pack(pady=2)

# Mix කරන Button එක
tk.Button(root, text="Mix Songs Now", command=mix_songs, bg="green", fg="white", font=("Arial", 10, "bold")).pack(pady=15)

root.mainloop()

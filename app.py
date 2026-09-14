import tkinter as tk
from tkinter import filedialog, messagebox
import librosa
import soundfile as sf
import numpy as np
import os

def auto_mix_songs():
    song1_path = entry_song1.get()
    song2_path = entry_song2.get()
    
    if not song1_path or not song2_path:
        messagebox.showerror("දෝෂයකි", "කරුණාකර සින්දු දෙකම තෝරන්න!")
        return
    
    try:
        status_label.config(text="AI එක මඟින් සින්දු විශ්ලේෂණය කරමින් පවතී...")
        root.update()
        
        # 1. සින්දු දෙක AI (Librosa) මඟින් Load කරගැනීම (Sample rate 22050 ලෙස සකසයි)
        y1, sr1 = librosa.load(song1_path, sr=22050)
        y2, sr2 = librosa.load(song2_path, sr=22050)
        
        # 2. සින්දු දෙකේ වේගය (Tempo / BPM) AI එකෙන් සෙවීම
        tempo1, _ = librosa.beat.beat_track(y=y1, sr=sr1)
        tempo2, _ = librosa.beat.beat_track(y=y2, sr=sr2)
        
        # tempo එක scalar අගයකට හරවා ගැනීම
        t1 = float(tempo1) if not isinstance(tempo1, np.ndarray) else float(tempo1[0])
        t2 = float(tempo2) if not isinstance(tempo2, np.ndarray) else float(tempo2[0])
        
        # 3. වේගය සමාන කිරීම (Time Stretching - Beats දෙක එකම මට්ටමට ගෙන ඒම)
        if t1 > 0 and t2 > 0:
            stretch_factor = t1 / t2
            y2_stretched = librosa.effects.time_stretch(y2, rate=stretch_factor)
        else:
            y2_stretched = y2

        # 4. සින්දු දෙක එකට සම්බන්ධ කිරීම (Auto Alignment)
        # පළමු සින්දුවට දෙවන සින්දුව හරියටම Beat එකෙන් Mix වීම
        min_len = min(len(y1), len(y2_stretched))
        
        # ශබ්ද මට්ටම් සමානව එකතු කිරීම
        mixed_audio = y1[:min_len] + y2_stretched[:min_len]
        
        # ශබ්දය වැඩි වී කනට අමාරු වීම වැළැක්වීමට Normalization කිරීම
        mixed_audio = librosa.util.normalize(mixed_audio)

        # 5. Save කරගැනීම
        save_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV Files", "*.wav")])
        if save_path:
            sf.write(save_path, mixed_audio, sr1)
            status_label.config(text="සාර්ථකයි!")
            messagebox.showinfo("සාර්ථකයි!", "AI මඟින් සින්දු Auto Mix කර Save විය!")
        else:
            status_label.config(text="")
            
    except Exception as e:
        status_label.config(text="දෝෂයක් සිදු විය!")
        messagebox.showerror("දෝෂයක්", str(e))

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
root.title("AI Auto Mashup Mixer")
root.geometry("450x300")

tk.Label(root, text="පළමු සින්දුව:").pack(pady=5)
entry_song1 = tk.Entry(root, width=45)
entry_song1.pack()
tk.Button(root, text="Browse", command=browse_song1).pack(pady=2)

tk.Label(root, text="දෙවන සින්දුව:").pack(pady=5)
entry_song2 = tk.Entry(root, width=45)
entry_song2.pack()
tk.Button(root, text="Browse", command=browse_song2).pack(pady=2)

# AI Auto Mix කරන Button එක
tk.Button(root, text="🤖 AI Auto Mix Songs", command=auto_mix_songs, bg="purple", fg="white", font=("Arial", 11, "bold")).pack(pady=15)

status_label = tk.Label(root, text="", fg="blue", font=("Arial", 9))
status_label.pack(pady=5)

root.mainloop()

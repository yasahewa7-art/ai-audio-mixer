import streamlit as st
import librosa
import soundfile as sf
import numpy as np
import tempfile
import os

st.set_page_config(page_title="AI Auto Mashup Mixer", page_icon="🎧", layout="centered")

st.title("🎧 AI Auto Mashup Mixer")
st.write("AI තාක්ෂණය භාවිතයෙන් සින්දු දෙකක වේගය (BPM) සහ බීට් එකතු කර පරිපූර්ණව Mix කරන්න!")

# සින්දු දෙක Upload කරගැනීම සඳහා File Uploader
uploaded_file1 = st.file_uploader("පළමු සින්දුව තෝරන්න (MP3 / WAV)", type=["mp3", "wav"])
uploaded_file2 = st.file_uploader("දෙවන සින්දුව තෝරන්න (MP3 / WAV)", type=["mp3", "wav"])

if st.button("🤖 AI Auto Mix Songs", type="primary"):
    if uploaded_file1 is not None and uploaded_file2 is not None:
        with st.spinner("AI එක මඟින් සින්දු වල බීට් සහ ටෙම්පෝ විශ්ලේෂණය කරමින් පවතී... කරුණාකර රැඳී සිටින්න."):
            try:
                # Save uploaded files to temp files
                tfile1 = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                tfile1.write(uploaded_file1.read())
                tfile1.close()

                tfile2 = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                tfile2.write(uploaded_file2.read())
                tfile2.close()

                # 1. Load audio files (keeping sample rate consistent)
                y1, sr = librosa.load(tfile1.name, sr=22050)
                y2, sr = librosa.load(tfile2.name, sr=22050)

                # 2. Get BPM and Beat Frames for alignment
                tempo1, beats1 = librosa.beat.beat_track(y=y1, sr=sr)
                tempo2, beats2 = librosa.beat.beat_track(y=y2, sr=sr)

                t1 = float(tempo1) if not isinstance(tempo1, np.ndarray) else float(tempo1[0])
                t2 = float(tempo2) if not isinstance(tempo2, np.ndarray) else float(tempo2[0])

                # 3. Time stretching to match tempos precisely
                if t1 > 0 and t2 > 0:
                    stretch_factor = t2 / t1  # Correct stretch ratio alignment
                    # Using higher quality/robust time stretch
                    y2_stretched = librosa.effects.time_stretch(y2, rate=stretch_factor)
                else:
                    y2_stretched = y2

                # 4. Trimming or Padding to match lengths cleanly
                min_len = min(len(y1), len(y2_stretched))
                y1_trimmed = y1[:min_len]
                y2_trimmed = y2_stretched[:min_len]

                # 5. Balanced Volume Mixing (50% from each to prevent background drowning)
                mixed_audio = (0.6 * y1_trimmed) + (0.6 * y2_trimmed)
                mixed_audio = librosa.util.normalize(mixed_audio)

                # Save mixed output to a temp file
                output_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
                sf.write(output_file.name, mixed_audio, sr)

                st.success("සාර්ථකයි! ඔබේ පරිපූර්ණ AI Mashup සින්දුව සූදානම්.")
                
                # Play and Download options
                st.audio(output_file.name, format='audio/wav')
                
                with open(output_file.name, "rb") as file:
                    st.download_button(
                        label="📥 Download Mixed Song",
                        data=file,
                        file_name="ai_pro_mashup.wav",
                        mime="audio/wav"
                    )

                # Clean up temp files
                os.unlink(tfile1.name)
                os.unlink(tfile2.name)

            except Exception as e:
                st.error(f"දෝෂයක් සිදු විය: {e}")
    else:
        st.warning("කරුණාකර සින්දු ෆයිල් දෙකම Upload කරන්න!")

import streamlit as st
import subprocess
import tempfile
import os
import librosa
import soundfile as sf

st.set_page_config(page_title="C++ Powered AI Audio Mixer", page_icon="🎧", layout="centered")

st.title("🎧 C++ Powered AI Audio Mixer")
st.write("MP3 හෝ WAV ඕනෑම සින්දුවක් එකතු කර C++ එන්ජිම හරහා වේගයෙන් මිශ්‍ර කරන්න!")

uploaded_file1 = st.file_uploader("පළමු සින්දුව (MP3 / WAV)", type=["mp3", "wav"])
uploaded_file2 = st.file_uploader("දෙවන සින්දුව (MP3 / WAV)", type=["mp3", "wav"])

if st.button("🚀 Mix with C++ Engine", type="primary"):
    if uploaded_file1 and uploaded_file2:
        with st.spinner("සින්දු ෆයිල්ස් ප්‍රොසෙස් කර C++ එන්ජිමට සූදානම් කරමින් පවතී..."):
            with tempfile.TemporaryDirectory() as tmpdir:
                raw_path1 = os.path.join(tmpdir, "raw1")
                raw_path2 = os.path.join(tmpdir, "raw2")
                
                with open(raw_path1, "wb") as f:
                    f.write(uploaded_file1.getbuffer())
                with open(raw_path2, "wb") as f:
                    f.write(uploaded_file2.getbuffer())

                path1 = os.path.join(tmpdir, "song1.wav")
                path2 = os.path.join(tmpdir, "song2.wav")
                out_path = os.path.join(tmpdir, "output.wav")

                try:
                    # Convert any uploaded MP3/WAV to standard WAV format for C++
                    y1, sr1 = librosa.load(raw_path1, sr=22050)
                    sf.write(path1, y1, sr1)

                    y2, sr2 = librosa.load(raw_path2, sr=22050)
                    sf.write(path2, y2, sr2)
                except Exception as e:
                    st.error(f"ඕඩියෝ ෆයිල් කියවීමේ දෝෂයක්: {e}")
                    st.stop()

                # Compile C++ mixer on the fly
                compile_cmd = "g++ -o mixer mixer.cpp -lsndfile"
                compile_res = os.system(compile_cmd)

                if compile_res == 0:
                    # Run compiled C++ executable
                    run_cmd = f"./mixer {path1} {path2} {out_path}"
                    run_res = os.system(run_cmd)

                    if run_res == 0 and os.path.exists(out_path):
                        st.success("සාර්ථකයි! C++ මඟින් සින්දු මිශ්‍ර කර අවසන්.")
                        st.audio(out_path)
                        
                        with open(out_path, "rb") as f:
                            st.download_button("📥 Download C++ Mashup", f, file_name="cpp_mashup.wav", mime="audio/wav")
                    else:
                        st.error("C++ වැඩසටහන ක්‍රියාත්මකවීමේදී දෝෂයක් ඇති විය.")
                else:
                    st.error("C++ කෝඩ් එක Compile කරගැනීමේ දෝෂයක් (g++ / libsndfile missing).")
    else:
        st.warning("කරුණාකර සින්දු ෆයිල් දෙකම Upload කරන්න!")

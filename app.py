import streamlit as st
import subprocess
import tempfile
import os

st.set_page_config(page_title="C++ AI Audio Mixer", page_icon="🎧", layout="centered")

st.title("🎧 C++ Powered AI Audio Mixer")
st.write("C++ මඟින් ධාවනය වන වේගවත් සහ නිවැරදි ඕඩියෝ මිශ්‍රණ යන්ත්‍රය.")

uploaded_file1 = st.file_uploader("පළමු සින්දුව (WAV)", type=["wav"])
uploaded_file2 = st.file_uploader("දෙවන සින්දුව (WAV)", type=["wav"])

if st.button("🚀 Mix with C++ Engine", type="primary"):
    if uploaded_file1 and uploaded_file2:
        with st.spinner("C++ එන්ජිම හරහා ඕඩියෝ ප්‍රොසෙස් වෙමින් පවතී..."):
            with tempfile.TemporaryDirectory() as tmpdir:
                path1 = os.path.join(tmpdir, "song1.wav")
                path2 = os.path.join(tmpdir, "song2.wav")
                out_path = os.path.join(tmpdir, "output.wav")

                with open(path1, "wb") as f:
                    f.write(uploaded_file1.getbuffer())
                with open(path2, "wb") as f:
                    f.write(uploaded_file2.getbuffer())

                # Compile C++ mixer on the fly inside Streamlit environment
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
        st.warning("කරුණාකර WAV සින්දු ෆයිල් දෙකම Upload කරන්න!")

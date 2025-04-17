import streamlit as st
import os
from gpt_label import generate_blender_script
import subprocess

st.title("💡 3D Label Applicator")

model_file = st.file_uploader("Upload 3D Model (.obj or .glb)", type=["obj", "glb"])
label_file = st.file_uploader("Upload Label Image (.png)", type=["png", "jpg"])

col1, col2 = st.columns(2)
with col1:
    label_width = st.number_input("Label Width (mm)", value=41)
with col2:
    label_height = st.number_input("Label Height (mm)", value=82)

model_height_mm = st.number_input("Real Height of the Model (mm)", value=120)

if st.button("Apply Label") and model_file and label_file:
    # ✅ Create folders safely (for Streamlit Cloud compatibility)
    os.makedirs("models", exist_ok=True)
    os.makedirs("labels", exist_ok=True)
    os.makedirs("scripts", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    # ✅ Save uploaded files
    model_path = os.path.join("models", model_file.name)
    label_path = os.path.join("labels", label_file.name)

    with open(model_path, "wb") as f:
        f.write(model_file.read())

    with open(label_path, "wb") as f:
        f.write(label_file.read())

    st.write("🧠 Sending request to GPT-4...")
    script_path = "scripts/apply_label.py"
    generate_blender_script(model_path, label_path, label_width, label_height, model_height_mm, script_path)

    # 🛑 WARNING: Blender won't run in Streamlit Cloud. This works only locally.
    st.warning("Blender can't run in Streamlit Cloud. You'll need to run this script locally.")

    # ✅ Optionally show GPT-generated script
    with open(script_path, "r") as f:
        st.code(f.read(), language="python")

    # ✅ (Optional) Let user download the script
    with open(script_path, "rb") as f:
        st.download_button("Download Blender Script", f, file_name="apply_label.py")

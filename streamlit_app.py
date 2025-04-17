import streamlit as st
import os
import uuid
from gpt_label import generate_blender_script

st.set_page_config(page_title="3D Label Applicator", layout="centered")
st.title("💡 3D Label Applicator")

# Upload
model_file = st.file_uploader("Upload 3D Model (.obj or .glb)", type=["obj", "glb"])
label_file = st.file_uploader("Upload Label Image (.png or .jpg)", type=["png", "jpg"])

# Inputs
col1, col2 = st.columns(2)
with col1:
    label_width = st.number_input("Label Width (mm)", value=41, min_value=1)
with col2:
    label_height = st.number_input("Label Height (mm)", value=82, min_value=1)
model_height_mm = st.number_input("Real Height of 3D Model (mm)", value=120, min_value=1)

# 🔘 Button Click Handler
if st.button("🧠 Generate Blender Script"):

    # ✅ Ensure files are uploaded
    if not model_file or not label_file:
        st.error("❌ Please upload both a model and a label.")
        st.stop()

    try:
        # ✅ Prepare folders
        os.makedirs("models", exist_ok=True)
        os.makedirs("labels", exist_ok=True)
        os.makedirs("scripts", exist_ok=True)
        os.makedirs("output", exist_ok=True)

        # ✅ Unique filenames
        uid = str(uuid.uuid4())[:8]
        model_filename = f"{uid}_{model_file.name}"
        label_filename = f"{uid}_{label_file.name}"
        model_path = os.path.join("models", model_filename)
        label_path = os.path.join("labels", label_filename)
        script_path = os.path.join("scripts", f"{uid}_apply_label.py")

        # ✅ Save uploaded files
        with open(model_path, "wb") as f:
            f.write(model_file.getbuffer())
        with open(label_path, "wb") as f:
            f.write(label_file.getbuffer())

        # ✅ GPT generates the Blender script
        st.info("🧠 Asking GPT to generate Blender script...")
        generate_blender_script(
            model_path=model_path,
            label_path=label_path,
            label_width_mm=label_width,
            label_height_mm=label_height,
            model_height_mm=model_height_mm,
            output_script_path=script_path
        )

        # ✅ Display + download Blender script
        st.success("✅ Script generated! Run this in Blender locally.")
        with open(script_path, "r") as f:
            st.code(f.read(), language="python")
        with open(script_path, "rb") as f:
            st.download_button("📥 Download Blender Script", f, file_name="apply_label.py")

    except Exception as e:
        st.error(f"❌ Error: {e}")
        st.stop()

import streamlit as st
import os
from gpt_label import generate_blender_script

st.title("💡 3D Label Applicator")

model_file = st.file_uploader("Upload 3D Model (.obj or .glb)", type=["obj", "glb"])
label_file = st.file_uploader("Upload Label Image (.png or .jpg)", type=["png", "jpg"])

col1, col2 = st.columns(2)
with col1:
    label_width = st.number_input("Label Width (mm)", value=41)
with col2:
    label_height = st.number_input("Label Height (mm)", value=82)

model_height_mm = st.number_input("Real Height of the Model (mm)", value=120)

# 🟢 MAIN ACTION
if st.button("Apply Label"):

    # ✅ Check for both uploads
    if not model_file or not label_file:
        st.error("Please upload both a 3D model and a label image.")
    else:
        try:
            # ✅ Create necessary folders
            os.makedirs("models", exist_ok=True)
            os.makedirs("labels", exist_ok=True)
            os.makedirs("scripts", exist_ok=True)
            os.makedirs("output", exist_ok=True)

            # ✅ Save files
            model_path = os.path.join("models", model_file.name)
            label_path = os.path.join("labels", label_file.name)

            with open(model_path, "wb") as f:
                f.write(model_file.read())

            with open(label_path, "wb") as f:
                f.write(label_file.read())

            # ✅ Generate Blender script
            st.write("🧠 Sending request to GPT-4...")
            script_path = "scripts/apply_label.py"
            generate_blender_script(
                model_path=model_path,
                label_path=label_path,
                label_width_mm=label_width,
                label_height_mm=label_height,
                model_height_mm=model_height_mm,
                output_script_path=script_path
            )

            # ✅ Show and download Blender script
            st.warning("⚠️ Blender cannot run on Streamlit Cloud. Please run the script locally.")
            with open(script_path, "r") as f:
                st.code(f.read(), language="python")
            with open(script_path, "rb") as f:
                st.download_button("Download Blender Script", f, file_name="apply_label.py")

        except Exception as e:
            st.error(f"❌ Error: {e}")

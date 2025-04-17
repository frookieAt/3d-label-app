import streamlit as st
import os
import uuid
from gpt_label import generate_blender_script

st.set_page_config(page_title="3D Label Applicator", layout="centered")
st.title("💡 3D Label Applicator")

st.markdown("Upload a 3D packaging model and label image. The app will generate a Blender script that applies the label scaled to mm-accurate size. Run the script locally in Blender to preview or export your labeled model.")

# File upload section
model_file = st.file_uploader("Upload 3D Model (.obj or .glb)", type=["obj", "glb"])
label_file = st.file_uploader("Upload Label Image (.png or .jpg)", type=["png", "jpg"])

col1, col2 = st.columns(2)
with col1:
    label_width = st.number_input("Label Width (mm)", value=41, min_value=1)
with col2:
    label_height = st.number_input("Label Height (mm)", value=82, min_value=1)

model_height_mm = st.number_input("Real Height of the 3D Model (mm)", value=120, min_value=1)

# Handle button click
if st.button("🧠 Generate Blender Script"):

    # Validate file uploads
    if not model_file or not label_file:
        st.error("❌ Please upload both a 3D model and a label image.")
        st.stop()

    try:
        # Create necessary folders
        os.makedirs("models", exist_ok=True)
        os.makedirs("labels", exist_ok=True)
        os.makedirs("scripts", exist_ok=True)
        os.makedirs("output", exist_ok=True)

        # Generate unique filenames using UUID
        unique_id = str(uuid.uuid4())[:8]
        model_filename = f"{unique_id}_{model_file.name}"
        label_filename = f"{unique_id}_{label_file.name}"

        model_path = os.path.join("models", model_filename)
        label_path = os.path.join("labels", label_filename)
        script_path = os.path.join("scripts", f"{unique_id}_apply_label.py")

        # Save files
        with open(model_path, "wb") as f:
            f.write(model_file.getbuffer())

        with open(label_path, "wb") as f:
            f.write(label_file.getbuffer())

        # Confirm file saving
        if not os.path.exists(model_path) or not os.path.exists(label_path):
            st.error("❌ Error saving uploaded files.")
            st.stop()

        # Send to GPT to generate Blender script
        st.info("⏳ Generating Blender script with GPT-4...")
        generate_blender_script(
            model_path=model_path,
            label_path=label_path,
            label_width_mm=label_width,
            label_height_mm=label_height,
            model_height_mm=model_height_mm,
            output_script_path=script_path
        )

        # Confirm script generation
        if not os.path.exists(script_path):
            st.error("❌ Failed to generate Blender script.")
            st.stop()

        st.success("✅ Blender script generated successfully!")
        st.markdown("⚠️ **Blender cannot run on Streamlit Cloud.** Please run the script locally in Blender to apply and preview the label.")

        # Display the script
        with open(script_path, "r") as f:
            script_code = f.read()
            st.code(script_code, language="python")

        # Download button
        with open(script_path, "rb") as f:
            st.download_button("📥 Download Blender Script", f, file_name="apply_label.py")

    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
        st.stop()

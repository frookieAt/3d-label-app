import streamlit as st
import os
import subprocess
from generate_scaler_script import generate_blender_scaling_script

st.set_page_config("📐 Blender Model Scaler", layout="centered")
st.title("📐 Scale Blender Model by Real-World Dimensions")

height_mm = st.number_input("Target Height (mm)", min_value=1, value=120)
width_mm = st.number_input("Target Width (mm, optional)", min_value=0, value=0)
depth_mm = st.number_input("Target Depth (mm, optional)", min_value=0, value=0)

if st.button("🚀 Scale Active Blender Model"):
    try:
        os.makedirs("scripts", exist_ok=True)
        os.makedirs("output", exist_ok=True)

        width = width_mm if width_mm > 0 else None
        depth = depth_mm if depth_mm > 0 else None

        script_path = "scripts/scale_model.py"
        generate_blender_scaling_script(height_mm, width, depth, script_path)

        st.info("📤 Running Blender...")
        result = subprocess.run(["blender", "--background", "--python", script_path], capture_output=True, text=True)
        
        st.success("✅ Scaling Complete!")
        st.code(result.stdout, language="bash")

        st.download_button("📥 Download Scaled .blend", open("output/scaled_model.blend", "rb"), file_name="scaled_model.blend")

    except Exception as e:
        st.error(f"❌ Failed: {e}")

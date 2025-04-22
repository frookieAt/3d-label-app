import streamlit as st
import os
import subprocess
from generate_scaler_script import generate_blender_scaling_script

st.set_page_config("📐 Blender Model Scaler", layout="centered")
st.title("📐 Scale Blender Model")

height_mm = st.number_input("Target Height (mm)", min_value=1, value=120)
width_mm = st.number_input("Target Width (optional, mm)", min_value=0, value=0)
depth_mm = st.number_input("Target Depth (optional, mm)", min_value=0, value=0)

if st.button("🚀 Scale Active Blender Model"):
    try:
        os.makedirs("scripts", exist_ok=True)
        os.makedirs("output", exist_ok=True)

        width = width_mm if width_mm > 0 else None
        depth = depth_mm if depth_mm > 0 else None

        script_path = "scripts/scale_model.py"
        generate_blender_scaling_script(height_mm, width, depth, script_path)

        st.info("🔧 Running Blender in background...")
        result = subprocess.run(["blender", "--background", "--python", script_path], capture_output=True, text=True)

        st.success("✅ Scaling Complete!")
        st.code(result.stdout, language="bash")

        blend_path = "output/scaled_model.blend"
        if os.path.exists(blend_path):
            with open(blend_path, "rb") as f:
                st.download_button("📥 Download Scaled .blend", f, file_name="scaled_model.blend")
        else:
            st.warning("Blender completed but output file not found.")

    except Exception as e:
        st.error(f"❌ Error: {e}")

import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_blender_script(model_path, label_path, label_width_mm, label_height_mm, model_height_mm, output_script_path):
    prompt = f"""
Write a Blender Python script that:
1. Imports the 3D model from '{model_path}'
2. Scales the model so its Z height is exactly {model_height_mm} mm (0.0{model_height_mm} meters)
3. Imports the label image from '{label_path}'
4. UV unwraps the front face and applies the label image as a texture
5. The label must be sized to exactly {label_width_mm} mm wide by {label_height_mm} mm high
6. Render the result to 'output/render.png'
7. Export the model as a GLB to 'output/labeled_model.glb'

Ensure the script works in headless (background) Blender mode and uses mm-to-meter conversion.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )

    blender_code = response["choices"][0]["message"]["content"]
    with open(output_script_path, "w") as f:
        f.write(blender_code)

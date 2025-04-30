from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# ✅ Correct configuration with the right model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('models/gemini-pro-vision')  # ✅ Use full model name
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit UI setup
st.set_page_config(page_title="Gemini Health App")
st.header("Gemini Health App")

user_input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Tell me the total calories")

input_prompt = """
You are an expert nutritionist. Analyze the food items in this image and estimate total calories. 
Provide details in this format:

1. Item 1 - X calories
2. Item 2 - Y calories
...
"""

if submit:
    try:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, user_input)
        st.subheader("The Response is")
        st.write(response)
    except Exception as e:
        st.error(f"An error occurred: {e}")

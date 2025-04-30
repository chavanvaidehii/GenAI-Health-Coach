from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Configure the Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini response
def get_gemini_response(prompt, image_data, user_input):
    model = genai.GenerativeModel('models/gemini-pro-vision')
    response = model.generate_content([
        {"text": prompt},
        image_data[0],  # Ensure image_data is a list of dict with 'mime_type' and 'data'
        {"text": user_input}
    ])
    return response.text

# Function to handle image upload
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize the Streamlit app
st.set_page_config(page_title="Gemini Health App")
st.header("Gemini Health App")

# User input prompt
user_input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Show uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Prompt template for Gemini
input_prompt = """
You are an expert in nutritionist where you need to see the food items from the image
and calculate the total calories, also provide the details of every food item with calories intake
in the below format:
1. Item 1 - number of calories
2. Item 2 - number of calories
----
----
"""

# Button to submit and generate response
if st.button("Tell me the total calories"):
    if uploaded_file is not None:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, user_input)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.error("Please upload an image before submitting.")

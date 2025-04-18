import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
import base64
import requests
import io
from io import BytesIO
from dotenv import load_dotenv
import textwrap
import requests
import json
import random
from openai import OpenAI
from tinydb import TinyDB, Query

#openAI
client = OpenAI(
    base_url="",
    api_key=""
)

#tinyDB setup
db = TinyDB('memes.json')
with open('urls.json', 'r') as file:
    urls = json.load(file)
for url in urls:
    db.insert({'url': url})

#Retrive random meme template from TinyDB
def get_random_template_url():
    templates = db.all()
    if templates:
        return random.choice(templates)['url']
    else:
        return None

#generate_captions
def generate_captions(prompt, style, image_url):
    try:
        response = client.chat.completions.create(
            model="tgi",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are a witty meme generator. The funnier, the wittier, the better. "
                        f"Generate one caption for a meme based on the image provided"
                        f"The caption should be in Simplified/Traditional Chinese or English depending on the user's input language using {style.lower()} style."
                        f"incorporate the prompt's content into the caption"
                        f"Only respond with the actual meme caption, do not include anything else "
                        f"Never use emojis "
                    )
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url}
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
            max_tokens=300,
        )
        captions = response.choices[0].message.content.strip()
        return captions
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def generate_captions_upload(prompt, style):
    try:
        response = client.chat.completions.create(
            model="tgi",
            max_tokens=300,
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are a witty meme generator. The funnier, the wittier, the better. "
                        f"Generate one caption for a meme"
                        f"The caption should be in Simplified/Traditional Chinese or English depending "
                        f"on the user's input language using {style.lower()} style. "
                        f"Only respond with the actual meme caption, do not include anything else. "
                        f"Never use emojis."
                        f"incorporate the prompt's content into the caption"
                    )
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        st.error(f"Error generating caption: {e}")
        return None

def overlay_text_on_image(image, text):
    draw = ImageDraw.Draw(image)
    # Set a base font size based on the image width
    base_font_size = max(50, image.width // 20)
    # Reduce font size if the text is very long
    font_size = int(base_font_size * 0.8) if len(text) > 50 else base_font_size

    # Load the font (fallback to default if not found)
    try:
        font = ImageFont.truetype("msyh.ttc", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Define margin and maximum width for text
    margin = 20
    max_width = image.width - margin

    # Dynamically break text into lines that fit within max_width
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]
        if line_width > max_width and current_line:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test_line
    if current_line:
        lines.append(current_line)

    # Calculate total text block height
    total_text_height = 0
    line_heights = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_height = bbox[3] - bbox[1]
        line_heights.append(line_height)
        total_text_height += line_height

    # Position text near the bottom with a margin
    y = image.height - total_text_height - 20

    # Draw each line centered and with an outline for readability
    outline_range = 2
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x = (image.width - line_width) / 2

        # Draw text outline
        for shift_x in range(-outline_range, outline_range + 1):
            for shift_y in range(-outline_range, outline_range + 1):
                draw.text((x + shift_x, y + shift_y), line, font=font, fill="black")
        # Draw the actual text
        draw.text((x, y), line, font=font, fill="white")
        y += line_heights[i]

    return image

def main():
    logo = Image.open("meme.jpg")
    st.set_page_config(
        page_title="Meme Generator",
        page_icon=logo,
        layout="centered"
    )
    st.title("Meme Generator")
    st.write("Generate creative meme captions using AI and overlay them at the bottom of your image.")

    option = st.radio("Choose an option:", ("Upload an image", "Use meme template"))

    if option == "Upload an image":
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            image = Image.open(uploaded_file)
        else:
            image = None
    else:
        #use default meme template
        if "template_url" not in st.session_state:
            st.session_state.template_url = get_random_template_url()

        if st.button("Refresh Meme Template"):
            st.session_state.template_url = get_random_template_url()
        template_url = st.session_state.template_url
        response = requests.get(template_url)
        image = Image.open(BytesIO(response.content))
        st.image(image, caption="Your meme template", use_container_width=True)

    prompt = st.text_input("Enter a prompt for the meme caption: ")
    style = st.selectbox("Choose a caption style: ", ("Witty", "Sarcastic", "Wholesome", "Dark Humor"))

    if st.button("Generate meme"):
        if image is None:
            st.error("Please upload an image or select a meme template.")
        elif not prompt:
            st.error("Please enter a prompt for the caption generation.")
        else:
            with st.spinner("Generating captions..."):
                if option == "Upload an image":
                    caption = generate_captions_upload(prompt, style)
                else:
                    caption = generate_captions(prompt, style, template_url)
            if caption:
                st.subheader("Generated caption: ")
                st.write(caption)

                #overlay caption
                meme_image = overlay_text_on_image(image.copy(), caption)
                st.image(meme_image, caption="Your meme", use_container_width=True)

                #allow user to download the meme
                buffered = io.BytesIO()
                meme_image.save(buffered, format="JPEG")
                st.download_button("Download Meme", data=buffered.getvalue(), mime="image/jpeg", file_name="meme.png")

if __name__ == "__main__":
    main()
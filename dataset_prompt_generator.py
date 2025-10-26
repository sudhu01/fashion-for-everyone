'''import ollama

def generate_fashion_prompts():
    """
    Generates fashion item prompts for AI model.
    Each prompt should be unique and follow strict formatting rules.
    """
    ollama_prompt = Generate 200 unique prompts for AI fashion item generation with STRICT formatting:
    - Item description only (no styling/usage context)
    - Explicit "plain white background" mention
    - No people/accessories/body parts
    - Focus on fabric, cut, patterns, textures
    - Add gender/age group if applicable
    Example: "A tailored navy blazer with peak lapels on plain white background, men's wear"

    Items: cardigan, t-shirt, dress, jeans, jacket, skirt, blouse, shorts, sweater, coat, hoodie, pants, tank top, polo shirt, blazer, jumpsuit, leggings, scarf, vest, romper


    result = ollama.generate(model='llama3.2:latest', prompt=ollama_prompt)

    response = result['response']

    ollama_generated_prompts = []

    for i,line in enumerate(response.split('\n')):
        if i >= 2 and i < 202:
            print(f"Prompt {i-1}: {line.split('.')[1]}")
            #ollama_generated_prompts.append(line.split('.')[1])

    #return ollama_generated_prompts


generate_fashion_prompts()'''

import os
import re
import json
import base64
import google.generativeai as genai
from PIL import Image
from tqdm import tqdm
import multiprocessing

# === CONFIG ===
RENDERED_DIR = "C:/Users/jacks/OneDrive/Documents/dataset_blended"
OUTPUT_JSON = "captions_metadata.json"
OUTPUT_CSV = "captions_metadata.csv"
GEMINI_API_KEY = "AIzaSyApCp5b-lmuSPTFhBsBxIdswotLU8QBp24"
MODEL_NAME = "models/gemini-1.5-flash"

# === Gemini API Setup ===
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name=MODEL_NAME)

# === Call Gemini to caption an image ===
def caption_with_gemini(image_path, view):
    try:
        image = Image.open(image_path).convert("RGB")
        prompt = f'''Provide a rich visual description of the clothing in the image STRICTLY in this format with the EXACT wording. Replace the words in brackets with what is observed in the clothing:
“A [fit] [color] [garment] with [key features], from the [view] view.”'''

        response = model.generate_content([
            prompt,
            image
        ])
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# === Process a single folder ===
def process_folder(folder):
    result = []
    if not re.match(r"^\d+-\d+$", folder):
        return result

    for view in ['front', 'side', 'back']:
        image_path = os.path.join(folder, f"{view}.png")
        full_image_path = os.path.join(RENDERED_DIR, image_path)
        if os.path.exists(full_image_path):
            prompt = caption_with_gemini(full_image_path, view)
            result.append({
                "image": image_path.replace("\\", "/"),
                "prompt": prompt
            })
    return result

# === Parallel caption generation with tqdm ===
if __name__ == '__main__':
    folders = os.listdir(RENDERED_DIR)
    with multiprocessing.Pool(processes=os.cpu_count()) as pool:
        all_results = list(tqdm(pool.imap_unordered(process_folder, folders), total=len(folders), desc="Generating captions"))

    entries = [item for sublist in all_results for item in sublist]

    # === Save JSON ===
    with open(OUTPUT_JSON, 'w') as jf:
        json.dump(entries, jf, indent=4)

    # === Save CSV ===
    with open(OUTPUT_CSV, 'w') as cf:
        cf.write("image,prompt\n")
        for entry in entries:
            cf.write(f"{entry['image']},{entry['prompt']}\n")

    print(f"✅ Saved {len(entries)} caption entries to:\n- {OUTPUT_JSON}\n- {OUTPUT_CSV}")

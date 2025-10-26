from dataset_prompt_generator import generate_fashion_prompts
from google import genai
import os, shutil
from PIL import Image
from io import BytesIO
import base64

def add_extra_details(s):
    return s + ". No people/accessories/body parts, focus on fabric, cut, patterns, textures. Provide a high-quality result with realistic lighting"

def add_front_view(s):
    return s + ". Front view only"

def add_back_view(s):
    return s + ". Back view only"

def add_side_view(s):
    return s + ". Side view only"

ollama_generated_prompts = generate_fashion_prompts()
prompts_for_gemini = list(map(add_extra_details, ollama_generated_prompts))
prompts_for_gemini_front = list(map(add_front_view, prompts_for_gemini))
prompts_for_gemini_back = list(map(add_back_view, prompts_for_gemini))
prompts_for_gemini_side = list(map(add_side_view, prompts_for_gemini))

client =  genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

img_count = 1

source = os.getcwd()
destination = "C:/Users/jacks/OneDrive/Documents/dataset"

for i, prompt in enumerate(prompts_for_gemini_front):
    response = client.models.generate_content(
    model="gemini-2.0-flash-preview-image-generation",
    contents=prompt,
    config=genai.types.GenerateContentConfig(
      response_modalities=['TEXT', 'IMAGE']
    )
    )

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))
            image.save(f'{img_count}_front.png')
            image.show()
            img_count += 1
            prompt_file = open(f'{img_count}_front.txt', 'w')
            prompt_file.write(prompt)
            prompt_file.close()
            shutil.move(f'{source}/{img_count}_front.png', f'{destination}/{img_count}_front.png')
            shutil.move(f'{source}/{img_count}_front.txt', f'{destination}/{img_count}_front.txt')

    print(f"Processed prompt {i+1}/{len(prompts_for_gemini_front)}")

img_count = 1

for i, prompt in enumerate(prompts_for_gemini_side):
    response = client.models.generate_content(
    model="gemini-2.0-flash-preview-image-generation",
    contents=prompt,
    config=genai.types.GenerateContentConfig(
      response_modalities=['TEXT', 'IMAGE']
    )
    )

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))
            image.save(f'{img_count}_side.png')
            image.show()
            img_count += 1
            prompt_file = open(f'{img_count}_side.txt', 'w')
            prompt_file.write(prompt)
            prompt_file.close()
            shutil.move(f'{source}/{img_count}_side.png', f'{destination}/{img_count}_side.png')
            shutil.move(f'{source}/{img_count}_side.txt', f'{destination}/{img_count}_side.txt')

    print(f"Processed prompt {i+1}/{len(prompts_for_gemini_side)}")

img_count = 1

for i, prompt in enumerate(prompts_for_gemini_back):
    response = client.models.generate_content(
    model="gemini-2.0-flash-preview-image-generation",
    contents=prompt,
    config=genai.types.GenerateContentConfig(
      response_modalities=['TEXT', 'IMAGE']
    )
    )

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))
            image.save(f'{img_count}_back.png')
            image.show()
            img_count += 1
            prompt_file = open(f'{img_count}_back.txt', 'w')
            prompt_file.write(prompt)
            prompt_file.close()
            shutil.move(f'{source}/{img_count}_back.png', f'{destination}/{img_count}_back.png')
            shutil.move(f'{source}/{img_count}_back.txt', f'{destination}/{img_count}_back.txt')

    print(f"Processed prompt {i+1}/{len(prompts_for_gemini_back)}")
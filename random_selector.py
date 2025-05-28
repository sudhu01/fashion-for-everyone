import random, csv, os, shutil, pandas as pd
from data_packager import package_training_data

def random_selector(dirs, weights, num_samples=50):
    selected_images = random.choices(dirs, weights=weights, k=num_samples)
    return selected_images

def create_prompt(row):
    base_prompt = f"A {row['color']} {row['category']} in {row['style']} style"
    if pd.notna(row['description']):
        base_prompt += f", {row['description']}"
    return base_prompt


print(os.getcwd())
os.chdir('../../../Downloads/fashion-product-images-extracted/fashion-dataset/resized_images')
dirs = os.listdir()
weights = [1] * len(dirs)  # Equal weight for each image


selected_images = random_selector(dirs, weights, num_samples=50)

os.chdir('../')
os.mkdir('selected_images')
parent_dir = os.getcwd()

for img in selected_images:
    shutil.copy(os.path.join(parent_dir, 'resized_images',img), os.path.join(os.getcwd(), 'selected_images',img))


selected_images = [img.split('.')[0] for img in selected_images]  # Remove file extensions
print("Selected images:", selected_images)

rows_to_be_written = []

with open('styles.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header
    for row in reader:
        if row[0] in selected_images:
            rows_to_be_written.append([row[0], row[2], row[5], row[4]+' '+row[6]+' '+row[8], row[-1]])


with open('selected_styles.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id','category','color','style','description'])
    writer.writerows(rows_to_be_written)
print("Selected styles saved to 'selected_styles.csv'.")


df = pd.read_csv('selected_styles.csv')

# Create prompts for each image
df['prompt'] = df.apply(create_prompt, axis=1)

# Create dataset dictionary
dataset_dict = {
    'image': [],
    'text': []
}

for _, row in df.iterrows():
    image_path = os.path.join(os.getcwd(), 'selected_images',str(row['id']) + '.jpg')
    if os.path.exists(image_path):
        dataset_dict['image'].append(image_path)
        dataset_dict['text'].append(row['prompt'])


package_file = package_training_data(dataset_dict, 'selected_images')
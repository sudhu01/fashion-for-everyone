from PIL import Image
import os

def smart_crop_resize(image_path, output_path, size=(512, 512)):
    with Image.open(image_path) as img:
        width, height = img.size

        # For fashion images, focus on the center-upper portion
        # This usually contains the main garment
        if height > width:
            # Portrait - crop from top 60% to get main clothing area
            crop_height = width
            top = height * 0.1  # Start 10% from top
            bottom = top + crop_height
            img_cropped = img.crop((0, top, width, bottom))
        else:
            # Landscape - center crop
            crop_width = height
            left = (width - crop_width) // 2
            img_cropped = img.crop((left, 0, left + crop_width, height))

        # Resize to target
        img_resized = img_cropped.resize(size, Image.BICUBIC)
        img_resized.save(output_path)


print(os.getcwd())
os.chdir('../../../Downloads/fashion-product-images-extracted/fashion-dataset/images')
dirs = os.listdir()

parent_dir = "C:/Users/jacks/Downloads/fashion-product-images-extracted/fashion-dataset"
path = os.path.join(parent_dir, "resized_images")
os.mkdir(path)

for img in dirs:
    smart_crop_resize(img, os.path.join(path, img), size=(512, 512))

print("Resizing complete. Images saved to:", path)
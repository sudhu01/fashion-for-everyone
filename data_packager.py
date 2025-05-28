import json, zipfile, os

def package_training_data(dataset_dict, selected_images_folder, output_file="fashion_training_data_preprocessed.zip"):

    # Save dataset dictionary as JSON
    with open('dataset_metadata.json', 'w') as json_file:
        json.dump(dataset_dict, json_file, indent=2)
    
    # Create zip file with images and metadata
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:

        # Add all selected images
        for image_path in dataset_dict['image']:
            if os.path.exists(image_path):
                # Get just the filename for archive
                filename = os.path.basename(image_path)
                zipf.write(image_path, f"images/{filename}")
        
        # Add metadata
        zipf.write('dataset_metadata.json', 'dataset_metadata.json')
        zipf.write('selected_styles.csv', 'selected_styles.csv')
    
    print(f"Training data packaged in: {output_file}")
    print(f"File size: {os.path.getsize(output_file) / (1024*1024):.2f} MB")
    return output_file


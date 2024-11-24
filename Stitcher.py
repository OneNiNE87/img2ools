from PIL import Image
import os
import sys
from datetime import datetime

def stitch_images_in_directory(input_dir):
    # Get a list of all files in the input directory
    files = os.listdir(input_dir)
    
    # Filter the list to include only image files (you can customize this filter if needed)
    image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    
    # Sort the list of image files alphabetically
    image_files.sort()
    
    if not image_files:
        print("No image files found in the input directory.")
        return None
    
    images = []
    max_height = 0
    
    # Open and collect image objects, and determine the maximum height
    for image_file in image_files:
        image_path = os.path.join(input_dir, image_file)
        img = Image.open(image_path).convert('RGB')
        images.append(img)
        if img.height > max_height:
            max_height = img.height
    
    # Calculate the new width for each image based on the maximum height
    scaled_images = []
    for img in images:
        ratio = max_height / img.height
        new_width = int(img.width * ratio)
        scaled_img = img.resize((new_width, max_height), Image.LANCZOS)  # Use LANCZOS for high-quality resizing
        scaled_images.append(scaled_img)
    
    # Create the result image
    total_width = sum(img.width for img in scaled_images)
    result_image = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    
    # Paste the scaled images onto the result image
    for img in scaled_images:
        result_image.paste(img, (x_offset, 0))
        x_offset += img.width
    
    return result_image

def generate_output_filename(image_files):
    # Extract the first three letters from each image file name
    name_parts = [file[:3] for file in image_files]
    
    # Join the name parts with '_' separator
    file_name = '_'.join(name_parts)
    
    # Append current date and time stamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_filename = f"{file_name}_{timestamp}.jpg"
    
    return output_filename

if __name__ == "__main__":
    # Check if an input directory is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python Stitcher.py <input_directory>")
        sys.exit(1)
    
    # Get the input directory path from the command-line argument
    input_dir = sys.argv[1]
    
    # Validate the input directory
    if not os.path.isdir(input_dir):
        print("Error: Input directory does not exist.")
        sys.exit(1)
    
    # Stitch images in the specified input directory
    result = stitch_images_in_directory(input_dir)
    
    if result:
        result.show()  # Display the stitched image
        
        # Generate the output file name based on input file names and current timestamp
        image_files = os.listdir(input_dir)
        output_filename = generate_output_filename(image_files)
        
        # Save the stitched image to a file with the generated output filename
        output_path = os.path.join(input_dir, output_filename)
        result.save(output_path)  # Save the stitched image to a file
        print(f"Stitched image saved to: {output_path}")

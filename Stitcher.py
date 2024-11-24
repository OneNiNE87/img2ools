from PIL import Image
import os
import sys
from datetime import datetime

def resize_image_for_processing(img, target_max_size=1000):
    """
    Resize the image to a manageable size before processing, if it's too large.
    The target size can be adjusted based on available memory.
    """
    if img.width > target_max_size or img.height > target_max_size:
        ratio = target_max_size / float(max(img.width, img.height))
        new_width = int(img.width * ratio)
        new_height = int(img.height * ratio)
        img = img.resize((new_width, new_height), Image.LANCZOS)
    return img

def stitch_images_in_grid(input_dir, rows, cols):
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
    for image_file in image_files:
        image_path = os.path.join(input_dir, image_file)
        img = Image.open(image_path).convert('RGB')

        # Resize image for processing to a manageable size
        img = resize_image_for_processing(img)
        
        images.append(img)
    
    # Check if we have enough images for the grid
    if len(images) < rows * cols:
        print(f"Warning: Only {len(images)} images found, which is less than the requested {rows * cols} images for the grid.")
    
    # Find the largest width and height
    max_width = max(img.width for img in images)
    max_height = max(img.height for img in images)
    
    # Resize all images to match the max width/height for uniformity in the grid
    resized_images = []
    for img in images:
        ratio_width = max_width / img.width
        ratio_height = max_height / img.height
        ratio = max(ratio_width, ratio_height)  # Keep the largest dimension ratio
        new_width = int(img.width * ratio)
        new_height = int(img.height * ratio)
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        resized_images.append(resized_img)
    
    # Create the result image size based on the grid dimensions
    grid_width = max_width * cols
    grid_height = max_height * rows
    
    result_image = Image.new('RGB', (grid_width, grid_height))

    # Paste the images into the result image in the specified grid layout
    x_offset = 0
    y_offset = 0
    for i in range(len(resized_images)):
        img = resized_images[i]
        result_image.paste(img, (x_offset, y_offset))

        # Move to the next column
        x_offset += max_width
        if (i + 1) % cols == 0:  # Move to the next row after the last column
            x_offset = 0
            y_offset += max_height

        if (i + 1) >= rows * cols:  # Only use the first `rows * cols` images
            break
    
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
    # Get the input directory path from the user
    input_dir = input("Enter the directory path containing images: ")

    # Validate the input directory
    if not os.path.isdir(input_dir):
        print("Error: Input directory does not exist.")
        sys.exit(1)

    # Ask the user for the grid dimensions (rows and columns)
    try:
        rows = int(input("Enter the number of rows (A): "))
        cols = int(input("Enter the number of columns (B): "))
    except ValueError:
        print("Error: Please enter valid integers for rows and columns.")
        sys.exit(1)

    # Stitch images into a grid based on user input
    result = stitch_images_in_grid(input_dir, rows, cols)
    
    if result:
        result.show()  # Display the stitched image
        
        # Generate the output file name based on input file names and current timestamp
        image_files = os.listdir(input_dir)
        output_filename = generate_output_filename(image_files)
        
        # Save the stitched image to a file with the generated output filename
        output_path = os.path.join(input_dir, output_filename)
        result.save(output_path)  # Save the stitched image to a file
        print(f"Stitched image saved to: {output_path}")

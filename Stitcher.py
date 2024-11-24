from PIL import Image
import os
import sys

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
        images.append(img)
    
    # Check if we have enough images for the grid
    if len(images) < rows * cols:
        print(f"Warning: Only {len(images)} images found, which is less than the requested {rows * cols} images for the grid.")
    
    # Resize images to fit in the grid (optional)
    width, height = images[0].size
    grid_width = width * cols
    grid_height = height * rows
    
    result_image = Image.new('RGB', (grid_width, grid_height))

    # Paste the images onto the result image
    x_offset = 0
    y_offset = 0
    for i in range(len(images)):
        img = images[i]
        result_image.paste(img, (x_offset, y_offset))

        # Move to the next column
        x_offset += img.width
        if (i + 1) % cols == 0:  # Move to the next row after the last column
            x_offset = 0
            y_offset += img.height

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

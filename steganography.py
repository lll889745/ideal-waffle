from PIL import Image
import numpy as np
import random

def create_random_gray_image(image_path):
    # Generate a random gray image
    width, height = 256, 256
    data = np.random.randint(0, 256, (height, width), dtype=np.uint8)
    image = Image.fromarray(data, 'L')
    image.save(image_path)

def hide_data_in_image(image_path, binary_data):
    # Load the image
    img = Image.open(image_path)
    pixels = np.array(img)

    # Hide data in the LSB of each pixel
    data_index = 0
    height, width = pixels.shape
    for i in range(height):
        for j in range(width):
            if data_index < len(binary_data):
                # Get the current pixel value
                current_pixel = pixels[i, j]
                # Modify the LSB of the pixel value
                if binary_data[data_index] == '1':
                    pixels[i, j] = current_pixel | 3  # Make sure the last bit is 1
                else:
                    pixels[i, j] = current_pixel & ~3 # Make sure the last bit is 0
                data_index += 1
            else:
                break

    # Save the modified image
    new_img = Image.fromarray(pixels, 'L')
    new_image_path = image_path.replace('.bmp', '_modified.bmp')
    new_img.save(new_image_path)
    return new_image_path

def extract_data_from_image(image_path, data_length):
    # Load the image
    img = Image.open(image_path)
    pixels = np.array(img)
    
    # Extract data from the LSB of each pixel
    binary_data = ''
    height, width = pixels.shape
    for i in range(height):
        for j in range(width):
            if len(binary_data) < data_length:
                # Extract the LSB of the pixel value
                binary_data += str(pixels[i, j] & 1)
            else:
                break

    return binary_data

def main():
    # Change file path here
    original_image_path = 'original.bmp'
    create_random_gray_image(original_image_path)

    # Generate random binary data
    data_length = 10000 # Change length of the binary data here
    random_binary_data = ''.join([str(random.randint(0, 1)) for _ in range(data_length)])
    
    # Hide data
    modified_image_path = hide_data_in_image(original_image_path, random_binary_data)
    
    # Extract data
    extracted_data = extract_data_from_image(modified_image_path, data_length)
    
    # Check if the extracted data matches the original data
    print("Random binary data:  ", random_binary_data)
    print("Extract binary data: ", extracted_data)
    print("Data match: ", random_binary_data == extracted_data)

if __name__ == '__main__':
    main()

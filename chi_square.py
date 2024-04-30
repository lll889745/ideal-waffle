import numpy as np
from scipy.stats import chi2
from PIL import Image

def calculate_chi_square(image_path):
    # Load the image & convert to grayscale
    img = Image.open(image_path)
    img = img.convert('L')
    pixels = np.array(img)
    
    # Compute the histogram of the image
    hist = np.bincount(pixels.flatten(), minlength=256)

    # Calculate the chi-square statistic
    chi_square_stat = 0
    degrees_of_freedom = 0
    for i in range(0, 256, 2):
        if i+1 >= len(hist):
            break
        
        h2i = hist[i]
        h2i1 = hist[i+1]
        h2i_star = (h2i + h2i1) / 2
        
        if h2i_star > 0:
            chi_square_stat += ((h2i - h2i_star)**2 + (h2i1 - h2i_star)**2) / h2i_star
            degrees_of_freedom += 1

    # Calculate the p-value
    p_value = 1 - chi2.cdf(chi_square_stat, degrees_of_freedom-1)
    return chi_square_stat, p_value, degrees_of_freedom-1

def test_steganography_detection(image_path):
    chi_square, p_value, df = calculate_chi_square(image_path)
    print(f"Chi-Square Statistic: {chi_square}")
    print(f"Degrees of Freedom: {df}")
    print(f"P-value: {p_value}")
    print("Steganography likely present." if p_value < 0.05 else "No steganography detected")

if __name__ == '__main__':
    print("Original image:")
    test_steganography_detection('original.bmp')
    print("\nModified image:")
    test_steganography_detection('original_modified.bmp')
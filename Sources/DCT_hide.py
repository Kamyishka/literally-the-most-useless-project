# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~ Encode secret message in image using DCT steganography ~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# ~~~~~~~~~~ External libraries ~~~~~~~~~~ #
from skimage.io import imread, imsave
from skimage.color import rgb2ycbcr, ycbcr2rgb
from skimage import img_as_float, img_as_ubyte
import numpy as np
import sys

# ~~~~~~~~~~~~~~ Source code ~~~~~~~~~~~~~ #
from dct_processing import dct_process_channel as dct
from dct_processing import idct_process_channel as idct
from extra import file_to_bin, bin_to_file
from extra import generate_difference


# the value lying in the interval [1; 99],
# which determines the image quality
_quality = 90

# Input: RGB-image (container), file name with extension (secret message)
# Output: saves a PNG stego-image with the given name (optional)
def dct_hide(img, filename, out_name='output', N=8, difference=False):
    # Save original image
    original = img.copy()

    # Find out the size of the image and the number of channels
    a, b = img.shape[:2]
    c = 3 if len(img.shape) == 3 else 1

    # # Receiving bitstream of the secret message
    data = file_to_bin(filename)

    # Check the capacity of the image
    if len(data) > (a // 8) * (b // 8) * 3:
        print("File is too large")
        return
    
    index = 0
    if c == 3:
        # Transition to YCbCr color space
        newimg = rgb2ycbcr(img)

        # Calculation of DCT coefficients on each channel
        Y =  dct(newimg[..., 0], _quality)
        Cb = dct(newimg[..., 1], _quality)
        Cr = dct(newimg[..., 2], _quality)
        newimg = np.dstack((Y, Cb, Cr))

        # Applying the LSB method to the coefficients in each NxN block
        for i in range(0, a, 8):
            for j in range(0, b, 8):
                for k in range(c):
                    if index + 1 < len(data):
                        newimg[i, j, k] += -(int(newimg[i, j, k]) % 2) + int(data[index])
                        index += 1


        # Inverse DCT to get new YCbCr pixel values
        Y =  idct(newimg[..., 0], _quality)
        Cb = idct(newimg[..., 1], _quality)
        Cr = idct(newimg[..., 2], _quality)
        newimg = np.dstack((Y, Cb, Cr))

        # Transition to RGB color space
        img = np.clip(0, 1.0, ycbcr2rgb(newimg))
        img = img_as_ubyte(img)

        # Generate difference between the original image and the output
        if difference:
            generate_difference(original, img)

        # The file must be saved without compression
        imsave(out_name + '.png', img)


def main():
    if len(sys.argv) < 3:
        print("Specify the path to the photo and file.")
    else:
        try:
            img = imread(sys.argv[1])
            file = open(sys.argv[2])
        except FileNotFoundError:
            print("This file does not exist.")
            exit()

        print("Do you want to generate difference image? (y/n):", end='')
        answer = input()
        if answer.lower() == 'y' or answer.lower() == 'yes':
            if len(sys.argv) == 4:
                dct_hide(img, sys.argv[2], sys.argv[3], difference=True)
            else:
                dct_hide(img, sys.argv[2], difference=True)
        else:
            if len(sys.argv) == 4:
                dct_hide(img, sys.argv[2], sys.argv[3])
            else:
                dct_hide(img, sys.argv[2])
    

if __name__ == '__main__':
    main()

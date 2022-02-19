# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~ Decode hidden message in image using DCT steganography ~~~~~~~ #
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

# Some of the images in the examples are not readable by the library
from PIL import PngImagePlugin
PngImagePlugin.MAX_TEXT_CHUNK = 500 * (1024**2)

_quality = 70

# Input: stego RGB-image
# Output: saves a hidden file with the given name (optional)
def dct_reveal(img, out_name='output_file', N=8):
    a, b = img.shape[:2]
    c = 3 if len(img.shape) == 3 else 1

    if c == 3:
        bitstream = []

        # Transition to YCbCr color space
        newimg = rgb2ycbcr(img)

        # Calculation of DCT coefficients on each channel
        Y =  dct(newimg[..., 0], _quality)
        Cb = dct(newimg[..., 1], _quality)
        Cr = dct(newimg[..., 2], _quality)
        newimg = np.dstack((Y, Cb, Cr))
        
        # Retrieving LSB from DCT coefficients in each NxN block
        for i in range(0, a, 8):
            for j in range(0, b, 8):
                for k in range(c):
                    bitstream.append(str(int(abs(newimg[i + 1, j + 1, k])) % 2))

        # Convert the bitstream to a file
        bin_to_file(bitstream, out_name)


def main():
    if len(sys.argv) < 2:
        print("Specify the path to the photo.")
    else:
        try:
            img = imread(sys.argv[1])

            if len(sys.argv) == 3:
                dct_reveal(img, sys.argv[2])
            else:
                dct_reveal(img)
        except FileNotFoundError:
            print("This file does not exist.")
    

if __name__ == '__main__':
    main()

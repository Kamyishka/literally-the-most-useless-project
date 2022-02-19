# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~ Decode secret message in image using PVD steganography ~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# ~~~~~~~~~~ External libraries ~~~~~~~~~~ #
from skimage.io import imread, imsave
import numpy as np
import sys

# ~~~~~~~~~~~~~~ Source code ~~~~~~~~~~~~~ #
from extra import bin_to_file, embed_number

# Some of the images in the examples are not readable by the library
from PIL import PngImagePlugin
PngImagePlugin.MAX_TEXT_CHUNK = 500 * (1024**2)

def pvd_reveal(img, out_name='output_file'):
    # Find out the size of the image and the number of channels
    a, b = img.shape[0], img.shape[1]
    c = 3 if len(img.shape) == 3 else 1

    # If the width of the image is odd, the last column can be ignored
    b -= b % 2

    bitstream = []
    for i in range(a):
        for j in range(0, b, 2):
            for k in range(c):
                # Find out the difference between two consecutive pixels
                dif = 0
                if c == 1:
                    dif = max(img[i, j + 1], img[i, j]) - min(img[i, j + 1], img[i, j])
                else:
                    dif = max(img[i, j + 1, k], img[i, j, k]) - min(img[i, j + 1, k], img[i, j, k])

                # Find out how many bits have been embedded, and the boundaries of the interval in which the difference lies
                emb = embed_number(dif)

                # Restore embedded number
                secret = emb[2] - dif

                # Convert the number into a bits and add to bitstream
                bits = bin(secret)[2:].rjust(emb[0], "0")
                bitstream.extend(bits)

    # Convert the bitstream to a file
    bin_to_file(bitstream, out_name)


def main():
	if len(sys.argv) == 1:
		print("Specify the path to the photo.")
	else:
		try:
			image = imread(sys.argv[1])
			pvd_reveal(image)
		except FileNotFoundError:
			print("This file does not exist.")


if __name__ == '__main__':
	main()

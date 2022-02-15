# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~ Decode secret message in image using modified PVD steganography ~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# ~~~~~~~~~~ External libraries ~~~~~~~~~~ #
from skimage.io import imread, imsave
import numpy as np
import sys

# ~~~~~~~~~~~~~~ Source code ~~~~~~~~~~~~~ #
from extra import bin_to_file, embed_number, pixel_dif

def cool_pvd_reveal(img, out_name='output_file'):
    # Find out the size of the image and the number of channels
    a, b = img.shape[0], img.shape[1]
    c = 3 if len(img.shape) == 3 else 1

    bitstream = []
    for k in range(c):
        for i in range(a):
            j = 0
            while j + 1 < b:

                # Find out the difference between two consecutive pixels
                if c == 1:
                    dif = pixel_dif(img[i, j + 1], img[i, j])
                else:
                    dif = pixel_dif(img[i, j + 1, k], img[i, j, k])

                # Find out how many bits to embed, and the boundaries of the interval in which the difference lies
                emb = embed_number(dif)

                # Restore embedded number
                secret = emb[2] - dif

                # Convert the number into a bits and add to bitstream
                bits = bin(secret)[2:].rjust(emb[0], "0")
                bitstream.extend(bits)

                # If the first pixel in the pair is odd, the next pixel must be skipped
                if c == 1:
                    if img[i, j] % 2 == 0:
                        j += 2
                    else:
                        j += 3
                else:
                    if img[i, j, k] % 2 == 0:
                        j += 2
                    else:
                        j += 3

    # Convert the bitstream to a file
    bin_to_file(bitstream, out_name)


def main():
	if len(sys.argv) == 1:
		print("Specify the path to the photo.")
	else:
		try:
			image = imread(sys.argv[1])
			cool_pvd_reveal(image)
		except FileNotFoundError:
			print("This file does not exist.")


if __name__ == '__main__':
	main()

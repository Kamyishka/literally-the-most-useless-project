# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~ Decode secret message in image using LSB steganography ~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# ~~~~~~~~~~ External libraries ~~~~~~~~~~ #
from skimage.io import imread, imsave
import sys

# ~~~~~~~~~~~~~~ Source code ~~~~~~~~~~~~~ #
from extra import bin_to_file

# Some of the images in the examples are not readable by the library
from PIL import PngImagePlugin
PngImagePlugin.MAX_TEXT_CHUNK = 500 * (1024**2)

def lsb_reveal(img, bits=1, out_name='output_file'):
	# Find out the size of the image and the number of channels
	a, b = img.shape[0], img.shape[1]
	c = 3 if len(img.shape) == 3 else 1


	bitstream = []
	for i in range(a):
		for j in range(b):
			for k in range(c):
				# Get the last bits of pixel and add them to the bitstream
				if c == 1:
					bitstream.extend(bin(img[i, j] % (2 ** bits))[2:].rjust(bits, "0"))
				else:
					bitstream.extend(bin(img[i, j, k] % (2 ** bits))[2:].rjust(bits, "0"))

	# Convert the bitstream to a file
	bin_to_file(bitstream, out_name)


def main():
	if len(sys.argv) == 1:
		print("Specify the path to the photo.")
	else:
		try:
			image = imread(sys.argv[1])
			lsb_reveal(image, 1)
		except FileNotFoundError:
			print("This file does not exist.")


if __name__ == '__main__':
	main()

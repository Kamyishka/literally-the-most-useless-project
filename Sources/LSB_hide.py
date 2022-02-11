# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~ Encode secret message in image using LSB steganography ~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# ~~~~~~~~~~ External libraries ~~~~~~~~~~ #
from skimage.io import imread, imsave
import sys

# ~~~~~~~~~~~~~~ Source code ~~~~~~~~~~~~~ #
from extra import file_to_bin

def lsb_hide(img, filename, bits=1, out_name='output'):
    # Find out the size of the image and the number of channels
    a, b = img.shape[0], img.shape[1]
    c = 3 if len(img.shape) == 3 else 1
    
    # Receiving bitstream of the secret message
    bitstream = file_to_bin(filename, bits)

    # Check the capacity of the image
    capacity = a * b * c;
    if capacity < len(bitstream):
        print("File is too large!")
        return

    i, x = 0, 0
    while i < a and x + 1 < len(bitstream):
        for j in range(b):
            k = 0
            while k < c and x + 1 < len(bitstream):
                # Delete the last bits and replace with the secret message bits
                if c == 1:
                    img[i, j] += -(img[i, j] % (2 ** bits)) + int(bitstream[x], base=2)
                else:
                    img[i, j, k] += -(img[i, j, k] % (2 ** bits)) + int(bitstream[x], base=2)
                k += 1
                x += 1
        i += 1

    # The file must be saved without compression
    imsave(out_name + '.png', img)


def main():
    if len(sys.argv) < 3:
        print("Specify the path to the photo and file.")
    else:
        try:
            img = imread(sys.argv[1])
            file = open(sys.argv[2])
            if len(sys.argv) == 4:
                print(lsb_hide(img, sys.argv[2], 1, sys.argv[3]))
            else:
                print(lsb_hide(img, sys.argv[2], 1))
        except FileNotFoundError:
            print("This file does not exist.")


if __name__ == '__main__':
    main()

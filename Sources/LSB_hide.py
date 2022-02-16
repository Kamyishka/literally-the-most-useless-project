# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~ Encode secret message in image using LSB steganography ~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# ~~~~~~~~~~ External libraries ~~~~~~~~~~ #
from skimage.io import imread, imsave
import sys

# ~~~~~~~~~~~~~~ Source code ~~~~~~~~~~~~~ #
from extra import file_to_bin, generate_difference

def lsb_hide(img, filename, bits=1, out_name='output', difference=False):
    # Save original image
    original = img.copy()

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
                lsb_hide(img, sys.argv[2], 1, sys.argv[3], True)
            else:
                lsb_hide(img, sys.argv[2], 1, difference=True)
        else:
            if len(sys.argv) == 4:
                lsb_hide(img, sys.argv[2], 1, sys.argv[3])
            else:
                lsb_hide(img, sys.argv[2], 1)

if __name__ == '__main__':
    main()

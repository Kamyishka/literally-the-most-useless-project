# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~ Encode secret message in image using PVD steganography ~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# ~~~~~~~~~~ External libraries ~~~~~~~~~~ #
from skimage.io import imread, imsave
import sys

# ~~~~~~~~~~~~~~ Source code ~~~~~~~~~~~~~ #
from extra import file_to_bin, embed_number, change_difference
from extra import generate_difference

def pvd_hide(img, filename, out_name='output', difference=False):
    # Save original image
    original = img.copy()

    # Find out the size of the image and the number of channels
    a, b = img.shape[0], img.shape[1]
    c = 3 if len(img.shape) == 3 else 1
    
    # Receiving bitstream of the secret message
    data = file_to_bin(filename)

    # Index of current bit in bitsteam
    x = 0

    # If the width of the image is odd, the last column can be ignored
    b -= b % 2

    i = 0
    capacity = 0
    message_not_ended = True
    while i < a and message_not_ended:
        for j in range(0, b, 2):
            for k in range(c):
                # Find out the difference between two consecutive pixels
                dif = 0
                if c == 1:
                    dif = max(img[i, j + 1], img[i, j]) - min(img[i, j + 1], img[i, j])
                else:
                    dif = max(img[i, j + 1, k], img[i, j, k]) - min(img[i, j + 1, k], img[i, j, k])

                # Find out how many bits to embed, and the boundaries of the interval in which the difference lies
                emb = embed_number(dif)

                # Exit if all the secret message is already embedded
                if x + emb[0] >= len(data):
                    message_not_ended = False
                    print("Success (message ended).")
                    break

                # Convert the required number of bits into a number
                bits = int(''.join(data[x:x + emb[0]]), base=2)

                # Find out the new difference between pixels            
                newdif = emb[2] - bits

                # Changing the pixel difference to a new one
                if c == 1:
                    img[i, j], img[i, j + 1] = change_difference(img[i, j], img[i, j + 1], dif, newdif)
                else:
                    img[i, j, k], img[i, j + 1, k] = change_difference(img[i, j, k], img[i, j + 1, k], dif, newdif)

                x += emb[0]
                capacity += emb[0]
        i += 1
    
    # Generate difference between the original image and the output
    if difference:
        generate_difference(original, img)

    # The file must be saved without compression
    imsave(out_name + '.png', img)
    return capacity


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
                pvd_hide(img, sys.argv[2], sys.argv[3], True)
            else:
                pvd_hide(img, sys.argv[2], difference=True)
        else:
            if len(sys.argv) == 4:
                pvd_hide(img, sys.argv[2], sys.argv[3])
            else:
                pvd_hide(img, sys.argv[2])


if __name__ == '__main__':
    main()

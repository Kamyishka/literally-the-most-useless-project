# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~ Encode secret message in image using modified PVD steganography ~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


# ~~~~~~~~~~ External libraries ~~~~~~~~~~ #
from skimage.io import imread, imsave
import sys

# ~~~~~~~~~~~~~~ Source code ~~~~~~~~~~~~~ #
from extra import file_to_bin, bin_to_file
from extra import embed_number, change_difference, pixel_dif

def search_best_pairs(row):
    # We need to always include the first pair in the answer
    first_pair = [(0, embed_number(pixel_dif(row[1], row[0])))]
        
    i = 4

    # Maximum possible capacity for all pixels up to i - 2 and i - 1 respectively
    a, b = 0, embed_number(pixel_dif(row[3], row[2]))[0]

    # To save memory, we will store only two arrays and swap them around
    is_swaped = True

    # Two arrays for dynamic programming, contain pairs of indexes of 
    # the first element of a pair of pixels and the number of bits to embed in that pair
    dp1, dp2 = [], []
    is_first_0_255 = True if (row[0], row[1]) == (0, 255) else False
    is_first_255_0 = False
    is_0_255 = False

    if (row[0], row[1]) == (255, 0):
        dp1.append((3, embed_number(pixel_dif(row[4], row[3]))))
        dp2.append((3, embed_number(pixel_dif(row[4], row[3]))))
        a = embed_number(pixel_dif(row[4], row[3]))[0]
        b = embed_number(pixel_dif(row[4], row[3]))[0]
        i = 5
        is_first_255_0 = True
        is_swaped = False
    else:
        dp2.append((2, embed_number(pixel_dif(row[3], row[2]))))
    while i < len(row):
        embed = embed_number(pixel_dif(row[i], row[i - 1]))
        if is_swaped and len (dp2) > 0 and (dp2[-1][0],row[dp2[-1][0]],row[dp2[-1][0] + 1]) == (i - 2, 255, 0):
            dp1 = dp2.copy()
            a = b
            i += 1
        elif not is_swaped and len (dp1) > 0 and (dp1[-1][0],row[dp1[-1][0]],row[dp1[-1][0] + 1]) == (i - 2, 255, 0):
            dp2 = dp1.copy()
            a = b
            i += 1
        elif (is_swaped and len (dp2) > 0 and (dp2[-1][0],row[dp2[-1][0]],row[dp2[-1][0] + 1]) == (i - 2, 0, 255)) or (not is_swaped and len (dp1) > 0 and (dp1[-1][0],row[dp1[-1][0]],row[dp1[-1][0] + 1]) == (i - 2, 0, 255)):
            if i == len(row) - 1:
                break
            else:
                if is_first_0_255 and i == 4:
                    dp1 = dp2.copy()
                    a = b
                dp1.append((i, embed))
                dp2.append((i, embed))
                b += embed_number(pixel_dif(row[i], row[i + 1]))[0]
                a = b
                is_0_255 = True
                if is_swaped:
                    dp1 = dp2.copy()
                else:
                    dp2 = dp1.copy()
                i += 1
        else:
            if a + embed[0] > b and (not is_first_255_0 or i != 5) and not is_0_255:
                if is_swaped:
                    dp1.append((i - 1, embed))
                else:
                    dp2.append((i - 1, embed))
                b, a = a + embed[0], b
            else:
                if is_swaped:
                    dp1 = dp2.copy()
                else:
                    dp2 = dp1.copy()
                a = b
            is_swaped = not is_swaped
            if is_0_255:
                is_0_255 = False
        i += 1
    # Add first pair to an answer and return it
    return (first_pair + dp2.copy() if is_swaped else first_pair + dp1.copy())


# Change the numbers in [0; 255] so as to keep their difference, 
# but change the parity of the first number to the required number, avoiding an overflow.
def change_parity(a, b, odd):
    if odd and a % 2 == 0:
        if b == 255:
            a -= 1
            b -= 1
        else:
            a += 1
            b += 1
    elif not odd and a % 2 != 0:
        if b == 0:
            a += 1
            b += 1
        else:
            a -= 1
            b -= 1
    return a, b


def cool_pvd_hide(img, filename, out_name='output'):
    # Find out the size of the image and the number of channels
    a, b = img.shape[0], img.shape[1]
    c = 3 if len(img.shape) == 3 else 1

    # Receiving bitstream of the secret message
    data = file_to_bin(filename)

    # Index of current bit in bitsteam
    x = 0

    capacity = 0
    message_not_ended = True
    for k in range(c):
        i = 0
        while i < a and message_not_ended:

            if c == 1:
                row = search_best_pairs(img[i])
            else:
                row = search_best_pairs(img[i,:,k])

            for pairs in range(len(row)):
                j = row[pairs][0]
                bits = row[pairs][1][0]
                right = row[pairs][1][2]

                # Find out the difference between two consecutive pixels
                if c == 1:
                    dif = pixel_dif(img[i, j + 1], img[i, j])
                else:
                    dif = pixel_dif(img[i, j + 1, k], img[i, j, k])

                # Exit if all the secret message is already embedded
                if x + bits >= len(data):
                    message_not_ended = False
                    print("Success (message ended).")
                    break

                # Convert the required number of bits into a number
                secret = int(''.join(data[x:x + bits]), base=2)

                # Find out the new difference between pixels    
                newdif = right - secret

                # Changing the pixel difference to a new one
                if c == 1:
                    img[i, j], img[i, j + 1] = change_difference(img[i, j], img[i, j + 1], dif, newdif)
                    if k == 2:
                        print("idfoif")
                else:
                    img[i, j, k], img[i, j + 1, k] = change_difference(img[i, j, k], img[i, j + 1, k], dif, newdif)

                # If the next pixel after a pair is "skipped," then its first element must be an odd one
                if c == 1 and pairs != len(row) - 1:
                    img[i, j], img[i, j + 1] = change_parity(img[i, j], img[i, j + 1], (row[pairs + 1][0] == j + 3))
                elif pairs != len(row) - 1:
                    img[i, j, k], img[i, j + 1, k] = change_parity(img[i, j, k], img[i, j + 1, k], (row[pairs + 1][0] == j + 3))


                x += bits
                capacity += bits
            i += 1
    
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
            if len(sys.argv) == 4:
                coo_pvd_hide(img, sys.argv[2], sys.argv[3])
            else:
                cool_pvd_hide(img, sys.argv[2])
        except FileNotFoundError:
            print("This file does not exist.")


if __name__ == '__main__':
    main()
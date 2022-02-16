# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~ Other functions ~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


# ------------------------- External libraries ------------------------ #
import numpy as np
from skimage.io import imsave
from skimage import img_as_float, img_as_ubyte


# --------- Section 1: file handling and conversion to binary --------- #

# Input:  file name (with extension)
# Output: list of grouped bits as strings
def file_to_bin(filename, bits=1):
    bin_file = open(filename, 'rb').read()
    bin_strings = map(bin, list(bin_file))

    binlist = list(''.join([i[2:].rjust(8, "0") for i in bin_strings]))

    if bits == 1:
        return binlist

    answer, s = list(), ''
    for i in range(len(binlist)):
        s += binlist[i]
        if i % bits == bits - 1:
            answer.append(s)
            s = ''
    return answer

# Input:  list of grouped bits as strings
# Output: the file with the specified name is saved
def bin_to_file(binlist, filename='output_file'):
	s = ''
	bytes_list = list()
	for i in range(len(binlist)):
		s += binlist[i]
		if i % 8 == 7:
			bytes_list.append(int(s, base=2))
			s = ''

	binary_data = bytes(bytes_list)
	out_file = open(filename, 'wb')
	out_file.write(binary_data)
	out_file.close()


# ------------------- Section 2: functions for PVD -------------------- # 

# Input: difference value between two pixels
# Output: number of bits to embed, left and right 
# boundaries of the interval in which the difference lies
def embed_number(n):
    srange = (0, 2, 4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256)
    l , r = 0, len(srange) - 1
    while r - l > 1:
        mid = (l + r) // 2
        if srange[mid] >= n:
            r = mid
        else:
            l = mid
    return int(np.log2(srange[r] - srange[l])), srange[l], srange[r]

# Input: three numbers in [0; 255]
# Output: two numbers in [0; 255] altered so that the difference
# between them equals the third one
def change_difference(a, b, dif, newdif):
    swap = False
    if a > b:
        a, b = b, a
        swap = True
    
    upper_add = abs(newdif - dif) // 2 + abs(newdif - dif) % 2
    lower_add = abs(newdif - dif) // 2

    # Overflow handling
    if newdif > dif:
        if a - upper_add < 0:
            shift = upper_add - a
            upper_add -= shift
            lower_add += shift

        if b + lower_add > 255:
            shift = b + lower_add - 255
            lower_add -= shift
            upper_add += shift

        a -= upper_add
        b += lower_add
    else:
        a += upper_add
        b -= lower_add

    if swap:
        a, b = b, a
    return a, b


def pixel_dif(a, b):
    return max(a, b) - min(a, b)



# ----------------- Section 3: additional functionality ----------------- #

# Input: two images of the same shape
# Output: 
def generate_difference(original, output):
    # Find out the number of channels
    c = 3 if len(original.shape) == 3 else 1
    dif = abs(img_as_float(original) - img_as_float(output))
    if c == 1:
        dif -= dif.min()
        dif = dif / dif.max()
        imsave("difference.png", img_as_ubyte(dif))
    else:
        black = original[:,:,0] * 0
        dif_r = dif[:, :, 0]
        dif_g = dif[:, :, 1]
        dif_b = dif[:, :, 2]
        dif = np.dstack((dif_b, dif_g, dif_r))
        dif -= dif.min()
        dif = dif * 1 / dif.max()

        dif_r -= dif_r.min()
        dif_r = dif_r / dif_r.max()
        dif_r = np.dstack((dif_r, black, black))

        dif_g -= dif_g.min()
        dif_g = dif_g / dif_g.max()
        dif_g = np.dstack((black, dif_g, black))

        dif_b -= dif_b.min()
        dif_b = dif_b / dif_b.max()
        dif_b = np.dstack((black, black, dif_b))

        imsave("difference.png", img_as_ubyte(dif))
        imsave("differencer.png", img_as_ubyte(dif_r))
        imsave("differenceg.png", img_as_ubyte(dif_g))
        imsave("differenceb.png", img_as_ubyte(dif_b))
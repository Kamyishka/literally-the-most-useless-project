# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~ Other functions ~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


# ------------------------- External libraries ------------------------ #
from numpy import log2


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
    srange = (0, 2, 4, 8, 16, 32, 64, 128, 256)
    l , r = 0, len(srange) - 1
    while r - l > 1:
        mid = (l + r) // 2
        if srange[mid] >= n:
            r = mid
        else:
            l = mid
    return int(log2(srange[r] - srange[l])), srange[l], srange[r]

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

    if newdif > dif:
        if a - upper_add < 0:
            shift = upper_add - a
            upper_add -= shift
            lower_add += shift
            #print("1")
        if b + lower_add > 255:
            shift = b + lower_add - 255
            lower_add -= shift
            upper_add += shift
            #print("2")

        a -= upper_add
        b += lower_add
    else:
        a += upper_add
        b -= lower_add

    if swap:
        a, b = b, a
    return a, b
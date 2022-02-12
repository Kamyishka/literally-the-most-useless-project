# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~ Calculation of discrete cosine transform and quantization ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

import numpy as np

class quantization_class():

    def __init__(self):
        self.count = 0

    # Input: image compression quality
    # Output: quantization matrix
    def get_quantization_matrix(self, quality):
        Q = np.array([[16,  11,  10,  16,  24,  40,  51,  61],
                      [12,  12,  14,  19,  26,  58,  60,  55],
                      [14,  13,  16,  24,  40,  57,  69,  56],
                      [14,  17,  22,  29,  51,  87,  80,  62],
                      [18,  22,  37,  56,  68,  109, 103, 77],
                      [24,  35,  55,  64,  81,  104, 113, 92],
                      [49,  64,  78,  87,  103, 121, 120, 101],
                      [72,  92,  95,  98,  112, 100, 103, 99]])

        if quality == 50:
            return Q
        elif quality > 50:
            Q = Q * np.divide(100 - quality,  50)
            Q = np.where(Q > 255, 255, Q)
            return Q
        else:
            Q = np.divide(Q * 50, quality)
            Q = np.where(Q > 255, 255, Q)
            return Q

    # Input: DCT coefficients (NxN block)
    # Output: quantized coefficients (NxN block)
    def quantize(self, matrix, quality, N=8):
        Q = self.get_quantization_matrix(quality)
        for i in range(N):
            for j in range(N):
                matrix[i][j] = np.around(np.divide(matrix[i][j], Q[i][j]))
        return matrix

    # Input: quantized coefficients (NxN block)
    # Output: DCT coefficients (NxN block)
    def inverse_quantize(self, matrix, quality, N=8):
        Q = self.get_quantization_matrix(quality)
        for i in range(N):
            for j in range(N):
                matrix[i][j] *= Q[i][j]
        return matrix


class DCT_class():

    def __init__(self):
        self.count = 0

    def point(self, N=8):
        D = np.random.randn(N, N)

        # additional variables to speed up calculations
        u = np.sqrt(2 / N)
        v = 1 / np.sqrt(N)
        w = np.pi / (2 * N)

        for i in range(N):
            for j in range(N):
                D[i, j] = v if i == 0 else u * np.cos(((2 * j + 1) * i) * w)

        return D

    # calculate DCT II for NxN block
    def calculate_DCT(self, a):
        dct_matrix = self.point()
        return (dct_matrix @ a @ dct_matrix.T)


    # calculate DCT III (inverse DCT) for NxN block
    def calculate_IDCT(self, a):
        dct_matrix = self.point()
        return (dct_matrix.T @ a @ dct_matrix)


# Input: single-channel YCbCr image
# Output: quantized DCT coefficients
def dct_process_channel(img, quality, N=8):
    a, b = img.shape[:2]

    # center values relative to zero
    temp = img.copy() - 128

    # сalculate result for each NxN block
    dct = DCT_class()
    qnt = quantization_class()
    for i in range(0, a, N):
        for j in range(0, b, N):
            temp[i:i + N, j:j + N] = dct.calculate_DCT(temp[i:i + N, j:j + N])
            if quality != 0:
                temp[i:i + N, j:j + N] = qnt.quantize(temp[i:i + N, j:j + N], quality)
    return temp

# Input: quantized DCT coefficients
# Output: single-channel YCbCr image
def idct_process_channel(img, quality, N=8):
    a, b = img.shape[:2]
    temp = img.copy()

    # сalculate result for each NxN block
    dct = DCT_class()
    qnt = quantization_class()
    for i in range(0, a, N):
        for j in range(0, b, N):
            if quality != 0:
                temp[i:i + N, j:j + N] = qnt.inverse_quantize(img[i:i + N, j:j + N], quality)
            temp[i:i + N, j:j + N] = dct.calculate_IDCT(img[i:i + N, j:j + N])
    return temp + 128

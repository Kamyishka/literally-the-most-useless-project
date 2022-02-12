# literally-the-most-useless-project
[Different steganography methods with examples and my own small image database]

This project currently contains three different steganography methods in digital images and a small database of images.

# ------------------------------------------------------------------------------- #

Existing methods (Source/):
- Least Significant Bit      (LSB).
  - LSB_hide.py - hides the message in the image using the classic LSB method
  - LSB_reveal.py - reveals the message hidden by this method
- Pixel-value Differencing   (PVD).
  - PVD_hide.py - hides the message in the image using the classic PVD method
  - PVD_reveal.py - reveals the message hidden by this method
- Discrete Cosine Transform  (DCT).
  - DCT_hide.py - hides the message in the image using the classic DCT method (uses only one DC-coefficient in each block)
  - DCT_reveal.py - reveals the message hidden by this method
  - dct_processing.py - image preparation (discrete cosine transform, quantization, functions for channel processing)

# ------------------------------------------------------------------------------- #

Images for testing the methods (Examples/) are divided into four groups. 
1. 512px (22 images) - photos taken by me, size 512x512 in .png format.
Contains contrast photos (good for checking for overflow), photos with smooth areas such as the sky or walls 
(they show the difference, for example, between PVD and LSB), black and white, with lots of detail, etc.
2. 1024x (22 images) - the same images, but in better quality (1024x1024).
3. Classic (9 images) - images, standard for testing image processing methods, such as lenna, cameraman, moon.
Also contains color and black and white photos (from 256x256 to 1024x1024). 
Such images are often used in papers about steganography.
4. Other (6 images) - several non-square color photos.

Examples/ also contains some text files and a small watermark.jpg file as secret messages.

# ------------------------------------------------------------------------------- #

In development:
- error correction (hamming code) for DCT
- using multiple images as containers for a single message
- enhanced PVD using dynamic programming to increase capacity

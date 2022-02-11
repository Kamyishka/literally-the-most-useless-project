# literally-the-most-useless-project
[Different steganography methods with examples and my own small image database]

This project currently contains three different steganography methods in digital images and a (very) small database of images.

Existing methods (Source folder):
- Least Significant Bit      (LSB)
- Pixel-value Differencing   (PVD)
- Discrete Cosine Transform  (DCT)

There are two files for each method: one for hiding the secret message and one for revealing it.


Images for testing the methods (Examples folder) are divided into four groups. 
1. 512px - photos taken by me, size 512x512 in .png format
Contains contrast photos (good for checking for overflow), photos with smooth areas such as the sky or walls 
(they show the difference, for example, between pvd and lsb), black and white, with lots of detail, etc.
2. 1024x - the same images, but in better quality (1024x1024)
3. Classic - images, standard for testing image processing methods, such as lenna, cameraman, moon.
Also contains color and black and white photos (from 256x256 to 1024x1024). 
Such images are often used in papers about steganography.
4. Other - several large non-square color photos

It also contains some text files and a small .jpg file for testing.

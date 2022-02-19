# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~ Generate PVD vs MPVD bpb plot ~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


# ~~~~~~~~~~ External libraries ~~~~~~~~~~ #
import matplotlib.pyplot as plt
from skimage.io import imread
import numpy as np

# ~~~~~~~~~~~~~~ Source code ~~~~~~~~~~~~~ #
from MPVD_hide import cool_pvd_hide
from PVD_hide import pvd_hide


# Some of the images in the examples are not readable by the library
from PIL import PngImagePlugin
PngImagePlugin.MAX_TEXT_CHUNK = 500 * (1024**2)

# Includes images from 512px/ and Classic/
cat_par = ["autumn.png",       "autumn_kharkiv.png", "berries.png",        "blueberries.png",  "dandelion.png",
            "dawn.png",         "dispersion.png",     "earth.png",          "happy_asriel.png", "hiding_bird.png",
	      "insect.png",       "kitty.png",          "lilac.png",          "muffins.png",      "parrot.png",
	      "peppers.png",      "pink_sun.png",       "railway.png",        "rainbow.png",      "rats.png",
	      "sleeping_cat.png", "spring.png",         "summer_kharkiv.png", "sunset.png",       "town.png", 
	      "winter.png",       "boat.png",           "beans.png",          "couple.png",       "house.png",
	      "lenna.png",        "mandril.png",        "moon.png",           "pirate.png",       "resolution.png"]

# Receive image size in bytes
siz = []
for i in cat_par:
	img = imread(i)
	cc = len(img.shape)
	aa, bb = img.shape[0], img.shape[1]
	siz.append(aa * bb * cc)

# Receive capacity of the images using PVD
# pvd = [pvd_hide(imread(cat_par[i]), "big_text.txt") for i in range(len(cat_par))]
pvd = [999138, 493293, 252111, 760973, 687112, 510347, 814917, 491481, 680327, 454199,
       951805, 700060, 656677, 530763, 542722, 456418, 481342, 182094, 578502, 539328,
       726318, 645310, 432817, 522672, 807854, 552568, 231124, 127591, 149828, 142524,
       631999, 922783, 57546,  856355, 42967]
'''pvd = [1201581, 497265, 284312, 859643, 735021, 523096, 929662, 502086, 736798, 452110,
       1159741, 751252, 708365, 548975, 539788, 448132, 495897, 195207, 634304, 508122,
       807363, 696056, 429324, 522657, 926574, 600813, 243649, 133013, 154098, 140883,
       643819, 1107940, 60933, 873705, 44343]'''

# Calculate bits-per-byte
pvd = np.divide(pvd, siz)

# Receive capacity of the images using MPVD
# mpvd = [cool_pvd_hide(imread(cat_par[i]), "big_text.txt") for i in range(len(cat_par))]
mpvd = [1085896, 510394, 267784, 808236, 721450, 529269, 879007, 510427, 725159, 462655, 
        1034875, 751292, 686297, 551262, 568027, 467944, 497380, 189980, 606278, 566978,
        771184,  670864, 440655, 546443, 870539, 577982, 246190, 131249, 156981, 150213,
       672133, 1006826, 61225,  912314, 45265]
'''mpvd = [1342775, 523239, 315550, 953483, 803581, 549154, 1041446, 536515, 816257, 462534,
        1308500, 844781, 761904, 588431, 579621, 459020, 521107, 206723, 684831, 547744, 
        886068, 740942, 438542, 563857, 1029053, 645740, 270544, 138848, 166739, 152715, 
        712450, 1248753, 68535, 976354, 46089]'''

# Calculate bits-per-byte
mpvd = np.divide(mpvd, siz)

# Parallel sorting
indices = sorted(range(len(cat_par)), key=lambda i: pvd[i])
cat_par = [cat_par[i] for i in indices]
mpvd = [mpvd[i] for i in indices]
pvd = [pvd[i] for i in indices]

# Make grouped bars
width = 0.3
x = np.arange(len(cat_par))
fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, pvd,  width, label='Класичний РЗП',     color=(0, 0.5, 0.9))
rects2 = ax.bar(x + width/2, mpvd, width, label='Модифiкований РЗП', color=(0, 0.9, 0.6))

# Set titles
plt.ylabel("Кiлькiсть бiтiв на байт (bpb)", fontsize=16)
ax.set_title('Порiвняння мiсткостi зображень з використанням рiзних алгоритмiв', fontsize=24)
ax.set_ylim(0, 1.8)

# Remove ".png" from picture names to save space
ax.set_xticks(x)
ax.set_xticklabels([s[:-4] for s in cat_par], rotation=90)

# Make labels larger
ax.legend(prop={"size":18})
for label in ax.get_yticklabels():
	label.set_fontsize(18)

plt.show()
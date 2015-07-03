import numpy as np
import cv2
import os.path
import moviepy.editor as mpy

# Number of frames in resulting .gif, >=3
FRAMES = 18
# Number of frames per second
FPS = 10
# Size of 'pixels' in resulting .gif
SIZE = 10
# New value of black after transformation
BLACK = 80

# Load image
imgname = 'input.jpg'
if not os.path.isfile(imgname):
    raise ValueError('Image does not exist')
img = cv2.imread(imgname, cv2.IMREAD_COLOR)

height, width, channels = img.shape

# To avoid black areas in the image, convert it to LAB and transform lightness
def lighten(image, black):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    # Create a lightness transformation array
    lut = np.empty((1, 256, channels), np.uint8)
    for i in range(0, 256):
        lut[0, i, 0] = black + (i * (255 - black)) // 255
        lut[0, i, 1] = i
        lut[0, i, 2] = i

    # Transform image using multichannel LUT
    lab = cv2.LUT(lab, lut)

    # Convert image back to BGR
    bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    return bgr


img = lighten(img, BLACK)

# Size of image in 'big pixels'
heightbysize = (height + SIZE - 1) // SIZE
widthbysize = (width + SIZE - 1) // SIZE

# Create array of black images
gif = np.zeros((FRAMES, height, width, channels), np.uint8)

for xsize in range(0, heightbysize):
    for ysize in range(0, widthbysize):
        # Choose random frames
        rand = np.random.choice(FRAMES, channels, replace = False)
        for x in range(xsize * SIZE, min((xsize + 1) * SIZE, height)):
            for y in range(ysize * SIZE, min((ysize + 1) * SIZE, width)):
                px = img[x, y]
                # Transfer colors
                for i in range(0, channels):
                    # OpenCV uses BGR mode and MoviePy uses RGB mode
                    gif[rand[i], x, y, channels - 1 - i] = px[i]


# Transform sequence to list for ImageSequenceClip
gif = list(gif)

animation = mpy.ImageSequenceClip(gif, fps = FPS)
animation.write_gif('output.gif')

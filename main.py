import numpy as np
import matplotlib.pyplot as plt
from skimage import color


# fixed epsilon
def hue2colors(img):
    c = np.unique(image[:, :, 0])
    colors = []
    prev_color = -1
    a = []

    for i in c:
        if prev_color == -1:
            a.append(i)
        elif np.abs(i - prev_color) >= 0.02:
            mean = np.mean(a)
            if mean != 0.0:
                colors.append(mean)
            a = [i]
        else:
            a.append(i)
        prev_color = i

    colors.append(np.mean(a))
    return colors


# dynamic epsilon
def hue2colors2(img):
    c = np.unique(image[:, :, 0])
    colors = []
    e = np.diff(c).mean()
    prev_color = -1
    a = []

    for i in c:
        if prev_color == -1:
            a.append(i)
        elif np.abs(i - prev_color) >= e:
            mean = np.mean(a)
            if mean != 0.0:
                colors.append(mean)
            a = [i]
        else:
            a.append(i)
        prev_color = i

    colors.append(np.mean(a))
    return colors


path = './data/balls.png'

image = plt.imread(path)

image = color.rgb2hsv(image)

plt.figure()
plt.subplot(121)
plt.imshow(image)
plt.subplot(122)
plt.plot(np.unique(image[:, :, 0]), 'o')
print(hue2colors(image))
print(hue2colors2(image))
plt.show()

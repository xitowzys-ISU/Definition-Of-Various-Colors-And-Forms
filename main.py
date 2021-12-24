import numpy as np
import matplotlib.pyplot as plt

from skimage import color, filters
from skimage.measure import label, regionprops


def hue2colors(img):
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


def get_color(color: np.array, colors: np.array):
    max_abs = 1
    original_color = 0
    col = color[-1]
    for i in range(len(colors)):
        if abs(colors[i] - col) < max_abs:
            max_abs = abs(colors[i]-col)
            original_color = abs(colors[i])
    return original_color


def binarize(img):
    img = np.mean(img, 2)

    img[img < filters.threshold_otsu(img)] = 0
    img[img > 0] = 1

    return img


if __name__ == "__main__":
    rectangle_count, circle_count = 0, 0
    figures_colors = {'rectangle': {}, 'circle': {}}

    path = './data/balls_and_rects.png'

    image = plt.imread(path)
    image = color.rgb2hsv(image)
    binary_image = binarize(image)

    labeled = label(binary_image)
    regions = regionprops(labeled)
    colors = hue2colors(image)

    for region in regions:
        (min_row, min_col, max_row, max_col) = region.bbox

        region_image = image[min_row:max_row, min_col:max_col]

        # plt.imshow(region_image)
        # plt.show()

        region_colors = np.unique(region_image[:, :, 0])
        color = str(get_color(region_colors, colors))

        if region.extent == 1:
            rectangle_count += 1

            if color in figures_colors['rectangle']:
                figures_colors['rectangle'][color] += 1
            else:
                figures_colors['rectangle'][color] = 1

        else:
            circle_count += 1

            if color in figures_colors['circle']:
                figures_colors['circle'][color] += 1
            else:
                figures_colors['circle'][color] = 1

    print(f"Всего фигур: {rectangle_count + circle_count}")
    print(f"Всего прямоугольников: {rectangle_count}")
    print(f"Всего кругов: {circle_count}")

    print("-"*50)

    print(f"Прямоугольники по цветам: {figures_colors['rectangle']}")

    print(f"Круги по цветам: {figures_colors['circle']}")

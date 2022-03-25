from collections import Counter
from sklearn.cluster import KMeans
import cv2


# Image Resizing
def pre_process(raw_img):
    image = cv2.resize(raw_img, (900, 600), interpolation=cv2.INTER_AREA)
    image = image.reshape(image.shape[0] * image.shape[1], 3)
    return image


# Converting rgb_values to hex
def rgb_to_hex(rgb_color):
    hex_color = "#"
    for i in rgb_color:
        i = int(i)
        hex_color += ("{:02x}".format(i))
    return hex_color


def extract_colors(img):
    clf = KMeans(n_clusters=5)
    color_labels = clf.fit_predict(img)
    center_colors = clf.cluster_centers_
    counts = Counter(color_labels)
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [rgb_to_hex(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [str(tuple(int(j) for j in ordered_colors[i]))
                  for i in counts.keys()]
    color_count = [count for count in counts.values()]
    image_color_data = {
        "hex_colors": hex_colors,
        "rgb_colors": rgb_colors,
        "color_count": color_count
    }
    return image_color_data


def main(img_path=""):
    original_image = cv2.imread(
        f"{img_path}")
    image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    modified_image = pre_process(image)
    return extract_colors(modified_image)

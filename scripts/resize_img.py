import cv2
import numpy as np

# read img
image = cv2.imread("samples/")

# new size
new_width = 1024
new_height = 1024
resized_image = cv2.resize(image, (new_width, new_height))
# save
cv2.imwrite("resized_image.jpg", resized_image)

# keep the same shape
# original size
original_height, original_width = image.shape[:2]
black_pudding_image = np.zeros((new_width, new_height, 3), dtype=np.uint8)
scale = min(new_width / original_width, new_height / original_height)
same_ratio_image = cv2.resize(image, (original_width * scale, original_height * scale))
height_pudding = (new_height - original_height * scale) // 2
width_pudding = (new_width - original_width * scale) // 2
black_pudding_image[
    height_pudding : height_pudding + new_height,
    width_pudding : width_pudding + new_width,
] = same_ratio_image
cv2.imwrite("black_pudding_image.jpg", black_pudding_image)
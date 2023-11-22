import numpy as np
import matplotlib.pyplot as plt

# Replace this with your RGB pixel values array
# Example: a 4x4 image with random RGB values
# Here, each row contains RGB values for one pixel
# rgb_values = np.random.randint(0, 256, size=(2 * 6, 3))  # Replace this with your RGB values array

# print(rgb_values)

# # Reshape the array to get the image dimensions
# image_height, image_width = 2, 6
# rgb_image = rgb_values.reshape(image_height, image_width, 3)

# print()
# print(rgb_image)

# # Display the image using imshow
# plt.imshow(rgb_image)
# plt.title('RGB Image')
# plt.show()

import numpy as np

R = np.array([66, 75, 209, 166])
G = np.array([135,133, 227, 126])
B = np.array([245,57,43,148])

# Combine the arrays A and B
combined = np.vstack((R,G,B))

# print(combined)
# Reshape the combined array
result = combined.T
result = result.reshape(2,2,3)
print(result[0])
# plt.imshow(result)
# plt.show()



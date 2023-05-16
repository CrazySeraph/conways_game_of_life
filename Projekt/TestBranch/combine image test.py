from keras.datasets import mnist
import numpy as np
import matplotlib.pyplot as plt

# Load the MNIST dataset
(x_train, _), (_, _) = mnist.load_data()

# Select 9 random indices
random_indices = np.random.choice(len(x_train), size=9, replace=False)

# Create a grid to combine the images
grid_size = (3, 3)
combined_image = np.zeros((grid_size[0] * 28, grid_size[1] * 28))

# Fill the grid with the selected images
for i, idx in enumerate(random_indices):
    # Calculate the row and column indices in the grid
    row = i // grid_size[1]
    col = i % grid_size[1]

    # Get the image corresponding to the random index
    image = x_train[idx]

    # Compute the row and column indices in the combined image
    row_start = row * 28
    row_end = (row + 1) * 28
    col_start = col * 28
    col_end = (col + 1) * 28

    # Copy the image to the corresponding position in the combined image
    combined_image[row_start:row_end, col_start:col_end] = image

# Display the combined image
plt.imshow(combined_image, cmap='gray')
plt.axis('off')
plt.show()

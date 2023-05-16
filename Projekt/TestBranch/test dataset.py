from keras.datasets import mnist
import numpy as np
import matplotlib.pyplot as plt

# Load the MNIST dataset
(x_train, _), (_, _) = mnist.load_data()

# Select 10 random indices
random_indices = np.random.choice(len(x_train), size=10, replace=False)

# Display the selected images
fig, axes = plt.subplots(2, 5, figsize=(10, 4))

for i, ax in enumerate(axes.flatten()):
    # Get the image corresponding to the random index
    image = x_train[random_indices[i]]

    # Display the image
    ax.imshow(image, cmap='gray')
    ax.axis('off')

plt.tight_layout()
plt.show()

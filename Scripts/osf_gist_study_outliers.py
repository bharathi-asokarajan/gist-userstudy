'''
We calculate the centroid (center of mass) of the dataset using the mean of x-coordinates and y-coordinates.
For each outlier, we generate a random angle in radians and calculate the outlier's coordinates based on this angle and 
the specified outlier distance from the centroid. Outliers are added to the dataset at these calculated coordinates, ensuring a more even spread of 
outliers in random directions from the centroid.
'''


import matplotlib.pyplot as plt
import numpy as np
import os

# Create a folder on the desktop to save plots
folder_path = os.path.join(os.path.expanduser("~"), "Desktop", "gist_outliers_centroid_nocolor")
os.makedirs(folder_path, exist_ok=True)

np.random.seed(42)

# Numbers of points to iterate over
num_points_list = [100, 500, 1000]
distributions = ["normal"]


index = 1

for num_points in num_points_list:
    for distribution in distributions:
        for num_outliers in [1, 2, 3, 4]:
            for outlier_distance in [3.0, 4.0, 5.0]: 
                x_data = np.random.normal(0, 1, num_points)
                y_data = np.random.normal(0, 1, num_points)

                # Calculate centroid (center of mass) of the dataset
                centroid_x = np.mean(x_data)
                centroid_y = np.mean(y_data)

                # Add outliers
                outliers_x = []
                outliers_y = []
                for _ in range(num_outliers):
                    # Generate random angle in radians
                    angle = np.random.uniform(0, 2*np.pi)
                    # Calculate coordinates of outlier based on angle and distance
                    outlier_x = centroid_x + outlier_distance * np.cos(angle)
                    outlier_y = centroid_y + outlier_distance * np.sin(angle)
                    outliers_x.append(outlier_x)
                    outliers_y.append(outlier_y)

                # Combine existing data with outliers
                x_data = np.concatenate([x_data, outliers_x])
                y_data = np.concatenate([y_data, outliers_y])

                # Update is_outlier accordingly
                is_outlier = np.concatenate([np.zeros(len(x_data) - num_outliers), np.ones(num_outliers)])

                # Plot the data
                plt.figure(figsize=(4, 4), dpi=300)
                plt.scatter(x_data, y_data, s=3, color=np.where(is_outlier, 'black', 'k'), marker='o')
                plt.xlabel('x')
                plt.ylabel('y')  
                plt.gca().set_xticklabels([])
                plt.gca().set_yticklabels([])
                plt.gca().spines['top'].set_visible(False)
                plt.gca().spines['right'].set_visible(False)

                title = f'plot_{num_points}_dist_{distribution}_outl_{num_outliers}_dist_{outlier_distance}.png'
                # Save the plot to the folder
                save_path = os.path.join(folder_path, title)
                plt.savefig(save_path, dpi=300)

                # Clear the current plot for the next iteration
                plt.clf()
                plt.close()

print("Plots and CSV data saved to:", folder_path)

import matplotlib.pyplot as plt
import numpy as np
import os

# Create a folder on the desktop to save plots
folder_path = os.path.join(os.path.expanduser("~"), "Desktop", "cat4_gist_correlation_positive_jitter2")
os.makedirs(folder_path, exist_ok=True)

np.random.seed(42)

# Numbers of points to iterate over
num_points_list = [100, 500, 1000]
distributions = ["normal"]
correlation_values = [0.2,0.5,0.8]

index = 1

for num_points in num_points_list:
    for distribution in distributions:
        for r_value in correlation_values:
            x_data = np.random.normal(0, 1, num_points)
            y_data = np.random.normal(0, 1, num_points)

            if r_value == 1.0:
                # Generate y_data as linear transformation of x_data with reduced noise
                y_data = x_data + np.random.normal(0, 0, num_points)  # Reduced noise
                covariance_matrix = [[-1, 1], [1, -1]] #comment for positive
            else:
                unique_points = np.unique(np.vstack((x_data, y_data)).T, axis=0)
                data = unique_points.T
                
                #covariance_matrix = [[1, -r_value], [-r_value, 1]]
                covariance_matrix = [[1, r_value], [r_value, 1]] #Uncomment for positive correlation
                cholesky_matrix = np.linalg.cholesky(covariance_matrix)
                correlated_data = np.dot(cholesky_matrix, data)

                x_data = correlated_data[0]
                y_data = correlated_data[1]

            # Add jitter
            jitter_range = 0.5
            x_data += np.random.uniform(-jitter_range, jitter_range, size=num_points)
            y_data += np.random.uniform(-jitter_range, jitter_range, size=num_points)

            index += 1
            plt.figure(figsize=(4, 4), dpi=300)
            plt.scatter(x_data, y_data, s=3, color='k', marker='o')

            plt.xlabel('x')
            plt.ylabel('y')  
            plt.gca().set_xticklabels([])
            plt.gca().set_yticklabels([])
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)

            title = f'plot_{num_points}_rval_{r_value}_positive_jitter2.png'
            # Save the plot to the folder
            save_path = os.path.join(folder_path, title)
            plt.savefig(save_path, dpi=300)

            # Clear the current plot for the next iteration
            plt.clf()
            plt.close()

print("Plots and CSV data saved to:", folder_path)

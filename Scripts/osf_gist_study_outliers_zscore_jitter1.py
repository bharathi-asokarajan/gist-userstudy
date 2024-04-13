import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

# Create a folder on the desktop to save plots
folder_path = os.path.join(os.path.expanduser("~"), "Desktop", "gist_outliers_zscore_jitter2")
os.makedirs(folder_path, exist_ok=True)

np.random.seed(42)

# Numbers of points to iterate over
num_points_list = [100, 500, 1000]
num_outliers = [0, 1, 2, 3]  # Include scenario with 0 outliers
sd_away = [2, 3, 4]

# Jitter range
jitter_range = 0.5  # You can adjust this value as needed

for num_points in num_points_list:
    for num_out in num_outliers:
        if num_out == 0:
            # Generate data
            x = np.random.rand(num_points) * 10
            y = 2 * x + 1 + np.random.normal(loc=2, scale=1.5, size=num_points)  # Normal distribution

            # Add jitter
            x += np.random.uniform(-jitter_range, jitter_range, size=num_points)
            y += np.random.uniform(-jitter_range, jitter_range, size=num_points)

            # Recalculate z-score for each data point
            z_scores = np.abs(stats.zscore(y))

            # Plot the data
            plt.figure(figsize=(4, 4), dpi=300)
            plt.scatter(x, y, s=3, color='k', marker='o')
            plt.xlabel('x')
            plt.ylabel('y')  
            plt.gca().set_xticklabels([])
            plt.gca().set_yticklabels([])
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)

            # Save plot as PNG
            filename = f"plot_{num_points}_{num_out}_jitter2.png"
            filepath = os.path.join(folder_path, filename)
            plt.savefig(filepath)

            plt.close()
        else:
            for sd in sd_away:
                # Generate data
                x = np.random.rand(num_points) * 10
                y = 2 * x + 1 + np.random.normal(loc=2, scale=1.5, size=num_points)  # Normal distribution

                # Add outliers
                for _ in range(num_out):
                    outlier_index = np.random.randint(0, num_points)
                    outlier = np.random.normal(loc=2, scale=1.5, size=1) * sd * np.std(y)
                    y[outlier_index] += outlier[0]  # Extract a single element from the outlier array

                # Add jitter
                x += np.random.uniform(-jitter_range, jitter_range, size=num_points)
                y += np.random.uniform(-jitter_range, jitter_range, size=num_points)

                # Recalculate z-score for each data point
                z_scores = np.abs(stats.zscore(y))

                # Plot the data
                plt.figure(figsize=(4, 4), dpi=300)
                plt.scatter(x, y, s=3, color='k', marker='o')
                plt.xlabel('x')
                plt.ylabel('y')  
                plt.gca().set_xticklabels([])
                plt.gca().set_yticklabels([])
                plt.gca().spines['top'].set_visible(False)
                plt.gca().spines['right'].set_visible(False)

                # If there are outliers, mark them in red
                if num_out > 0:
                    outliers = np.where(z_scores > sd)[0]
                    plt.scatter(x[outliers], y[outliers], s=3, color='k', marker='o')

                # Save plot as PNG
                filename = f"plot_{num_points}_outliers_{num_out}_sd_{sd}_jitter2.png"
                filepath = os.path.join(folder_path, filename)
                plt.savefig(filepath)

                plt.close()

print("Plots saved in:", folder_path)

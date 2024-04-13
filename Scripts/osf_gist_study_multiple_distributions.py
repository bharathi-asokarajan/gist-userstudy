import matplotlib.pyplot as plt
import numpy as np
import os
import csv

# Create a folder on the desktop to save plots
folder_path = os.path.join(os.path.expanduser("~"), "Desktop", "gist_all6dist_3")
os.makedirs(folder_path, exist_ok=True)

# Create a CSV file for storing data
csv_file_path = os.path.join(folder_path, "combined_data.csv")
csv_columns = ["Index", "No. of Points", "Correlation Value", "Distribution", "Geometry/Topology"]

np.random.seed(42)

# Numbers of points to iterate over
num_points_list = [100, 500, 1000]
distributions = ["normal", "exponential", "uniform", "curvilinear", "striated", "stringy"]

index = 1

for num_points in num_points_list:

        for distribution in distributions:

                if distribution in ["normal", "exponential", "uniform"]:
                    # Generate correlated random data with the current distribution and r value
                    if distribution == "normal":
                        # Generate continuous data in the range [0, 1] using the inverse transform method
                        x_data = np.random.normal(0, 1, num_points)
                        y_data = np.random.normal(0, 1, num_points)
                    elif distribution == "exponential":
                        data = np.random.exponential(scale=0.5, size=(2, num_points))
                        x_data = data[0]
                        y_data = data[1]
                    
                    elif distribution == "uniform":
                        data = np.random.uniform(low=0.0001, high=0.9999, size=(2, num_points))
                        x_data = data[0]
                        y_data = data[1]

                elif distribution in ["curvilinear", "striated", "stringy"]:
                    # Generate data for different distributions and geometries
                    if distribution == "curvilinear":
                        x_data = np.linspace(0, 1, num_points)
                        y_data = -x_data**2 + np.random.normal(0, 0.07, size=num_points)
                        geometry_topology = "Curvilinear"


                    elif distribution == "stringy":
                        # Generate x values between 0 and 1
                        x_data = np.linspace(0, 1, num_points)

                        up_amplitudes = np.array([0.2, 0.6, 1.0, 0.4, 0.8])
                        down_amplitudes = np.array([0.5, 0.3, 0.8, 0.2, 0.6])

                        # Create sine waves for the y values with different amplitudes
                        y_data = np.zeros(num_points)

                        for i in range(len(up_amplitudes)):
                            # Modulate the amplitude for each set of up and down
                            y_data += np.sin(x_data * 4 * np.pi * (i + 1)) * up_amplitudes[i]
                            y_data += np.sin(x_data * 4 * np.pi * (i + 1) + np.pi) * down_amplitudes[i]


                        geometry_topology = "stringy"

                    elif distribution == "striated":
                        x_data = np.linspace(0, 1, num_points)
                        # Number of parallel lines
                        num_lines = 3

                        y_data = np.zeros((num_lines, num_points))
                        for i in range(num_lines):
                            line_deviation = np.random.normal(0, 0.1)  # Random deviation for each line
                            x_deviation = np.random.normal(0, 0.05, num_points)  # Random deviation for x-coordinates

                            y_data[i, :] = i * 0.2 + line_deviation  # Linear arrangement along y-axis
                            x_data += x_deviation  # Vary x-coordinates randomly


                        geometry_topology = "striated"

                else:
                    raise ValueError(f"Invalid distribution: {distribution}")
  
                index += 1
                plt.figure(figsize=(4, 4), dpi=300)
                
                if distribution == "striated": 
                    for i in range(num_lines):
                        plt.scatter(x_data, y_data[i, :], s=3, color='k', marker='o')
                else:
                     plt.scatter(x_data, y_data, s=3, color='k', marker='o')

                plt.xlabel('x')
                plt.ylabel('y')  
                plt.gca().set_xticklabels([])
                plt.gca().set_yticklabels([])
                plt.gca().spines['top'].set_visible(False)
                plt.gca().spines['right'].set_visible(False)


                title = f'plot_{num_points}_{distribution}.png'
                # Save the plot to the folder
                save_path = os.path.join(folder_path, title)
                plt.savefig(save_path, dpi=300)

                # Clear the current plot for the next iteration
                plt.clf()
                plt.close()

print("Plots and CSV data saved to:", folder_path)

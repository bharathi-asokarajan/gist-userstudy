import matplotlib.pyplot as plt
import numpy as np
import os
import csv

# Create a folder on the desktop to save plots
folder_path = os.path.join(os.path.expanduser("~"), "Desktop", "gist_correlationplots_outliers_distance4.0_nocolor")
os.makedirs(folder_path, exist_ok=True)

# Create a CSV file for storing data
csv_file_path = os.path.join(folder_path, "combined_data.csv")
csv_columns = ["Index", "No. of Points", "Correlation Value", "Distribution", "Geometry/Topology"]

with open(csv_file_path, mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
    writer.writeheader()

    # Set seed for reproducibility
    np.random.seed(42)

    # Numbers of points to iterate over
    #num_points_list = [100, 500, 1000]
    num_points_list = [100]
    

    # Correlation coefficient (r value) values
    correlation_values = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.99]

    #distributions = ["normal", "exponential", "uniform", "logarithmic", "skewed", "clumpy", "striated", "convex", "stringy"]
    distributions = ["normal"]

    index = 1

    for num_points in num_points_list:
        #for r_value in correlation_values:
            for distribution in distributions:
                for num_outliers in [1, 2, 3, 4]:
                    outlier_distance = 4.0
                    if distribution in ["normal", "exponential", "uniform"]:
                        # Generate correlated random data with the current distribution and r value
                        if distribution == "normal":
                            # Generate continuous data in the range [0, 1] using the inverse transform method
                            x_data = np.random.normal(0, 1, num_points)
                            y_data = np.random.normal(0, 1, num_points)


                        
                        elif distribution == "exponential":
                            data = np.random.exponential(scale=0.5, size=(2, num_points))
                        
                        elif distribution == "uniform":
                            data = np.random.uniform(low=0.0001, high=0.9999, size=(2, num_points))
                        '''
                        unique_points = set()
                        while len(unique_points) < num_points:
                            unique_points.update(tuple(map(tuple, np.vstack((x_data, y_data)).T)))


                        unique_points = np.unique(np.vstack((x_data, y_data)).T, axis=0)
                        data = unique_points.T
                        
                        covariance_matrix = [[1, r_value], [r_value, 1]]
                        cholesky_matrix = np.linalg.cholesky(covariance_matrix)
                        correlated_data = np.dot(cholesky_matrix, data)

                        # Extract x and y coordinates with 2 decimal points
                        x_data = correlated_data[0]
                        y_data = correlated_data[1]
                        '''
                        geometry_topology = "Correlation-Based"

                    #elif distribution in ["logarithmic", "skewed", "clumpy", "striated", "convex", "stringy"]:
                    elif distribution in ["curvilinear", "skewed", "clumpy", "striated", "convex", "stringy"]:
                        # Generate data for different distributions and geometries
                        if distribution == "curvilinear":
                            x_data = np.linspace(0, 1, num_points)
                            y_data = -x_data**2 + np.random.normal(0, 0.07, size=num_points)
                            geometry_topology = "Curvilinear"


                        elif distribution == "stringy":
                            # Generate x values between 0 and 1
                            x_data = np.linspace(0, 1, num_points)

                            
                            # Create a sine wave for the y values with increased amplitude
                            #amplitude = 0.6  # Adjust the amplitude to make the waves taller
                            #y_data = np.sin(x_data * 4 * np.pi) * amplitude  # Increase the frequency (multiplied by 4)
                            # Create an array of amplitudes for each set of up and down
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

                        elif distribution == "convex":
                            angle = np.linspace(0, 2 * np.pi, num_points)
                            radius = np.linspace(0.2, 1.0, num_points)
                            data = np.array([radius * np.cos(angle), radius * np.sin(angle)])
                            geometry_topology = "Convex"

                        

                    else:
                        raise ValueError(f"Invalid distribution: {distribution}")
                    
                    # Add outliers
                    x_outliers = np.random.normal(0, 1, num_outliers)
                    y_outliers = np.random.normal(0, 1, num_outliers)

                    # Calculate mean of existing data
                    mean_x = np.mean(x_data)
                    mean_y = np.mean(y_data)

                    # Add outliers at a specified distance from the mean
                    x_outliers += mean_x + np.sign(x_outliers) * outlier_distance
                    y_outliers += mean_y + np.sign(y_outliers) * outlier_distance

                    # Combine existing data with outliers
                    x_data = np.concatenate([x_data, x_outliers])
                    y_data = np.concatenate([y_data, y_outliers])

                    # Identify outliers for coloring
                    is_outlier = np.concatenate([np.zeros(len(x_data) - num_outliers), np.ones(num_outliers)])


                    # Save data to CSV
                    writer.writerow({
                        "Index": index,
                        "No. of Points": num_points,
                        #"Correlation Value": r_value,
                        "Distribution": distribution,
                        "Geometry/Topology": geometry_topology,
                    })

                    index += 1
                    plt.figure(figsize=(4, 4), dpi=300)
                    # Scatterplot with round dots
                    plt.scatter(x_data, y_data, s=3, color='k', marker='o')
                    plt.scatter(x_data, y_data, s=3, color=np.where(is_outlier, 'black', 'k'), marker='o')
                    #plt.scatter(data[0], data[1], s=3, color='k', marker='o')
                    #for i in range(num_lines):
                        #plt.scatter(x_data, y_data[i, :], s=3, color='k', marker='o')

                    # Set the x-axis and y-axis limits between 0 and 1
                    #plt.xlim(-0.9, 1.1)
                    #plt.ylim(-0.9, 1.1)
                    plt.axis('off')
                    plt.xticks([])
                    plt.yticks([])

                    plt.gca().set_aspect('equal', adjustable='box')

                    # Set the title
                    title = f'plot_{num_points}_{distribution}_{num_outliers}.png'
                    #title = f'plot_{num_points}_{distribution}.png'
                    #plt.title(title)

                    # Save the plot to the folder
                    save_path = os.path.join(folder_path, title)
                    plt.savefig(save_path, dpi=300)

                    # Clear the current plot for the next iteration
                    plt.clf()
                    plt.close()

print("Plots and CSV data saved to:", folder_path)

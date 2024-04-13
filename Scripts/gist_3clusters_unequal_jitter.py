import numpy as np
import matplotlib.pyplot as plt
import os

# Create a folder on the desktop to save plots
folder_path = os.path.join(os.path.expanduser("~"), "Desktop", "gist_clusters_unequal_points_jitter2")
os.makedirs(folder_path, exist_ok=True)
np.random.seed(42)

def generate_clusters_specific(num_clusters, cluster_means, cluster_covariances, num_points_per_cluster):
    data = []
    for i in range(num_clusters):
        # Generate points for the current cluster
        cluster_points = np.random.multivariate_normal(cluster_means[i], cluster_covariances[i], num_points_per_cluster[i])
        
        # Append points to the data list
        data.append(cluster_points)
    
    # Concatenate points from all clusters
    return np.concatenate(data)

# Number of clusters
num_clusters = 3

# Means for each cluster separated by a distance of 3 units
cluster_means = [[2, 7], [5, 2], [8, 6]]
#distance = 4
#cluster_means = [[2, 7], [6, 2], [10, 6]]
#distance = 5
#cluster_means =[[2, 7], [7, 2], [12, 6]]

# Covariance matrices for each cluster
covariance_cluster1 = [[1, 0.1], [0.1, 1]]
covariance_cluster2 = [[1, 0.1], [0.1, 1]]
covariance_cluster3 = [[1, 0.1], [0.1, 1]]
cluster_covariances = [covariance_cluster1, covariance_cluster2, covariance_cluster3]

# Number of points per cluster - 60%, 25% and 15%
num_points_per_cluster_list = [[60, 25, 15], [300, 125, 75], [600, 250, 150]]

# Jitter range
jitter_range = 0.5

# Generate and plot clusters for each combination
for num_points_per_cluster in num_points_per_cluster_list:
    # Generate clusters
    data = generate_clusters_specific(num_clusters, cluster_means, cluster_covariances, num_points_per_cluster)

    # Add jitter for each cluster
    jittered_data = np.copy(data)
    start_index = 0
    for i, num_points in enumerate(num_points_per_cluster):
        end_index = start_index + num_points
        jittered_data[start_index:end_index, 0] += np.random.uniform(-jitter_range, jitter_range, size=num_points)
        jittered_data[start_index:end_index, 1] += np.random.uniform(-jitter_range, jitter_range, size=num_points)
        start_index = end_index

    # Create a scatter plot
    plt.figure(figsize=(4, 4), dpi=300)
    plt.scatter(jittered_data[:, 0], jittered_data[:, 1], s=3, color='k', marker='o')
    plt.xlabel('x')
    plt.ylabel('y')  
    plt.gca().set_xticklabels([])
    plt.gca().set_yticklabels([])
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    title = f'plot_{sum(num_points_per_cluster)}_{num_clusters}_clusters_dist_3_jitter2.png'
    # Save the plot to the folder
    save_path = os.path.join(folder_path, title)
    plt.savefig(save_path, dpi=300)

    # Clear the current plot for the next iteration
    plt.clf()
    plt.close()

print("Plots and CSV data saved to:", folder_path)

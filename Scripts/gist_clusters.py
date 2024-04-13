import numpy as np
import matplotlib.pyplot as plt

# Set a seed for reproducibility
np.random.seed(42)

# Number of data points
num_points = 100
num_points = 100

# Adjust the means to increase the separation
mean_cluster1 = [2, 3]
mean_cluster2 = [8, 10]
mean_cluster3 = [5, 12]

# Covariance matrices remain the same
covariance_cluster1 = [[1, 0.7], [0.7, 1]]
covariance_cluster2 = [[1, -0.5], [-0.5, 1]]
covariance_cluster3 = [[1, -0.2], [-0.2, 1]]

# Generate points for two clusters
cluster1_points = np.random.multivariate_normal(mean_cluster1, covariance_cluster1, int(num_points/2))
cluster2_points = np.random.multivariate_normal(mean_cluster2, covariance_cluster2, int(num_points/2))
cluster3_points = np.random.multivariate_normal(mean_cluster3, covariance_cluster3, int(num_points/2))


# Concatenate the points
data = np.concatenate([cluster1_points, cluster2_points,cluster3_points])

# Create a scatter plot
#plt.scatter(data[:, 0], data[:, 1], s=3, color='k', marker='o')
colors = ['r', 'g', 'b']
plt.scatter(data[:, 0], data[:, 1], s=3, c=np.concatenate([[colors[i]] * len(cluster) for i, cluster in enumerate([cluster1_points, cluster2_points, cluster3_points])]), marker='o')

plt.axis('off')
plt.xticks([])
plt.yticks([])
#plt.title('Scatter Plot with Normal Distribution (Mean=0, Std_dev=1) and 2 Clusters')
#plt.xlabel('X-axis')
#plt.ylabel('Y-axis')
plt.show()

# --------------------------Load Library-------------------------------------
import numpy as np
from acf_and_pacf import plot_acf
import os
import sys

# Get the absolute path to the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add parent directory to Python's path
sys.path.append(parent_dir) 
from random_walk.random_walk import visualize_random_walk

# --------------------------Load Library-------------------------------------


# Set parameters for the AR(2) model
c_0 = 0.001
c_1 = -0.1
c_2 = 0.4
sigma = 1
Nt = 1000

# Initialize the time series and the white noise
r = np.zeros(Nt)
z = np.random.normal(0, sigma, Nt)

# Generate the AR(2) time series data
for t in range(2, Nt):
    r[t] = c_0 + c_1 * r[t-1] + c_2 * r[t-2] + z[t]

# Calculate the cumulative sum to represent the path
r_cumulative = np.cumsum(r)


# -----------------------Visualization-----------------------------

# Plot 1: the AR(2) path
# Call the visualization function with the cumulative data
_ = visualize_random_walk(r_cumulative, 
                          title="AR(2) Sample Path", xlabel="Time", ylabel="Cumulative r", 
                          colors='k',
                        #   save_filename="ar2_sample_path.png")
                          save_options=False)



# Plot 2: AR(2) sample ACF
plot_acf(r, title="AR(2) Sample Autocorrelation Function", partial=False)
# Plot 3: AR(2) sample PACF
plot_acf(r, title="AR(2) Sample Partial Autocorrelation Function", partial=True)






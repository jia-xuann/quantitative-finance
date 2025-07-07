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

# --- Model Parameters ---
mu = 0.0
sigma = 1.0
phi_1 = -0.1  # Coefficient for the first lag of the error term
phi_2 = 0.4   # Coefficient for the second lag of the error term
Nt = 1000     # Number of time steps


# --- Simulation ---

# Generate the white noise series (the error terms)
# Z values are scaled standard normal values mu + z_std * sigma
z = np.random.normal(loc=mu, scale=sigma, size=Nt)

# Initialize the return series
r = np.zeros(Nt)

# Generate the MA(2) return series recursively
r[0] = z[0]
r[1] = z[1] + phi_1 * z[0]
for t in range(2, Nt):
    r[t] = z[t] + phi_1 * z[t-1] + phi_2 * z[t-2]

# --- Visualization ---

# 1. Plot the MA(2) Sample Path
r_cumulative = np.cumsum(r)
visualize_random_walk(r_cumulative, 
                      title="MA(2) Sample Path", 
                      xlabel="Time", 
                      ylabel="Cumulative r", 
                      colors='navy',
                      save_options=False)   

# 2. Plot the Sample ACF
plot_acf(r, title="MA(2) Sample Autocorrelation Function", partial=False)
# 3. Plot the Sample PACF
plot_acf(r, title="MA(2) Sample Partial Autocorrelation Function", partial=True)    



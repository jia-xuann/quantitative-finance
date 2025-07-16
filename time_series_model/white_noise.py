# --------------------------Load Library-------------------------------------
from acf_and_pacf import plot_acf
import os
import sys

# Get the absolute path to the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add parent directory to Python's path
sys.path.append(parent_dir) 
from lognormal_price_process.lognormal_price import normal_return


# --------------------------Load Library-------------------------------------

# Set parameters 
sigma = 0.3       # Set annualized volotility to 30%
mu = 0.1          # Set annual drift/return to 10%
nt = 252          # Number of time steps
dt = 1/nt         # Set time step scale factor to one day

# Generate a sample of white noise returns
r = normal_return(nt, dt, mu, sigma)

# Plot 1: White Noise sample ACF
_ = plot_acf(r, title="White Noise Sample Autocorrelation Function", partial=False)

# Plot 2: White Noise sample PACF
_ = plot_acf(r, title="White Noise Sample Partial Autocorrelation Function", partial=True)  


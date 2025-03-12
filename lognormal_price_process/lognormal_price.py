import numpy as np



def normal_return(nt, dt, mu, sigma):
    # Generate a set of standard normal random draws
    # np.random.seed(seed) # For reproducibility
    z = np.random.normal(0, 1, nt)

    # Draw daily return from scaled N(mu, sigma^2)
    r = mu * dt + z * sigma * np.sqrt(dt)
    
    return r
def log_price_dynamics(nt, dt, mu, sigma, N, P0=1):

    '''
    Parameters:
    -----------
    nt: number of time steps
    dt: time step size
    mu: annual drift/return
    sigma: annualized volatility
    P0: initial price(s) for the asset(s) - float or array-like, defaults to 1
    N = number of assets 

    '''
    i = 0
    paths = np.zeros((N, nt+1)) # set nt+1 to include the inital position

    for i in range(N):
        j = 0
        position = 0 
        paths[0,i] = position 
        x = normal_return(nt, dt, mu, sigma) # generate random steps for this walk

        while j < nt:
            position = position + x[j] # new loacation equals previous plus a random step
            paths[i, j+1] = position
            j += 1
    
    P0_array = np.array(P0)

    # reshape only if it's not already a column vector
    if P0_array.ndim == 1:
        P0_array = P0_array.reshape(-1,1)

    P = P0_array * np.exp(paths)
    return P 


if __name__ == '__main__':
    
    # Set parameters for sampling interval
    sigma = 0.3       # Set annualized volotility to 30%
    mu = 0.1          # Set annual drift/return to 10%
    nt = 252          # Number of time steps
    dt = 1/nt         # Set time step scale factor to one day
    N = 8             # Number of assets
    paths = log_price_dynamics(nt, dt, mu, sigma, N)
    
    # Visualize the lognormal price process
    import os
    import sys
    
    # Get the absolute path to the parent directory
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Add parent directory to Python's path
    sys.path.append(parent_dir) 

    from random_walk.random_walk import visualize_random_walk as visualize
    visualize(paths, ylabel='Price', 
              title='Sample Paths for a Lognormal Process', 
              save_filename='lognormal_price_plot.png')
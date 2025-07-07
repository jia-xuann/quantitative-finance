import numpy as np
import matplotlib.pyplot as plt

'''
Parameters:
-----------
p:  probability of go upward
nt: number of time steps
dt: time step size
N = number of random walks generated

'''

def random_walk(p,nt):

    # generate a set of uniform random draws
    z = np.random.uniform(size=nt*N) # z \in [0,1]

    # transform to binomial random variable +/- 1
    x = 2 * (z < p) - 1 # 50% chance that a unifrom random variable will be less than 0.5

    return x

def random_walk_2d(p,nt, N):

    i = 0
    paths = np.zeros((N, nt+1)) # set nt+1 to include the inital position

    for i in range(N):
        j = 0
        position = 0
        paths[0,i] = position
        x = random_walk(p, nt) # generate random steps for this walk

        while j < nt:
            position = position + x[j] # new loacation equals previous plus a random step
            paths[i, j+1] = position
            j += 1
    return paths


def visualize_random_walk(paths, xlabel='Time Step', ylabel='Distance', 
                         title='Sample Paths for a Random Walk Process',
                         colors=None,
                         save_filename='random_walk_plot.png', save_options=True):
    
    # If the input is a 1D array, reshape it to a 2D array with one row
    if paths.ndim == 1:
        paths = paths.reshape(1, -1)
    
    # Determine the colors for the plots
    if colors is None: 
        # If no colors are provided, use a colormap
        cmap = plt.cm.plasma
        plot_colors = cmap(np.linspace(0, 1, paths.shape[0]))
    elif isinstance(colors, str):
        # If a single color string is provided, use it for all paths
        plot_colors = [colors] * paths.shape[0]
    else:
        # If a list of colors is provided, use it
        plot_colors = colors

    # Plot each path
    for i, path in enumerate(paths):
        time_steps = np.arange(len(path))
        plt.plot(time_steps, path, color=plot_colors[i])
        
    # # add a horizontal line at y=0 for reference
    # plt.axhline(y=0, color='k', linestyle='--')
    
    # set the left boundary of x-axis to 0
    plt.xlim(left=0)
    
    # add labels and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, alpha=0.3)
    
    if save_options:
        plt.savefig(save_filename)
    plt.show()
    
    


if __name__ == '__main__':
    # set the parameters
    p = 0.5       
    nt = 252      
    N = 8        

    paths = random_walk_2d(p, nt, N)
    
    # --- Test Cases ---
    # 1. Default behavior (using colormap)
    # visualize_random_walk(paths)

    # 2. Custom color list for multiple paths
    custom_colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#A133FF', '#33FFA1', '#FFC300', '#C70039']
    # visualize_random_walk(paths, title="Custom Color List Visualization", colors=custom_colors, save_options=False)

    # 3. Single path with a single custom color
    single_path = paths[0]
    visualize_random_walk(single_path, colors='purple', save_options=False)

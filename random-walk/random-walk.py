import numpy as np
import matplotlib.pyplot as plt


p = 0.5
nt = 252 # number of trading days in a year
N = 8 # number of time steps

def random_walk(p,nt):

    # generate a set of uniform random draws
    z = np.random.uniform(size=nt*N) # z \in [0,1]

    # transform to binomial random variable +/- 1
    x = 2 * (z < p) - 1 # 50% chance that a unifrom random variable will be less than 0.5

    return x

def random_walk_2d(p,nt, N):

    i = 0
    # path = np.array([0])
    paths = np.zeros((N, nt+1)) # set nt+1 to include the inital position

    for i in range(N):
        j=0
        position = 0
        paths[0,i] = position
        x = random_walk(p, nt) # generate random steps for this walk

        while j < nt:
            position = position + x[j] # new loacation equals previous plus a random step
            paths[i, j+1] = position
            # path = np.append(path, position)
            j += 1
    return paths


def visualize_random_walk(paths):
    cmap = plt.cm.plasma # color palette: viridis, plasma, cool, tab10, Set2
    colors = cmap(np.linspace(0, 1, paths.shape[0]))

    for i, path in enumerate(paths):
        time_steps = np.arange(len(path))
        plt.plot(time_steps, paths[i], color=colors[i])

    # add a horizontal line at y=0 for reference
    plt.axhline(y=0, color='k', linestyle='--')
    # set the left boundary of x-axis to 0
    plt.xlim(left=0)
    
    # add labels and title
    plt.xlabel('Time Step')
    plt.ylabel('Distance')
    plt.title('Sample Paths for a Random Walk Process')
    plt.grid(True, alpha=0.3)
    
    plt.savefig('random_walk_plot.png')
    plt.show()
    
    


if __name__ == '__main__':
    paths = random_walk_2d(p, nt, N)
    visualize_random_walk(paths)
    

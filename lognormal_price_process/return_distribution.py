
import numpy as np
from lognormal_price import log_price_dynamics 
import matplotlib.pyplot as plt
from scipy import stats


def plot_normal_distribution(returns, title, bins=50, color='tab:blue', edgecolor='black'):
    """
    Plots a histogram of sample values along with a fitted normal distribution curve.
    """

    # Plot the histogram
    plt.hist(returns, bins=bins, edgecolor=edgecolor, color=color, density=True)
    
    # Generate the density curve
    x = np.linspace(min(returns), max(returns), 1000)
    mu_value = np.mean(returns)
    std_value = np.std(returns)
    pdf = stats.norm.pdf(x, loc=mu_value, scale=std_value)
    
    # Add the density curve to the plot
    label_text = rf'$\mu$={mu_value:.4f}, $\sigma$={std_value:.4f}'
    plt.plot(x, pdf, 'r', label=label_text)
    
    # Add legend and title
    plt.legend()
    plt.title(title)
    
    plt.savefig('distribution_plot.png')
    print('\nPlot Saved.')
    plt.show()

if __name__ == '__main__':
    # Set parameters for sampling interval
    sigma = 0.3       # Set annualized volotility to 30%
    mu = 0.1          # Set annual drift/return to 10%
    nt = 252          # Number of time steps
    dt = 1/nt         # Set time step scale factor to one day
    N = 10**4         # Number of paths
    
    # Generate N sample paths
    P = log_price_dynamics(nt, dt, mu, sigma, N)

    # Calculate returns
    returns = P[:,-1]/P[:,0] - 1

    #  Calculate empirical statistics
    empirical_mean = np.mean(returns)
    empirical_var = np.std(returns)
    # Calculate theoretical statistics
    theoretical_mean = np.exp(mu + sigma**2/2) - 1
    theretical_var = np.exp(2*mu + sigma**2) * (np.exp(sigma**2) - 1)

    print(f'Empirical mean: {empirical_mean:.4f}\n'
        f'Theoretical mean: {theoretical_mean:.4f}\n'
        f'Empirical std: {empirical_var:.4f}\n'
        f'Theretical std: {np.sqrt(theretical_var):.4f}')

    # Plot the histogram
        # returns+1: the price ratios follow a lognormal distribution, but returns do not.
    price_ratios = np.log(returns+1)

    title = 'Distribution of 1-year log returns'
    plot_normal_distribution(price_ratios, title)
    
  
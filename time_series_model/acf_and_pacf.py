import numpy as np
import matplotlib.pyplot as plt

def calculate_autocovariance(x, nlags):
    """
    Assesses the relationship of a time series with its own past values.
    """
    n = len(x)
    autocov = np.zeros(nlags + 1)
    # range(nlags + 1): from 0 to nlags inclusive
    for k in range(nlags + 1):
        autocov[k] = np.sum(x[:n-k] * x[k:]) / n
    return autocov


def calculate_acf(x, nlags):
    """
    ACF, autocorrelation function
    helpful to determine the order of AR model 
    """

    mu = np.mean(x)
    x_centered = x - mu
    autocovariance = calculate_autocovariance(x_centered, nlags)
    autocorrelation = autocovariance / autocovariance[0]
    return autocorrelation

def calculate_pacf(x, nlags):
    """
    PCAF, partial autocorrelation function
    helpful to determine the order of AR model
    Using the Durbin-Levinson algorithm, a recursive method to compute the PACF.
    """
    acf_values = calculate_acf(x, nlags + 1)
    pacf = np.zeros(nlags + 1)
    pacf[0] = 1.0
    phi = np.zeros((nlags, nlags))

    if nlags > 0:
        # For lag 1, PACF is equal to ACF
        # This is because there are no shorter lags to consider
        pacf[1] = acf_values[1]
        phi[0, 0] = pacf[1]

    # For lags 2 to nlags
    for k in range(2, nlags + 1):
        # The slice acf_values[1:k] gives [acf(1), acf(2), ..., acf(k-1)]
        # We reverse it to get [acf(k-1), ..., acf(1)] for the formula
        reversed_acf = acf_values[1:k][::-1]
        # Calculate the portion of the correlation that is not explained by shorter lags
        numerator = acf_values[k] - np.dot(phi[k-2, :k-1], reversed_acf)
        # Normalization factor
        denominator = 1 - np.dot(phi[k-2, :k-1], acf_values[1:k])
        
        if denominator == 0:
            pacf[k] = 0
        else:
            pacf[k] = numerator / denominator
        
        phi[k-1, k-1] = pacf[k]
        for j in range(k-1):
            phi[k-1, j] = phi[k-2, j] - pacf[k] * phi[k-2, k-2-j]
            
    return pacf

def plot_acf(data, title, nlags=30, partial=False):
    """
    Plots ACF or PACF with confidence intervals.
    """
    # --- Input Validation ---
    data = np.asarray(data)  # Ensure data is a numpy array
    if data.ndim > 2 or (data.ndim == 2 and 1 not in data.shape):
        raise ValueError("Input 'x' must be a 1D array or a 2D array with one column or row.")
    
    if data.ndim == 2:
        data = data.flatten()  # Convert row/column vector to 1D array
    # --- End Validation ---

    x_axis = np.arange(0, nlags + 1)
    if partial:
        rho = calculate_pacf(data, nlags=nlags)
        ylabel = "Partial ACF"
    else:
        rho = calculate_acf(data, nlags=nlags)
        ylabel = "ACF"      

    fig, ax = plt.subplots()
    
    
    # Create the stem plot
    # Stem plot is designed for discrete data, where each point is represented as a vertical line
    ax.stem(x_axis, rho,
            linefmt='k-',
            markerfmt=' ',  # No marker
            basefmt='k-')   # Base line at y=0
    
    ax.set_title(title)
    ax.set_xlabel("Lag")
    ax.set_ylabel(ylabel)
    

    # Add confidence interval lines
    # The confidence interval help us to identify whether the correlation is statistically significant
    # Under assumption: the central limit theorem
    # The critical value for two tailed test: 1.65, 1.96, 2.58 at 10%, 5%, and 1% significance level respectively
    # when a bar is within the confidence interval, we assume the true correlation is zero
    conf_interval = 1.96 / np.sqrt(len(data))
    ax.axhline(y=conf_interval, color='k', linestyle='--')
    ax.axhline(y=-conf_interval, color='k', linestyle='--')

    ax.set_xlim(left=0, right=nlags)  
    # Adjust the y-axis limits
    max_val = np.max([np.max(rho[1:]), conf_interval])  # Exclude the zero lag
    ax.set_ylim(top=1.1 * max_val)


    plt.show()

if __name__ == '__main__':
    from statsmodels.tsa.stattools import acf, pacf 
    # --- Test Example for calculate_pacf ---

    # 1. Create a simple, known time series
    test_series = np.array([1, 2, 10, 4, 5, 7])
    nlags = 3

    # 2. Use our custom calculate_pacf function
    custom_acf_result = calculate_acf(test_series, nlags=nlags)
    custom_pacf_result = calculate_pacf(test_series, nlags=nlags)

    # 3. Use statsmodels' acf and pacf function for verification
    statsmodels_acf_result = acf(test_series, nlags=nlags)
    # Note: statsmodels pacf by default uses ols method. 
    # The Durbin-Levinson method is equivalent to the 'ywm' (Yule-Walker modified) method.
    statsmodels_pacf_result = pacf(test_series, nlags=nlags, method='ywm')

    # 4. Print the results for comparison
    
    print(f"Test Series: {test_series}")
    print(f"Lags: {nlags}\n")
    print("--- ACF Test Results ---")
    print("Custom Function Output:")
    print(custom_acf_result)
    print("\nStatsmodels Output (for verification):")
    print(statsmodels_acf_result)

    print("\n--- PACF Test Results ---")
    print("Custom Function Output:")
    print(custom_pacf_result)
    print("\nStatsmodels Output (for verification):")
    print(statsmodels_pacf_result)

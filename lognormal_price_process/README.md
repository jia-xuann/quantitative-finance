
# Application: Asset price dynamics

The script is based on the MITX course: [15.455x Mathematical Methods of Quantitative Finance](https://www.edx.org/learn/finance/massachusetts-institute-of-technology-mathematical-methods-for-quantitative-finance)

I've converted the original R script to Python and made the following improvement to the lognormal price process simulation:

- **Improved Reusability**: Packaged code into functions for better modularity and reuse.
- **Adjustable Initial Price**: In the original implementation, the initial lognormal price default to 0, which means $P_0=1$. However, different stocks, currencies and financial instruments have different price points. I've modified the code from `P <- exp(s)` to `P = P0 * np.exp(s)` to make $P_0$ adjustable, allowing for more realistic simulations of various assets.

## Simulate lognormal prices
Generally, we model asset prices as lognormal distribution. Therefore, their log returns are drawn from a normal distribution.
$$r_t = log(P_t/P_{t-1})\sim N(\mu, \sigma^2)$$

since 
$$P_T = P_0 e^{rT}=P_o\exp (r_1+..+r_T)$$
the sum of log returns is also Gaussian. And the mean and variance grows linearly with T.
$$r(T)=r_1+..+r_T\sim N(T\mu, T\sigma^2)$$


## Lognormal distribution of returns
$$R = P_{t+1}/P_0 - 1$$

$$E[R]=E[e^{r(T)}-1]=e^{\mu+\sigma^2/2}-1$$
$$Var(R)=e^{2\mu+\sigma^2}(e^{\sigma^2}-1)$$
Since prices follow a lognormal distribution, the price ratios are Gaussian.
$$log(R+1)\sim N(\mu, \sigma^2)$$

### Challenges:
The empirical mean and variance of returns do not match the theoretical ones.

- [x] I checked the function `normal_return()`, which generates `nt` normal sample returns. 

The theoretical mean and variance of the returns are given by:
$$E[r] = \mu \cdot dt$$  
$$Var(r) = \sigma^2 \cdot dt$$

- [x] I checked whether I mistakenly defined the formula for the returns. (That's it.)

    - **Original Definition:**  $R = \log\left(P_{t+1}/P_t\right) - 1$
    - **Revised Definition:**  $R = P_{t+1}/P_0 - 1$


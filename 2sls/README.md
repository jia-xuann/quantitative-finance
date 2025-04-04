## Two-Stage Least Squares (2SLS)

The MATLAB script is based on the textbook Econometrics (Bruce E. Hansen). It raises Acemoglu, Johnson and Robinson's (2001) paper as an example to illustrate instrumental variable (IV) regression. They research on the effect of political institutions on economic performance. 

Conclusion: Good institutions, for example, rule of law, should result in a country having higher long-term economic output.

IV regression is applied when there is an endogeneity.


### Definition for Endogeneity

There's a linear model $Y=X^{'}\beta +e$.

If $\mathbb{E}[Xe]\neq 0$
, then $X$ is endogenous for $\beta$.

If the regressors are endogenous, the estimator will be biased and inconsistent for the structural coefficient $\beta$. 

The standard approach to handling endogeneity is to specify instrumental variable $Z_i$ which are both relevant (correlated with $X_i$) yet exogenous(uncorrelated with $\epsilon _i$).


### Build Models
Their reported OLS estimates (intercept omitted) are (``mdl1``)

$$\log(\widehat{GDP\ per\ Capita})=\underset{(0.06)}{0.52}\ risk$$

The author argues that the risk is endogenous since economic output influences political institutions
and because the variable risk is undoubtedly measured with error. 

When mortality is unrelated to economic performance yet associated with political institutions. The authors think that colonies with high expected mortality will have less European migrants, who typically introduced systems that protected property ownership, promote democratic governance, and supported economic growth.

Therefore, they uses ``log(mortality)`` as an instrument for ``risk``.


the first-stage regression is (``mdl2``)

$$\widehat{risk}=\underset{(0.13)}{-0.61}\  \log(mortality)+\hat{\mu}$$
the second-stage regression is (``mdl3``)

$$\log(\widehat{GDP\ per\ Capita})=0.94\ \hat{risk}$$

### Endogeneity Test (Hausman test)
Structural equation: log(GDP per Capita) = $\beta_1 risk +\mu$

H0: the variable `risk` is exogenous for the structural equations.
First stage: $risk = \alpha_0 + \alpha_2\ instrument + \mu$
We take the least squares residuals $\hat \mu$ from the first stage equation, and include them in the structural equation:

$$loggdp = \beta_1 risk+\beta_2\hat \mu+v$$
Reasoning: Since $\hat \mu$ captures unexplained portion of `risk`, when we run the regression, $\beta_2$ can captures any additional relationship between `loggdp` and the unexplained part. If risk is truly exogenous, $\beta_2$ should equal zero.

The estimates (`mdl_test`) are:

$$loggdp = 0.93\ risk-0.57\hat \mu$$

We found a coefficient on $\hat \mu$ of -0.57 with a t-ratio of -4.7, which is highly significant. We reject the null hypothesis, confirming that `risk` is indeed endogenous.

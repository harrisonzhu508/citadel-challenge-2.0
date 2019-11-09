import GPy
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
cmap = viridis = cm.get_cmap('viridis', 100)


def fit_poisson_GP(X, y, kernel = GPy.kern.RBF(3), optimize=True, plot=True, optimizer='scg'):
    """

    """
    # X = np.linspace(0, 10, x_len)[:, None]
    # Y = np.array([np.random.poisson(np.exp(f)) for f in f_true])[:,None]

    # kern = GPy.kern.RBF(1) 
    poisson_lik = GPy.likelihoods.Poisson()
    laplace_inf = GPy.inference.latent_function_inference.Laplace()

    # create simple GP Model
    m = GPy.core.GP(X, y, kernel=kernel, likelihood=poisson_lik, inference_method=laplace_inf)

    if optimize:
        m.optimize(optimizer)
    if plot:
        m.plot()

    return m
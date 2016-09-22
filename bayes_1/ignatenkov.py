import numpy as np
from scipy.stats import binom, poisson


def expect(prob, support):
    return prob.dot(support.T)


def pa(params, model=2):
    """
    Probability distribution for b
    :param params: dict with params
    :param model: 1 for model with binomial distributon for p(c|a,b),
    2 for Poisson distribution
    :return: p, b
    """
    size = params['amax'] - params['amin'] + 1
    return np.arange(params['amin'], params['amax'] + 1), np.ones(size)*1./size


def pb(params, model=2):
    size = params['bmax'] - params['bmin'] + 1
    return np.arange(params['bmin'], params['bmax'] + 1), np.ones(
        size) * 1. / size


def pd_c(c, params, model=2):
    bin_dist = binom(c, params['p3'])
    support = np.arange(c, 2*c + 1)
    return np.array([bin_dist.pmf(x) for x in np.arange(c + 1)]), support


def pc_ab(a, b, params, model=2):
    dist = poisson(a*params['p1'] + b*params['p2'])
    support = np.arange(a + b + 1)
    return np.array(dist.pmf(x) for x in support), support

import numpy as np
from scipy.stats import binom, poisson
from scipy.misc import factorial


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
    return bin_dist.pmf(support), support


def pc_ab(a, b, params, model=2):
    lmbd = a*params['p1'] + b*params['p2']
    dist = poisson(lmbd)
    support = np.arange(params['amax'] + params['bmax'] + 1)
    return dist.pmf(support), support


def pb_a(a, params, model=2):
    return pb(params, model)


def pc(params, model=2):
    p1 = params['p1']
    p2 = params['p2']
    amin = params['amin']
    amax = params['amax']
    bmin = params['bmin']
    bmax = params['bmax']
    support = np.arange(params['amax'] + params['bmax'] + 1)
    lmbds = np.array([a*p1 + b*p2 for a in np.arange(amin, amax + 1) for b in np.arange(bmin, bmax + 1)])
    all_dists = poisson(lmbds).pmf(np.matrix(support).T)
    weights = np.ones((amax-amin+1)*(bmax-bmin+1))/(amax-amin+1)/(bmax-bmin+1)
    final_dist = all_dists.dot(np.matrix(weights).T).A1
    return final_dist, support

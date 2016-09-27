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
    return bin_dist.pmf(support - c), support


def pc_ab(a, b, params, model=2):
    lmbd = a*params['p1'] + b*params['p2']
    dist = poisson(lmbd)
    size = params['amax'] + params['bmax'] + 1
    support = np.arange(size)
    if isinstance(a, np.ndarray):
        return dist.pmf(support.reshape(size, 1)), support
    else:
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


def pd(params, model=2):
    p3 = params['p3']
    c_dist, c_support = pc(params, model)
    d_support = np.arange(c_support.size*2-1)
    all_support = np.subtract(d_support.reshape(d_support.size, 1)*np.ones(c_dist.size), np.arange(c_dist.size))
    all_dists = binom(np.arange(c_dist.size), p3).pmf(all_support)
    final_dist = all_dists.dot(np.matrix(c_dist).T).A1
    return final_dist, d_support


def pb_d(d, params, model=2):
    # p(b|d) = p(b,d)/p(d) = p(a)p(b)\sum_c p(d|c)\sum_a p(c|a,b)/p(d)
    d_dist, d_support = pd(params, model)

    def p_d_c(d, c, params):
        dist, support = pd_c(c, params)
        return dist[np.where(support == d)[0][0]]
    p_d_c_vect = np.array([p_d_c(d, c, params) for c in np.arange((d+1)/2, d+1)])
    result = []
    # calculate for every b
    for b in np.arange(params['bmin'], params['bmax']+1):
        pc_ab_sum_a = np.sum(pc_ab(np.arange(params['amin'], params['amax']+1), b, params)[0], axis=1)
        result.append(pc_ab_sum_a[(d+1)/2:(d+1)].dot(p_d_c_vect))
    return np.array(result)/sum(result), np.arange(params['bmin'], params['bmax']+1)


def pb_ad(a, d, params, model=2):
    # p(b|a,d) = p(a,b,d)/p(a,d) = p(a)p(b)\sum_c p(d|c)p(c|a,b)/p(a)p(b)\sum_b \sum_c p(c|a,b)p(d|c)
    def p_d_c(d, c, params):
        dist, support = pd_c(c, params)
        return dist[np.where(support == d)[0][0]]
    p_d_c_vect = np.array([p_d_c(d, c, params) for c in np.arange((d+1)/2, d+1)])
    result = []
    for b in np.arange(params['bmin'], params['bmax']+1):
        result.append(pc_ab(a, b, params)[0][(d+1)/2:(d+1)].dot(p_d_c_vect))
    return np.array(result)/sum(result), np.arange(params['bmin'], params['bmax']+1)


def pc_a(a, params, model=2):
    support = np.arange(params['amax'] + params['bmax'] + 1)
    return sum(pc_ab(a, b, params, model)[0] for b in np.arange(
        params['bmin'], params['bmax'] + 1)) / (
           params['bmax'] - params['bmin'] + 1), support


def pc_b(b, params, model=2):
    support = np.arange(params['amax'] + params['bmax'] + 1)
    return sum(pc_ab(a, b, params, model)[0] for a in np.arange(
        params['amin'], params['amax'] + 1)) / (
           params['amax'] - params['amin'] + 1), support

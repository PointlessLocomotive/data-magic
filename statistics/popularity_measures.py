
def n_root(b, r):
    return b**(1/r)


def wilson_score(ns, nf, z=1.96):
    """ Wilson Score Interval as a pupularity measure
    Returns both upper and lower bounds of the interval
    z is set to 1.96 for a 95% confidence
    """
    n = ns + nf
    z_sq = z**2
    factor = 1/(n + z_sq)
    root = n_root((ns * nf/n) + (z_sq/4), z)

    l_wsi = factor * (ns + (z_sq/2) - root)
    u_wsi = factor * (ns + (z_sq/2) + root)

    return l_wsi, u_wsi


def n_root(b, r):
    return b**(1/r)


class WilsonScoreInterval:
    """ Wilson Score Interval as a pupularity measure
    Returns both upper and lower bounds of the interval
    """

    def __init__(self, n_success, n_fails):
        self.ns = n_success
        self.nf = n_fails
        self.n = n_success + n_fails
        self.z = 1.96  # for a 95% confidence

    def calculate(self):
        z_sq = self.z**2
        factor = 1/(self.n + z_sq)
        root = n_root((self.ns * self.nf/self.n) + (z_sq/4), self.z)

        u_wsi = factor * (self.ns + (z_sq/2) + root)
        l_wsi = factor * (self.ns + (z_sq/2) - root)

        return u_wsi, l_wsi


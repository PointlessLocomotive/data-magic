from scipy.stats import spearmanr


def spearman_correlation(rank_a, rank_b):
    """ Spearman Rank Correlation
    Using scypy for performance, this is a wrapper function for consistency
    p_value is the probability of an uncorrelated system but is not used
    """
    rho, p_value = spearmanr(rank_a, rank_b)
    return rho

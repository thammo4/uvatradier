from config import *
import numpy as np


def ApEn(U, m, r) -> float:

    """
    Compute the Approximate Entropy (ApEn) of a given time series.

    Approximate Entropy is a measure of the complexity or irregularity of a time series.
    It quantifies the likelihood that similar patterns of data points will remain similar
    when the time series is extended by one data point.

    Args:
        U (list): The input time series as a list of numerical data points.
        m (int): The embedding dimension, representing the length of compared subsequences.
        r (float): The tolerance parameter that defines the maximum difference allowed between
                   data points of two subsequences to consider them as similar.

    Returns:
        float: The computed Approximate Entropy value.

    Note:
        This function uses numpy and assumes that the module 'config' is imported.

    References:
        1. Pincus, S. M. (1991). Approximate entropy as a measure of system complexity.
           Proceedings of the National Academy of Sciences, 88(6), 2297-2301.
        2. Richman, J. S., & Moorman, J. R. (2000). Physiological time-series analysis
           using approximate entropy and sample entropy. American Journal of Physiology-Heart
           and Circulatory Physiology, 278(6), H2039-H2049.
    """

    def _maxdist(x_i, x_j):
        return max([abs(ua - va) for ua, va in zip(x_i, x_j)])

    def _phi(m):
        x = [[U[j] for j in range(i, i + m - 1 + 1)] for i in range(N - m + 1)]
        C = [
            len([1 for x_j in x if _maxdist(x_i, x_j) <= r]) / (N - m + 1.0)
            for x_i in x
        ]
        return (N - m + 1.0) ** (-1) * sum(np.log(C))

    N = len(U)

    return abs(_phi(m + 1) - _phi(m))
import random
import math


def uniform(a: float = 0, b: float = 1) -> float:
    u = random.random()
    return a + (b - a) * u


def normal(mu: float = 0, sigma: float = 1) -> float:
    u1 = random.random()
    u2 = random.random()
    while u1 == 0.0:
        u1 = random.random()
    z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
    return mu + z * sigma


def gamma(alpha: float = 1) -> float:
    if alpha <= 0:
        raise ValueError("Alpha must be greater than 0")
    if alpha < 1.0:
        u = random.random()
        return gamma(alpha + 1) * math.pow(u, 1.0 / alpha)
    d = alpha - 1.0 / 3.0
    c = 1.0 / math.sqrt(9.0 * d)
    while True:
        z = normal(0, 1)
        v = 1.0 + c * z
        if v <= 0:
            continue
        v = v**3
        u = random.random()
        if u < 1.0 - 0.0331 * z**4:
            return d * v
        if math.log(u) < 0.5 * z**2 + d * (1.0 - v + math.log(v)):
            return d * v


def beta(
    alpha: float = 1, beta: float = 1, min_val: float = 0.0, max_val: float = 1.0
) -> float:
    if alpha <= 0 or beta <= 0:
        raise ValueError("Alpha and Beta must be greater than 0")
    if min_val > max_val:
        raise ValueError("The minimum value must be lower than the maximum.")
    x = gamma(alpha)
    y = gamma(beta)
    if x + y == 0:
        return min_val
    standard_beta = x / (x + y)
    return min_val + (max_val - min_val) * standard_beta


def exponential(mean: float) -> float:
    u = uniform(0, 1)
    while u == 0.0:
        u = uniform(0, 1)
    lambd = 1.0 / mean
    return -math.log(u) / lambd

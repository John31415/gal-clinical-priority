import random
import math


def uniform(a: float, b: float) -> float:
    u = random.random()
    return a + (b - a) * u


def normal(mu: float, sigma: float) -> float:
    u1 = random.random()
    u2 = random.random()
    while u1 == 0.0:
        u1 = random.random()
    z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
    return mu + z * sigma

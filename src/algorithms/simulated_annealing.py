from __future__ import annotations
import abc
import math
from src.distributions.distributions import uniform


class State(abc.ABC):

    @abc.abstractmethod
    def next(self) -> State:
        pass

    @abc.abstractmethod
    def E(self) -> float:
        pass


def _p(e_current: float, e_next: float, t: float) -> bool:
    if e_next <= e_current:
        return True
    u = uniform()
    if u == 0.0:
        return False
    return -math.log(u) * t > e_next - e_current


def simulated_annealing(
    s0: State, t0: float = 10000.0, decay: float = 0.995, t_min: float = 1.0
) -> State:
    if len(s0.s) <= 1:
        return s0
    s_current = s_best = s0
    e_current = e_best = s0.E()
    t = t0
    while t > t_min:
        s_next = s_current.next()
        e_next = s_next.E()
        if _p(e_current=e_current, e_next=e_next, t=t):
            s_current = s_next
            e_current = e_next
            if e_current < e_best:
                s_best = s_current
                e_best = e_current
        t *= decay
    return s_best

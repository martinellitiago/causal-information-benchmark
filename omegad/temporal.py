"""Stationary lag-one binary processes; discrete state and discrete time."""
import copy
from . import _binary_dynamics as core

class BinaryProcess:
    """A four-node synchronous binary process initialized at stationarity.

    Args:
        name: A name returned by available_processes().
        persistence: Optional driver persistence in [0,1), for kinetic/Boolean cases.

    Other model parameters are fixed and documented for this initial release.
    The time step is one; arbitrary delays and continuous-time integration are not implemented.
    """
    def __init__(self, name='kinetic_product', *, persistence=None):
        registry={case['id']:case for case in core.cases()}
        if name not in registry:raise ValueError('Unknown process: '+str(name))
        self._case=copy.deepcopy(registry[name])
        if persistence is not None:
            if self._case['family'] not in ('kinetic','boolean'):
                raise ValueError('persistence applies only to kinetic and Boolean drivers')
            if not 0 <= persistence < 1:raise ValueError('persistence must be in [0,1)')
            self._case['persistence']=persistence

    @property
    def parameters(self):
        """Return an independent copy of the complete mechanism definition."""
        return copy.deepcopy(self._case)

    def sample(self, n_samples, seed=0):
        """Return ordered V1,...,V4 rows, starting at numerical stationarity."""
        if isinstance(n_samples,bool) or not isinstance(n_samples,int) or n_samples<2:
            raise ValueError('n_samples must be an integer of at least two')
        return core.sample(self._case,n_samples,seed)

    def population(self):
        """Return the stationary law of (V1(t),...,V4(t),V4(t+1))."""
        q,transition=core.kernel(self._case)
        pi,_=core.stationary(transition)
        return [(x+(y,),pi[k]*(q[k][3] if y else 1-q[k][3])) for k,x in enumerate(core.STATES) for y in (0,1)]

    def ground_truth(self):
        """Return all functional lag-one links as (source,target,lag) tuples."""
        q,_=core.kernel(self._case)
        return [tuple(edge) for edge in core.ground_truth(q)[0]]

    def diagnostics(self):
        """Return target-parent diagnostics, stationary law and convergence metadata."""
        return core.analyze(self._case)


def available_processes():
    """Return names of the eleven implemented fixed mechanism templates."""
    return tuple(case['id'] for case in core.cases())

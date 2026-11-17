"""Discrete IID target mechanisms with enumerable population distributions."""
from dataclasses import dataclass
import itertools
import math
import random
from .metrics import audit

@dataclass(frozen=True)
class DiscreteModel:
    """Independent fair binary sources with a stochastic binary target.

    Args:
        rule: parity, majority, additive, product, or mixed.
        n_sources: Number of observed source bits (1 to 8).
        noise: Independent target flip probability (strictly between 0 and 0.5).
        coupling: Field strength for logistic rules; finite and positive.
    """
    rule: str = 'parity'
    n_sources: int = 3
    noise: float = 0.1
    coupling: float = 0.8

    def __post_init__(self):
        if self.rule not in ('parity','majority','additive','product','mixed'):
            raise ValueError('Unknown rule')
        if isinstance(self.n_sources,bool) or not isinstance(self.n_sources,int) or not 1 <= self.n_sources <= 8:
            raise ValueError('n_sources must be an integer from 1 to 8')
        if not 0 < self.noise < .5:
            raise ValueError('noise must be strictly between 0 and 0.5')
        if not math.isfinite(self.coupling) or not 0 < self.coupling <= 20:
            raise ValueError('coupling must be finite, positive and at most 20')
        if self.rule == 'majority' and self.n_sources % 2 == 0:
            raise ValueError('Majority requires an odd number of sources')

    def probability(self, sources):
        """Return P(Y=1 | sources); sources is a binary tuple of the declared size."""
        if len(sources)!=self.n_sources or any(x not in (0,1) for x in sources):
            raise ValueError('Expected one binary value per source')
        if self.rule in ('parity','majority'):
            bit=sum(sources)%2 if self.rule=='parity' else int(sum(sources)>self.n_sources/2)
            return 1-self.noise if bit else self.noise
        spins=[2*x-1 for x in sources]
        additive=sum(spins)/self.n_sources
        product=math.prod(spins)
        field=self.coupling*(additive if self.rule=='additive' else product if self.rule=='product' else product+.2*additive)
        logistic=1/(1+math.exp(-2*field))
        return self.noise+(1-2*self.noise)*logistic

    def population(self):
        """Enumerate normalized [(joint_state, probability), ...], target last."""
        result=[]
        for x in itertools.product((0,1),repeat=self.n_sources):
            q=self.probability(x)
            result.extend([(x+(0,),(1-q)/2**self.n_sources),(x+(1,),q/2**self.n_sources)])
        return result

    def sample(self, n_samples, seed=0):
        """Draw IID rows with a local RNG; columns are X1,...,Xn,Y."""
        if isinstance(n_samples,bool) or not isinstance(n_samples,int) or n_samples<1:
            raise ValueError('n_samples must be a positive integer')
        rng=random.Random(seed);rows=[]
        for _ in range(n_samples):
            x=tuple(rng.randrange(2) for _ in range(self.n_sources))
            rows.append(x+(int(rng.random()<self.probability(x)),))
        return rows

    def ground_truth(self):
        """Functional parent edges, independently checked by source flips."""
        edges=[]
        for i in range(self.n_sources):
            effect=max(abs(self.probability(x)-self.probability(x[:i]+(1-x[i],)+x[i+1:])) for x in itertools.product((0,1),repeat=self.n_sources))
            if effect>1e-13:edges.append((f'X{i+1}','Y',0))
        return edges

    def diagnostics(self):
        """Audit every subset of the functionally active sources."""
        parents=[int(a[1:])-1 for a,_,_ in self.ground_truth()]
        return audit(self.population(),parents,self.n_sources,[f'X{i+1}' for i in range(self.n_sources)]+['Y'])

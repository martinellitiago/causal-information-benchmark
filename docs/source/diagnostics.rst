Conditioning diagnostics
========================

For a target Y and its n known active sources, define
:math:`c_i(S)=I(X_i;Y\mid S)` for every subset of the other sources.
There are :math:`n2^{n-1}` such queries.

.. math::

   F=\sum_i c_i(\varnothing),\qquad
   M=\sum_i c_i(X_{-i}),\qquad \Omega_D=F-M.

The report includes each query, its depth, parent-wise minima, and the mean
Lk at each depth. Equal depth weighting avoids overcounting the middle
because it contains more subsets. Averaging the information chain rule over
all source permutations gives

.. math::

   \sum_{k=0}^{n-1}L_k=I(\mathbf X;Y).

The figure's exploratory all-depth contrast is therefore I(X;Y)-M. It is a
different aggregate with different coefficients, not a complete record of
the profile. A zero aggregate balance is not a zero-CMI certificate.

The local parent-faithfulness margin is the minimum over all admissible
parent/subset queries. The minimality margin is the minimum over full-parent
queries. One zero query can be concealed by positive sums or means. Passing
this restricted local audit does not certify unrestricted global faithfulness.

Population diagnostics enumerate specified laws. They do not calculate
sample-based confidence intervals, significance tests or calibrated
probabilities of causal correctness. The numerical zero tolerance is 1e-10
bits. The normalized balance is undefined when F+M is below tolerance.

For temporal processes the source variables are at t and the target at t+1.
The conditioning universe is the true lag-one parents of V4, not all possible
histories. Changing that universe changes the diagnostic.

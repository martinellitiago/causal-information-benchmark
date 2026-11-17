Discrete IID generators
=======================

All implemented IID families have independent fair binary sources
:math:`X_i\in\{0,1\}` and a binary target. Every observation is generated
independently. Let :math:`s_i=2X_i-1`, :math:`\epsilon=\mathrm{noise}`,
and :math:`a=\mathrm{coupling}`.

Boolean responses
-----------------

``parity`` sets :math:`b=(\sum_i X_i)\bmod 2`. ``majority`` sets
:math:`b=1[\sum_i X_i>n/2]` and requires odd n. Both use

.. math::

   P(Y=1\mid X)=\epsilon+(1-2\epsilon)b.

A fair-source noisy parity with n >= 2 has zero marginal information for
each source, yet positive information when all other sources are supplied.
Noise must be strictly between 0 and 0.5.

Logistic responses
------------------

Let :math:`A=\sum_i s_i/n` and :math:`B=\prod_i s_i`.

================= ========================
Rule              Field g
================= ========================
``additive``      :math:`aA`
``product``       :math:`aB`
``mixed``         :math:`a(B+0.2A)`
================= ========================

.. math::

   P(Y=1\mid X)=\epsilon+(1-2\epsilon)\sigma(2g(X)).

Coupling is positive and at most 20. The target-flip noise is applied to the
logistic response too. These rules differ from the temporal kinetic templates,
whose coefficients and noise conventions are documented separately.

Parameters and outputs
----------------------

``DiscreteGenerator(rule, n_sources=3, noise=0.1, coupling=0.8)`` supports
1 to 8 sources. The upper bound limits exact enumeration; the exhaustive
conditioning audit is more expensive than sampling. ``coupling`` is unused
for Boolean rules. ``noise`` is the target-flip probability.

* ``population()``: pairs of joint states and probabilities, target last.
* ``sample(n_samples, seed)``: IID tuples with columns X1,...,Xn,Y.
* ``ground_truth()``: functional edges (source, target, lag=0).
* ``diagnostics()``: all parent-subset CMIs and derived summaries.

The example file is ``examples/discrete_parity.py``. These constructors define
mechanisms; they do not infer parents from observational samples.

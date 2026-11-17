Model dimensions
================

Classify a generator along independent axes:

* **State space:** discrete, continuous, or mixed.
* **Sampling:** independent draws or a time-ordered process.
* **Time:** no dynamics, discrete updates, or continuous-time evolution.
* **Mechanism:** additive, joint/product, Boolean, group contagion, or mixed.

A continuous-valued process can evolve in discrete time. A binary system can
have temporal memory. A nonlinear univariate parent term is different from a
term that combines multiple parents.

Ground truth and information
-----------------------------

The structural ground truth is determined by changes to the conditional
response under controlled source flips. It is computed independently of CMI.
A cause can be functionally active even when a marginal information value is
zero. Conversely, including a product or group term does not by itself prove
an information-theoretic synergy decomposition or a faithfulness violation.

``population()`` describes a declared mathematical law. ``sample()`` generates
finite observations using a local random-number generator. Population
calculations and sample-based estimation must remain distinct.

Reproducibility
---------------

Record the package version, model name, parameters, sample count and seed.
Temporal models start from their numerically computed stationary distribution.
Their convergence residual is returned in ``diagnostics()['stationary']``.
Stationary probabilities and CMIs use floating-point arithmetic, not symbolic
proofs. The full parent-subset audit grows as n times 2 to the n-1.

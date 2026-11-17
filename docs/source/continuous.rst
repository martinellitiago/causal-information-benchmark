Continuous and mixed-state roadmap
===================================

These categories are **planned**, not implemented APIs. The current package
has no continuous-state sampler or continuous-CMI estimator.

The proposed progression is:

1. Continuous IID structural equations: additive, multiplicative and mixed
   responses with explicit exogenous noise.
2. Discrete-time continuous processes: stable linear controls, then bounded
   nonlinear lagged responses and explicit delay parameters.
3. Continuous-time dynamics: declared integrator, sampling interval,
   transients, tolerances and observation model.
4. Mixed-state mechanisms with documented support and noise conventions.

For each family, separate mechanism validity, numerical integration and
information estimation. Gaussian formulas require a suitable joint Gaussian
law; continuous-valued observations alone do not justify that assumption.
Binning changes the analyzed variables and must be explicit. Differential
entropy must not be substituted indiscriminately for discrete entropy.

The first continuous release should establish small analytically controlled
examples before extending to coupled oscillators or chaotic systems.

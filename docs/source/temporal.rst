Discrete-state temporal generators
==================================

Eleven fixed mechanism templates evolve four binary variables in discrete
time. Every node updates synchronously with an independent Bernoulli
innovation conditional on the current state:

.. math::

   T(x,x')=\prod_{j=1}^4 q_j(x)^{x'_j}[1-q_j(x)]^{1-x'_j}.

All transition probabilities are strictly between 0 and 1. The 16-state
kernel has a unique stationary law, calculated by power iteration. Samples
start in that law. These are original small implementations inspired by the
cited families, not reproductions of published parameter sets.

Kinetic and Boolean families
----------------------------

For the first three drivers, :math:`q_i=(1+\rho s_i)/2`, with default
:math:`\rho=0.65`. The ``persistence`` argument may change this to any
value in [0,1). The fourth node uses one of these rules:

====================== ===============================================
Name                   Target response
====================== ===============================================
``kinetic_pairwise``   :math:`\sigma(2(0.6s_1-0.5s_2))`
``kinetic_product``    :math:`\sigma(2(0.8s_1s_2))`
``kinetic_mixed``      :math:`\sigma(2(0.8s_1s_2+0.18s_1+0.14s_2))`
``boolean_parity``     Three-source parity with flip probability 0.1
``boolean_majority``   Three-source majority with flip probability 0.1
====================== ===============================================

At rho=0 the drivers have no self-memory. Positive rho creates self-links.
The target still depends on sources from the preceding time step.

Correlated drivers
------------------

``redundant_drivers`` uses a fresh fair V1. V2 and V3 independently copy
V1(t) into t+1 with error 0.005. The target response is
:math:`\sigma(2\times0.65(s_2+s_3))`.

``intermediate_cancellation`` uses copy error 0.1 and

.. math::

   q_4=\frac{1+0.35s_3+0.45s_2s_1+0.10s_1}{2}.

For this law, :math:`I(V_2(t);V_4(t+1)\mid V_3(t))=0`, despite positive
marginal and full-parent information for V2. This is an intermediate
conditioning cancellation, not a disappearance of the functional cause.

Group contagion
---------------

An infected node remains infected with probability :math:`1-\mu`,
where :math:`\mu=0.35`. A susceptible node becomes infected with probability

.. math::

   q_i=1-(1-h)\exp(-\beta_1 n_i-\beta_2 m_i),\qquad h=0.04.

Here n counts infected pair neighbors and m counts incident triangles whose
other two nodes are infected. Imports h prevent an absorbing all-zero state.

* ``sis_pairwise``: ring edges 12,23,34,14; rates (0.35,0).
* ``sis_simplicial``: edges 12,23,34,14,24 and triangles 124,234;
  rates (0.15,0.7).
* ``sis_group_only``: triangles 124,234; rates (0,0.9).

Node numbering here is one-based. The parameters property stores zero-based
indices. Group-only describes infection transmission; recovery still creates
self-memory. This discrete-time hazard rule is an adaptation of the simplicial
contagion family, not a continuous-time implementation.

Null control and interface
--------------------------

``independent_dynamics`` replaces every node with a fresh fair bit at every
step. It has no true edges; the endpoint balance normalization is undefined.

``BinaryProcess(name, persistence=None)`` exposes ``parameters``, ``sample``,
``population``, ``ground_truth`` and ``diagnostics``. Parameters other than
kinetic/Boolean persistence are fixed in this release. Arbitrary delays,
multiple lags and contemporaneous links are not yet implemented.

``population()`` returns the joint law of V1(t),...,V4(t),V4(t+1).
``ground_truth()`` includes all functional lag-one links, not just the target's.
``diagnostics()`` audits the target against its true lag-one parents, including
its own past when the rule contains self-dependence.

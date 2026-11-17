Getting started
===============

Install from the repository (Python 3.9+). Core generation requires only the
standard library. Installation from a public package index is not offered.

.. code-block:: bash

   python -m pip install -e .

Discrete IID example
--------------------

>>> from causal_dynamics.generators import DiscreteGenerator
>>> model = DiscreteGenerator('parity', n_sources=3, noise=0.1)
>>> rows = model.sample(100, seed=7)
>>> len(rows), len(rows[0])
(100, 4)
>>> report = model.diagnostics()
>>> round(report['F_bits'], 6)
0.0
>>> report['M_bits'] > 1.5
True

The metric has its own namespace:

>>> from causal_dynamics.measures import omega_d
>>> round(omega_d(model.population(), sources=[0, 1, 2], target=3), 3)
-1.593

Columns are X1, X2, X3, Y. ``population()`` enumerates the distribution;
``sample()`` generates observations. Population diagnostics do not estimate
information from those observations.

Temporal example
----------------

>>> from causal_dynamics.generators import BinaryProcess
>>> process = BinaryProcess('kinetic_product', persistence=0.65)
>>> series = process.sample(100, seed=7)
>>> len(series), len(series[0])
(100, 4)
>>> ('V1', 'V4', 1) in process.ground_truth()
True

Columns are V1,...,V4 in time order. The target in population diagnostics is
V4(t+1); its candidate sources are at t. Do not treat these rows as IID.

Build this documentation
------------------------

.. code-block:: bash

   python -m pip install -e '.[docs]'
   python -m sphinx -W -b html docs/source generated/docs
   python -m sphinx -W -b doctest docs/source generated/doctest

Open ``generated/docs/index.html``. To execute the standalone examples:

.. code-block:: bash

   python examples/discrete_parity.py
   python examples/lagged_product.py

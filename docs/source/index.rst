Omega D generators
==================

.. raw:: html

   <p class="omega-lead">Known mechanisms. Reproducible samples. Information at every conditioning depth.</p>
   <p>Build a synthetic distribution or temporal process, inspect its functional parents, and calculate its population information profile.</p>
   <div class="omega-grid">
     <a class="omega-card" href="quickstart.html"><strong>Start in a few lines</strong><span>Install the package, generate data, and calculate your first Omega D profile.</span></a>
     <a class="omega-card" href="discrete.html"><strong>Discrete distributions</strong><span>Parity, majority, additive, product and mixed IID mechanisms.</span></a>
     <a class="omega-card" href="temporal.html"><strong>Temporal processes</strong><span>Eleven binary lag-one models, with equations, noise and stationary sampling.</span></a>
     <a class="omega-card" href="diagnostics.html"><strong>Information diagnostics</strong><span>Endpoint balance, intermediate conditioning, local margins and their interpretation.</span></a>
     <a class="omega-card" href="api.html"><strong>API reference</strong><span>Model constructors, sampling, population laws and functional ground truth.</span></a>
     <a class="omega-card" href="continuous.html"><strong>Continuous &amp; mixed roadmap</strong><span>The next model families, clearly separated from implemented functionality.</span></a>
   </div>
   <div class="omega-status"><strong>Available now:</strong> discrete IID and discrete-time binary processes. Core generation uses the Python standard library. Continuous-state generation and sample-based CMI estimation are planned.</div>

A small example
---------------

.. code-block:: python

   from omegad import DiscreteModel

   model = DiscreteModel("parity", n_sources=3, noise=0.1)
   rows = model.sample(1000, seed=7)
   profile = model.diagnostics()
   print(profile["omega_D_bits"])

See the :doc:`quickstart` for executable examples and the :doc:`concepts`
guide for the distinction between a generating mechanism, population law,
and finite observations.

.. toctree::
   :maxdepth: 2
   :caption: Documentation

   quickstart
   concepts
   discrete
   temporal
   continuous
   diagnostics
   api
   references

"""Run after installing the repository with pip install -e ."""
from omegad import DiscreteModel
model=DiscreteModel('parity',n_sources=3,noise=0.1)
report=model.diagnostics()
print('columns: X1, X2, X3, Y')
print('first rows:',model.sample(5,seed=7))
print('functional edges:',model.ground_truth())
print({key:report[key] for key in ('F_bits','M_bits','omega_D_bits','local_faithfulness_floor_bits')})

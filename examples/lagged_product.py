"""A stationary lag-one product process, with independent runs by seed."""
from omegad import BinaryProcess
process=BinaryProcess('kinetic_product',persistence=0.65)
report=process.diagnostics()
print('columns: V1, V2, V3, V4; rows are ordered time points')
print('first rows:',process.sample(5,seed=7))
print('functional lagged edges:',process.ground_truth())
print('stationarity:',report['stationary'])
print('target diagnostics:',{key:report['target_diagnostics'][key] for key in ('F_bits','M_bits','omega_D_bits')})

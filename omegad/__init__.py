"""Synthetic mechanisms and conditioning diagnostics for Omega D."""
from .discrete import DiscreteModel
from .temporal import BinaryProcess, available_processes
from .metrics import audit, cmi, mutual_information
__version__='0.1.0'
__all__=['DiscreteModel','BinaryProcess','available_processes','audit','cmi','mutual_information']

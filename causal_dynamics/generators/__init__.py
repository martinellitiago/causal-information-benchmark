"""Known discrete IID mechanisms and binary temporal processes."""
from .discrete import DiscreteGenerator
from .temporal import BinaryProcess, available_processes
__all__=['DiscreteGenerator','BinaryProcess','available_processes']

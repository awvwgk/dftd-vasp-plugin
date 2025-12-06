from dataclasses import dataclass
from typing import Optional, TypeAlias

import numpy as np
import numpy.typing as npt

IntArray: TypeAlias = npt.NDArray[np.int_]
IndexArray: TypeAlias = npt.NDArray[np.int_]
DoubleArray: TypeAlias = npt.NDArray[np.float64]


@dataclass(frozen=True)
class ConstantsForceAndStress:
    ENCUT: float
    NELECT: float
    shape_grid: IntArray
    number_ions: int
    number_ion_types: int
    ion_types: IndexArray
    atomic_numbers: IntArray
    lattice_vectors: DoubleArray
    positions: DoubleArray
    ZVAL: DoubleArray
    POMASS: DoubleArray
    forces: DoubleArray
    stress: DoubleArray
    charge_density: Optional[DoubleArray] = None


@dataclass
class AdditionsForceAndStress:
    total_energy: float
    forces: DoubleArray
    stress: DoubleArray

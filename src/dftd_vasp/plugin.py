# SPDX-License-Identifier: Apache-2.0

import os
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import tomli

try:
    import dftd3.interface as d3
except ModuleNotFoundError:
    d3 = None

try:
    import dftd4.interface as d4
except ModuleNotFoundError:
    d4 = None

from .typing import AdditionsForceAndStress, ConstantsForceAndStress
from .units import ANGSTROM_TO_BOHR, HARTREE_TO_EV


@dataclass(frozen=True)
class DFTDConfig:
    version: str
    method: str

    def __post_init__(self):
        if self.version not in {"d4", "d3zero", "d3bj", "d3mbj", "d3mzero", "d3op"}:
            raise ValueError(f"Unsupported DFTD method: {self.method}")

        if not isinstance(self.method, str):
            raise TypeError("Method must be a string")

    @classmethod
    def load_config(cls, basename: str) -> "DFTDConfig":
        if not Path(f"{basename}.toml").exists():
            raise FileNotFoundError(f"Configuration file not found: {basename}.toml")

        with open(f"{basename}.toml", "rb") as fd:
            raw = tomli.load(fd)

        if not isinstance(raw, dict):
            raise TypeError(
                "Configuration file must contain a dictionary at the top level"
            )

        try:
            return cls(**raw)
        except TypeError as e:
            raise ValueError(
                f"Invalid configuration parameters in {basename}.toml"
            ) from e


def main(
    constants: ConstantsForceAndStress, additions: AdditionsForceAndStress
) -> None:
    DFTD_VASP_PLUGIN_INPUT = os.getenv("DFTD_VASP_PLUGIN_INPUT", "dftd-input")
    config = DFTDConfig.load_config(DFTD_VASP_PLUGIN_INPUT)

    if config.version == "d4":
        if d4 is None:
            raise ModuleNotFoundError(
                "dftd4 is not installed but required for DFTD4 calculations"
            )
        param = d4.DampingParam(method=config.method)
        disp = d4.DispersionModel(
            numbers=constants.atomic_numbers,
            positions=constants.positions * ANGSTROM_TO_BOHR,
            lattice=constants.lattice_vectors * ANGSTROM_TO_BOHR,
        )
        res = disp.get_dispersion(param=param, grad=True)

    if config.version.startswith("d3"):
        if d3 is None:
            raise ModuleNotFoundError(
                "dftd3 is not installed but required for DFTD3 calculations"
            )
        param = {
            "d3zero": d3.ZeroDampingParam,
            "d3bj": d3.RationalDampingParam,
            "d3mbj": d3.ModifiedRationalDampingParam,
            "d3mzero": d3.ModifiedZeroDampingParam,
            "d3op": d3.OptimizedPowerDampingParam,
        }[config.version](method=config.method)
        disp = d3.DispersionModel(
            numbers=constants.atomic_numbers,
            positions=constants.positions * ANGSTROM_TO_BOHR,
            lattice=constants.lattice_vectors * ANGSTROM_TO_BOHR,
        )
        res = disp.get_dispersion(param=param, grad=True)

    volume = abs(np.linalg.det(constants.lattice_vectors * ANGSTROM_TO_BOHR))

    additions.total_energy += res["energy"] * HARTREE_TO_EV
    additions.forces -= res["gradient"] * (HARTREE_TO_EV * ANGSTROM_TO_BOHR)
    additions.stress += res["virial"] * (HARTREE_TO_EV / volume)

# Vasp plugin for DFT-D3 and DFT-D4 dispersion corrections

This plugin provides an interface to use DFT-D3 and DFT-D4 dispersion corrections
within the VASP electronic structure code via the ``PLUGIN`` mechanism.

## Usage

To use the plugin install it via pip to register the plugin endpoint with VASP:

```bash
pip install git+https://github.com/awvwgk/dftd-vasp-plugin.git
```

Then, in your VASP ``INCAR`` file, set the following parameters:

```ini
PLUGINS/FORCE_AND_STRESS = T
```

The plugin requires an extra input file in TOML format to specify the DFT-D version
and the method for chosing the damping parameters. By default, the plugin looks for
a file named ``dftd-input.toml`` in the working directory. You can change this
by setting the environment variable ``DFTD_VASP_PLUGIN_INPUT`` to the desired path
(without the ``.toml`` suffix).

For PBE-D4 use the following input

```toml
version = "d4"
method = "pbe"
```

For PBE-D3(BJ) use the following input

```toml
version = "d3bj"
method = "pbe"
```

Available versions of the D3 dispersion correction are:

- `d3zero`: DFT-D3 with zero damping
- `d3bj`: DFT-D3 with Becke-Johnson damping
- `d3mbj`: DFT-D3 with modified Becke-Johnson damping
- `d3mzero`: DFT-D3 with modified zero damping
- `d3op`: DFT-D3 with optimized power damping


## License

This project is available under an Apache-2.0 license. See the LICENSE file for details.
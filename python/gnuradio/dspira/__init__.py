"""GNU Radio processing blocks for DSPIRA telescope applications."""
from .chart_recorder import chart_recorder
from .comparator import comparator
from .correlate import correlate
from .csv_filesink import csv_filesink
from .hdf5_sink import hdf5_sink
from .integration import integration
from .png_print_spectrum import png_print_spectrum
from .power_spectrum import powerSpectrum
power_spectrum = powerSpectrum
from .running_norm_std import running_norm_std
from .systemp_calibration import systemp_calibration
from .triggered_save_csv import triggered_save_csv
from .vector_moving_average import vector_moving_average

# Keep imports used by older generated programs working.
import sys as _sys
_sys.modules[__name__ + ".powerSpectrum"] = _sys.modules[__name__ + ".power_spectrum"]

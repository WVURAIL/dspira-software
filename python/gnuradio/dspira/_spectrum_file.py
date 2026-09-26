"""Write spectra without replacing an earlier capture."""

from datetime import datetime, timedelta

import numpy as np


def write_spectrum(prefix, location, azimuth, elevation, data):
    timestamp = datetime.now()
    while True:
        stamp = timestamp.strftime("%Y-%m-%d_%H.%M.%S.%f")
        filename = f"{prefix}{stamp}_{location}_{azimuth}_{elevation}_spectrum.csv"
        try:
            stream = open(filename, "x")
        except FileExistsError:
            timestamp += timedelta(microseconds=1)
            continue
        with stream:
            np.savetxt(stream, data, delimiter=",")
        return filename

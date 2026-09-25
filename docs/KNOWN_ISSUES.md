# Compatibility findings at migration

The seven applications were moved without changing their contents. A GNU Radio
3.10.9.2 generation check found existing errors in all seven files. This check
used the shared repository's block definitions and did not operate a receiver.

| Application | Observed generation errors |
| --- | --- |
| Calibrated spectrometer | Five unconnected input-port errors |
| Adding and multiplying interferometers | An invalid chooser default and two unconnected input-port errors each |
| Amplitude and standard-deviation lightning detectors | Three unconnected input-port errors each |
| Coincident and cross-correlation lightning detectors | Six unconnected input-port errors each |

Several output paths also refer to an original author's home directory. Change
these to writable folders before running an application. Receiver drivers and
hardware were not validated during the repository split.

The catalog check in CI verifies application structure. It does not establish
that GNU Radio can generate a runnable program or that a telescope is calibrated.
These compatibility findings need a separate application repair and receiver test.
The migration hashes in `migration.json` distinguish existing behavior from later changes.

# Institute DSP exercises

These 29 source flowgraphs supplement the seven classroom telescope applications.
They were developed for the DSPIRA institute by Pranav Sanghavi and contributors.
Their original MIT license is retained here; this import does not relicense them under the repository's GPL.

Download individual files from the [DSP examples page](https://wvurail.org/dspira/dsp-examples/).
Open an XML .grc file in GNU Radio Companion, which imports the older format.
Review device settings and output paths before running a receiver example.

Generation was checked with GNU Radio 3.10.9.2 on September 25, 2026.
A pass means Python code generation succeeded. It does not establish runtime or receiver operation.
Sixteen examples passed; thirteen require compatibility work.
Known failures include obsolete window constants, disconnected ports, and invalid FFT or decimation settings.
No generated Python copies are included. Edit the .grc source instead.

| Exercise | Generation check |
| --- | --- |
| [Signal controls](a1.grc) | Passed |
| [Convolution](convolution.grc) | Passed |
| [Custom noise generator](custom-noisegen.grc) | Passed |
| [Signal source exercise](ex01-1.grc) | Passed |
| [Time display exercise](ex01-2.grc) | Passed |
| [Signal combination exercise](ex01-3.grc) | Passed |
| [Frequency display exercise](ex01-4.grc) | Needs update |
| [FM receiver](fmradio.grc) | Needs update |
| [FM receiver with equalizer](fmradioeq.grc) | Needs update |
| [Fourier series](fourier-series.grc) | Passed |
| [Square-wave Fourier series](fourierseries-square.grc) | Passed |
| [Triangle-wave Fourier series](fourierseries-triangle.grc) | Passed |
| [Sine and cosine transforms](ft-sine-cos.grc) | Passed |
| [Fourier transform pairs](ftpairs.grc) | Passed |
| [Fundamental frequency with FIR filters](fundamentalfreq.grc) | Needs update |
| [Fundamental frequency with IIR filters](fundamentalfreq-iir.grc) | Passed |
| [Mixing sine waves](mixing-demo-sines.grc) | Needs update |
| [Frequency and amplitude modulation](mixing-demo-sines-freq-amplitude-modulation.grc) | Needs update |
| [Moving average demonstration](movavggeir.grc) | Passed |
| [Moving average comparison](movingaverage.grc) | Needs update |
| [Polyphase spectrometer](pfb-spectrometer.grc) | Needs update |
| [Pluto polyphase spectrometer](pfb-spectrometer-pluto.grc) | Needs update |
| [RTL-SDR polyphase spectrometer](pfb-spectrometer-rtlsdr.grc) | Needs update |
| [Sampling](sampling.grc) | Passed |
| [Sampling demonstration](sampling-demo.grc) | Passed |
| [Sawtooth Fourier transform](sawfft.grc) | Passed |
| [LimeSDR spectrometer demonstration](spectrometer-demo-lime.grc) | Needs update |
| [LimeSDR polyphase spectrometer](spectrometer-pfb-lime.grc) | Needs update |

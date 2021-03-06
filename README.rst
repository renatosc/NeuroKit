.. image:: https://raw.github.com/neuropsychology/NeuroKit/master/docs/img/banner.png
        :target: https://neurokit2.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/pypi/pyversions/neurokit2.svg
        :target: https://pypi.python.org/pypi/neurokit2

.. image:: https://img.shields.io/pypi/v/neurokit2.svg
        :target: https://pypi.python.org/pypi/neurokit2

.. image:: https://img.shields.io/travis/neuropsychology/NeuroKit.svg
        :target: https://travis-ci.org/neuropsychology/NeuroKit

.. image:: https://codecov.io/gh/neuropsychology/NeuroKit/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/neuropsychology/NeuroKit
  
.. image:: https://img.shields.io/pypi/dm/neurokit2
        :target: https://pypi.python.org/pypi/neurokit2
        
.. image:: https://api.codeclimate.com/v1/badges/517cb22bd60238174acf/maintainability
   :target: https://codeclimate.com/github/neuropsychology/NeuroKit/maintainability
   :alt: Maintainability
   

  
  
**The Python Toolbox for Neurophysiological Signal Processing (EDA, ECG, PPG, EMG, EEG...)**

This is a work in progress project meant as a continuation of `NeuroKit.py <https://github.com/neuropsychology/NeuroKit.py>`_. We are looking to build a **community of people** around this collaborative project. If you're interested by getting involved, do `let us know! <https://github.com/neuropsychology/NeuroKit/issues/3>`_


Installation
------------

To install NeuroKit, run this command in your terminal:

.. code-block::

    pip install https://github.com/neuropsychology/neurokit/zipball/master

Contribution
------------

NeuroKit2 is meant to be a all-level-friendly collaborative project. Plus, it tries to credit all contributions and contributors, so that your involvement pays off also on your CV. Thus, if you have some ideas for **improvement**, **new features**, or just wanna **learn Python** and do something useful at the same time, do not hesitate and check-out the `CONTRIBUTION GUIDE <https://neurokit2.readthedocs.io/en/latest/contributing.html>`_.


Documentation
--------------

.. image:: https://readthedocs.org/projects/neurokit2/badge/?version=latest
        :target: https://neurokit2.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/badge/functions-API-orange.svg?colorB=2196F3
        :target: https://neurokit2.readthedocs.io/en/latest/functions.html
        :alt: API
        
.. image:: https://img.shields.io/badge/tutorials-help-orange.svg?colorB=E91E63
        :target: https://neurokit2.readthedocs.io/en/latest/tutorials/index.html
        :alt: Tutorials
        
Click on the links above and check out our tutorials:

-  `Intall Python and NeuroKit <https://neurokit2.readthedocs.io/en/latest/installation.html>`_
-  `How to contribute <https://neurokit2.readthedocs.io/en/latest/contributing.html>`_

Examples
-------------

Simulate physiological signals
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    import numpy as np
    import pandas as pd
    import neurokit2 as nk

    # Generate synthetic signals
    ecg = nk.ecg_simulate(duration=10, heart_rate=70)
    rsp = nk.rsp_simulate(duration=10, respiratory_rate=15)
    eda = nk.eda_simulate(duration=10, n_scr=3)
    emg = nk.emg_simulate(duration=10, n_bursts=2)

    # Visualise biosignals
    data = pd.DataFrame({"ECG": ecg,
                         "RSP": rsp,
                         "EDA": eda,
                         "EMG": emg})
    data.plot(subplots=True, layout=(4, 1))


.. image:: https://raw.github.com/neuropsychology/NeuroKit/master/docs/img/README_simulation.png

Respiration (RSP) processing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    # Generate one minute of respiratory signal
    rsp = nk.rsp_simulate(duration=60, respiratory_rate=15)

    # Process it
    signals, info = nk.rsp_process(rsp)

    # Visualise the processing
    nk.rsp_plot(signals)


.. image:: https://raw.github.com/neuropsychology/NeuroKit/master/docs/img/README_respiration.png

Signal processing
^^^^^^^^^^^^^^^^^^

Signal cleaning
""""""""""""""""

- `signal_distord() <https://neurokit2.readthedocs.io/en/latest/functions.html#neurokit2.signal_distord>`_: Add noise of a given frequency, amplitude and shape to a signal.
- `signal_binarize() <https://neurokit2.readthedocs.io/en/latest/functions.html#neurokit2.signal_binarize>`_: Convert a continuous signal into zeros and ones depending on a given threshold.
- `signal_filter() <https://neurokit2.readthedocs.io/en/latest/functions.html#neurokit2.signal_filter>`_: Apply a lowpass, highpass or bandpass filter to the signal.
- `signal_detrend() <https://neurokit2.readthedocs.io/en/latest/functions.html#neurokit2.signal_detrend>`_: Apply a baseline (order = 0), linear (order = 1), or polynomial (order > 1) detrending to the signal (i.e., removing a general trend).
- `signal_smooth() <https://neurokit2.readthedocs.io/en/latest/functions.html#neurokit2.signal_smooth>`_: Signal smoothing using the convolution of a filter kernel.


Signal preprocessing
""""""""""""""""""""

- `signal_resample() <https://neurokit2.readthedocs.io/en/latest/functions.html#neurokit2.signal_resample>`_: Up- or down-sample a signal.
- `signal_interpolate() <https://neurokit2.readthedocs.io/en/latest/functions.html#neurokit2.signal_interpolate>`_: Interpolate (fills the values between data points) a signal using different methods.
- `signal_merge() <https://neurokit2.readthedocs.io/en/latest/functions.html#neurokit2.signal_merge>`_: Arbitrary addition of two signals with different time ranges.

Signal processing
""""""""""""""""""

- `signal_zerocrossings() <https://neurokit2.readthedocs.io/en/latest/functions.html#neurokit2.signal_zerocrossings>`_: Locate the indices where the signal crosses zero.
- `signal_findpeaks() <https://neurokit2.readthedocs.io/en/latest/functions.html#neurokit2.signal_findpeaks>`_: Locate peaks (local maxima) in a signal and their related characteristics, such as height (prominence), width and distance with other peaks.
- `signal_plot() <https://neurokit2.readthedocs.io/en/latest/functions.html#neurokit2.signal_plot>`_: Plot signal with events as vertical lines.

Other Utilities
^^^^^^^^^^^^^^^^^^

Read data
""""""""""""""""""

- `read_acqknowledge() <https://neurokit2.readthedocs.io/en/latest/functions.html#neurokit2.read_acqknowledge>`_: Read and format a BIOPAC’s AcqKnowledge file into a pandas’ dataframe.

Events *(stimuli triggers and markers)*
""""""""""""""""""""""""""""""""""""""""""

- `events_find() <https://neurokit2.readthedocs.io/en/latest/functions.html#neurokit2.events_find>`_: Find and select events in a continuous signal (e.g., from a photosensor).
- `events_plot() <https://neurokit2.readthedocs.io/en/latest/functions.html#neurokit2.events_plot>`_: Plot events in signal.
- `events_to_mne() <https://neurokit2.readthedocs.io/en/latest/functions.html#neurokit2.events_to_mne>`_: Create `MNE <https://mne.tools/stable/index.html>`_ compatible events for integration with M/EEG.

Alternatives
-------------

Here's a list of great alternative packages that you should check-out:


General
^^^^^^^

- `BioSPPy <https://github.com/PIA-Group/BioSPPy>`_
- `PySiology <https://github.com/Gabrock94/Pysiology>`_
- `PsPM <https://github.com/bachlab/PsPM>`_
- `pyphysio <https://github.com/MPBA/pyphysio>`_


ECG
^^^^

- `hrv <https://github.com/rhenanbartels/hrv>`_
- `biopeaks <https://github.com/JohnDoenut/biopeaks>`_
- `py-ecg-detectors <https://github.com/berndporr/py-ecg-detectors>`_
- `HeartPy <https://github.com/paulvangentcom/heartrate_analysis_python>`_

EDA
^^^^

- `eda-explorer <https://github.com/MITMediaLabAffectiveComputing/eda-explorer>`_
- `cvxEDA <https://github.com/lciti/cvxEDA>`_
- `Pypsy <https://github.com/brennon/Pypsy>`_
- `BreatheEasyEDA <https://github.com/johnksander/BreatheEasyEDA>`_ *(matlab)*
- `EDA <https://github.com/mateusjoffily/EDA>`_ *(matlab)*

EEG
^^^^

- `MNE <https://github.com/mne-tools/mne-python>`_
- `unfold <https://github.com/unfoldtoolbox/unfold>`_ *(matlab)*
  
  
Eye-Tracking
^^^^^^^^^^^^

- `PyGaze <https://github.com/esdalmaijer/PyGaze>`_
- `PyTrack <https://github.com/titoghose/PyTrack>`_

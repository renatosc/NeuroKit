# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd




def rsp_findpeaks(filtered_rsp, sampling_rate=1000, outlier_threshold=0.3):
    """
    https://www.biorxiv.org/content/10.1101/270348v1.full

    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> import neurokit2 as nk
    >>>
    >>> signal = np.cos(np.linspace(start=0, stop=40, num=20000))
    >>> data = nk.rsp_prepare(signal, sampling_rate=1000)
    >>> info = nk.rsp_findpeaks(filtered_rsp=data["RSP_Filtered"], sampling_rate=1000)
    >>> nk.plot_events_in_signal(signal, [info["RSP_Peaks"], info["RSP_Troughs"]])
    """
    # Try retrieving right column
    if isinstance(filtered_rsp, pd.DataFrame):
        try:
            filtered_rsp = filtered_rsp["RSP_Filtered"]
        except NameError:
            try:
                filtered_rsp = filtered_rsp["RSP_Raw"]
            except NameError:
                filtered_rsp = filtered_rsp["RSP"]


    # Detect zero crossings (note that these are zero crossings in the raw
    # signal, not in its gradient).
    greater = filtered_rsp > 0
    smaller = filtered_rsp < 0
    risex = np.where(np.bitwise_and(smaller[:-1], greater[1:]))[0]
    fallx = np.where(np.bitwise_and(greater[:-1], smaller[1:]))[0]

    if risex[0] < fallx[0]:
        startx = "rise"
    elif fallx[0] < risex[0]:
        startx = "fall"

    allx = np.concatenate((risex, fallx))
    allx.sort(kind="mergesort")

    # Find extrema by searching minima between falling zero crossing and
    # rising zero crossing, and searching maxima between rising zero
    # crossing and falling zero crossing.
    extrema = []
    for i in range(len(allx) - 1):

        # Determine whether to search for minimum or maximum.
        if startx == "rise":
            if (i + 1) % 2 != 0:
                argextreme = np.argmax
            else:
                argextreme = np.argmin
        elif startx == "fall":
            if (i + 1) % 2 != 0:
                argextreme = np.argmin
            else:
                argextreme = np.argmax

        # Get the two zero crossings between which the extreme will be
        # searched.
        beg = allx[i]
        end = allx[i + 1]

        extreme = argextreme(filtered_rsp[beg:end])
        extrema.append(beg + extreme)

    extrema = np.asarray(extrema)


    # Only consider those extrema that have a minimum vertical distance
    # to their direct neighbor, i.e., define outliers in absolute amplitude
    # difference between neighboring extrema.
    vertdiff = np.abs(np.diff(filtered_rsp[extrema]))
    avgvertdiff = np.mean(vertdiff)
    minvert = np.where(vertdiff > (avgvertdiff * outlier_threshold))[0]
    extrema = extrema[minvert]

    # Make sure that the alternation of peaks and troughs is unbroken. If
    # alternation of sign in extdiffs is broken, remove the extrema that
    # cause the breaks.
    amps = filtered_rsp[extrema]
    extdiffs = np.sign(np.diff(amps))
    extdiffs = np.add(extdiffs[0:-1], extdiffs[1:])
    removeext = np.where(extdiffs != 0)[0] + 1
    extrema = np.delete(extrema, removeext)
    amps = np.delete(amps, removeext)

    # To be able to consistently calculate breathing amplitude, make
    # sure that the extrema always start with a trough and end with a peak,
    # since breathing amplitude will be defined as vertical distance
    # between each peak and the preceding trough. Note that this also
    # ensures that the number of peaks and troughs is equal.
    if amps[0] > amps[1]:
        extrema = np.delete(extrema, 0)
    if amps[-1] < amps[-2]:
        extrema = np.delete(extrema, -1)
    peaks = extrema[1::2]
    troughs = extrema[0:-1:2]

    # Prepare output
    info = {"RSP_Peaks": peaks,
            "RSP_Troughs": troughs}
    return(info)




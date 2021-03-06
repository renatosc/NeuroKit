import numpy as np
import pandas as pd
import neurokit2 as nk

import matplotlib.pyplot as plt

# =============================================================================
# RSP - Functions
# =============================================================================
def rsp_generate(duration=90, sampling_rate=1000, respiratory_rate=15, method="simple"):

    if method == "Simple":
        actual_method = "sinusoidal"
    else:
        actual_method = "breathmetrics"

    rsp = nk.rsp_simulate(duration=duration, sampling_rate=sampling_rate, respiratory_rate=respiratory_rate, noise=0, method=actual_method)

    info = {"Duration": [duration],
            "Sampling_Rate": [sampling_rate],
            "Respiratory_Rate": [respiratory_rate],
            "Simulation": [method]}

    return rsp, info



def rsp_distord(rsp, info, noise_amplitude=0.1, noise_frequency=100):
    distorted = nk.signal_distord(rsp,
                                  noise_amplitude=noise_amplitude,
                                  noise_frequency=noise_frequency,
                                  noise_shape="laplace")
    info["Noise_Amplitude"] = [noise_amplitude]
    info["Noise_Frequency"] = [noise_frequency]
    return distorted, info



def rsp_custom_process(distorted, info, detrend_position="First", detrend_order=0, filter_order=5, filter_lowcut=None, filter_highcut=2):
    sampling_rate = info["Sampling_Rate"][0]

    if detrend_position == "First":
        distorted = nk.signal_detrend(distorted, order=detrend_order)

    if filter_lowcut == 0:
        actual_filter_lowcut = None
    else:
        actual_filter_lowcut = filter_lowcut

    distorted = nk.signal_filter(signal=distorted,
                           sampling_rate=sampling_rate,
                           lowcut=actual_filter_lowcut,
                           highcut=filter_highcut,
                           method="butterworth",
                           butterworth_order=filter_order)

    if detrend_position == "Second":
        distorted = nk.signal_detrend(distorted, order=detrend_order)

    extrema_signal, _ = nk.rsp_findpeaks(distorted, outlier_threshold=0.3)

    try:
        rate = nk.rsp_rate(peaks=extrema_signal, sampling_rate=sampling_rate)["RSP_Rate"]
    except ValueError:
        rate = np.full(len(distorted), np.nan)

    info["Detrend_Order"] = [detrend_order]
    info["Detrend_Position"] = [detrend_position]
    info["Filter_Order"] = [filter_order]
    info["Filter_Low"] = [filter_lowcut]
    info["Filter_High"] = [filter_highcut]
    return rate, info





def rsp_quality(rate, info):
    diff = info["Respiratory_Rate"][0] - rate
    info["Difference_Mean"] = np.mean(diff)
    info["Difference_SD"] = np.std(diff, ddof=1)

    data = pd.DataFrame.from_dict(info)
    return data


# =============================================================================
# RSP - Run
# =============================================================================
all_data = []
for noise_amplitude in np.linspace(0.01, 1, 5):
    print("---")
    print(noise_amplitude*100)
    print("---")
    for noise_frequency in np.linspace(1, 150, 5):
        print("%.2f" %(noise_frequency/150*100))
        for simulation in ["Simple", "Complex"]:
            for detrend_position in ["First", "Second", "None"]:
                for detrend_order in [0, 1, 2, 3, 4, 5, 6]:
                    for filter_order in [1, 2, 3, 4, 5, 6]:
                        for filter_lowcut in [0, 0.05, 0.1, 0.15, 0.2]:
                            for filter_highcut in [3, 2, 1, 0.35, 0.25]:
                                rsp, info = rsp_generate(duration=120, sampling_rate=1000, respiratory_rate=15, method=simulation)
                                distorted, info = rsp_distord(rsp, info, noise_amplitude=noise_amplitude, noise_frequency=noise_frequency)
                                rate, info = rsp_custom_process(distorted, info,
                                                                detrend_position=detrend_position,
                                                                detrend_order=detrend_order,
                                                                filter_order=filter_order,
                                                                filter_lowcut=filter_lowcut,
                                                                filter_highcut=filter_highcut)
                                data = rsp_quality(rate, info)
                                all_data += [data]
    data = pd.concat(all_data)
    data.to_csv("data.csv")

# Check
fig, axes = plt.subplots(nrows=2, ncols=2)

data.plot.scatter(x="Noise_Amplitude", y="Difference_Mean", color='r', ax=axes[0,0])
data.plot.scatter(x="Noise_Amplitude", y="Difference_SD", color='r', ax=axes[1,0])
data.plot.scatter(x="Noise_Frequency", y="Difference_Mean", color='g', ax=axes[0,1])
data.plot.scatter(x="Noise_Frequency", y="Difference_SD", color='g', ax=axes[1,1])

import numpy as np
import copy
import logging
from NuRadioReco.utilities import units
from scipy import signal
logger = logging.getLogger('channelStopFilter')


class channelStopFilter:
    """
    at the beginning and end of the trace (around the 'stop') our electronic produces a glitch
    this modules smoothly filters the beginning and the end of the trace
    """

    def begin(self):
        pass

    def run(self, evt, station, det, filter_size=0.1, prepend=128 * units.ns, append=128 * units.ns):
        """
        parameters
        ----------
        filter_size: size of tukey window (float)
            specifies the percentage of the trace where the filter is active.
            default is 0.1, i.e. the first 5% and the last 5% of the trace are filtered
        prepend: time interval to prepend
            the time span that is filled with zeros and prepended to the trace
        append: time interval to append
            the time span that is filled with zeros and appended to the trace
        """
        for channel in station.iter_channels():
            trace = channel.get_trace()
            sampling_rate = channel.get_sampling_rate()
            window = signal.tukey(len(trace), filter_size)
            trace *= window
            trace = np.append(np.zeros(np.int(np.round(prepend * sampling_rate))), trace)
            trace = np.append(trace, np.zeros(np.int(np.round(append * sampling_rate))))
            channel.set_trace(trace, sampling_rate)

    def end(self):
        pass

#!/usr/bin/env python
from __future__ import absolute_import, division, print_function
import argparse
# import detector simulation modules
import NuRadioReco.modules.efieldToVoltageConverter
import NuRadioReco.modules.trigger.simpleThreshold
import NuRadioReco.modules.channelResampler
from NuRadioReco.utilities import units
from NuRadioMC.simulation import simulation2 as simulation
import logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("runstrawman")


# initialize detector sim modules
efieldToVoltageConverter = NuRadioReco.modules.efieldToVoltageConverter.efieldToVoltageConverter()
efieldToVoltageConverter.begin()
simpleThreshold = NuRadioReco.modules.trigger.simpleThreshold.triggerSimulator()
channelResampler = NuRadioReco.modules.channelResampler.channelResampler()

class mySimulation(simulation.simulation):


    def _detector_simulation(self):
        # start detector simulation

        efieldToVoltageConverter.run(self._evt, self._station, self._det)  # convolve efield with antenna pattern
        # downsample trace to internal simulation sampling rate (the efieldToVoltageConverter upsamples the trace to
        # 20 GHz by default to achive a good time resolution when the two signals from the two signal paths are added) 
        channelResampler.run(self._evt, self._station, self._det, sampling_rate=1. / self._dt)
        
        simpleThreshold.run(self._evt, self._station, self._det,
                             threshold=3. * self._Vrms,
                             triggered_channels=None,  # run trigger on all channels
                             number_concidences=1,
                             trigger_name='simple_threshold')  # the name of the trigger
        channelResampler.run(self._evt, self._station, self._det, sampling_rate=self._sampling_rate_detector)


sim = mySimulation(eventlist='NuRadioReco/test/trigger_tests/trigger_test_eventlist.hdf5',
        outputfilename='input.hdf5',
        detectorfile='NuRadioReco/test/trigger_tests/trigger_test_detector.json',
        outputfilenameNuRadioReco='NuRadioReco/test/trigger_tests/trigger_test_input.nur',
        config_file='NuRadioReco/test/trigger_tests/config.yaml')
sim.run()


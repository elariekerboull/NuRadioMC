import numpy as np
import time

from NuRadioMC.utilities import medium, medium_base
from NuRadioReco.utilities import units
from NuRadioMC.SignalProp import analyticraytracing
from NuRadioMC.SignalProp import radioproparaytracing


class ice_model_reflection(medium_base.IceModelSimple):
    def __init__(self):
        # from https://doi.org/10.1088/1475-7516/2018/07/055 MB1 model
        super().__init__(
            n_ice=1.78,
            z_0=77.0 * units.meter,
            delta_n=0.423,
        )


def GetSolutionsSP(start, end, radio_propa=False, _cache={}):
    if "ice_model" not in _cache:
        _cache["ice_model"] = ice_model_reflection()

        config = {"propagation": {}}
        config["propagation"]["attenuate_ice"] = True
        config["propagation"]["attenuation_model"] = "SP1"
        config["propagation"]["ice_model"] = "custom"
        config["propagation"]["focusing_limit"] = 2
        config["propagation"]["focusing"] = False
        config["propagation"]["n_reflections"] = 0
        _cache["config"] = config

    if radio_propa:
        ref_index_model = "southpole_2015"
        ice = medium.get_ice_model(ref_index_model)
        rays = radioproparaytracing.radiopropa_ray_tracing(ice)  # , config=_cache["config"])
    else:
        rays = analyticraytracing.ray_tracing(_cache["ice_model"], config=_cache["config"])
    rays.set_start_and_end_point(start, end)
    rays.find_solutions()

    return rays

start = [0, 0, -100]
for i in range(20) :
    start_time = time.perf_counter()
    for z in np.linspace(-2700, -1, 100):
        for x in np.linspace(0.0001, 1, 100):
            start_time_1 = time.perf_counter()
            test_point = [np.sqrt(x) * 6000, 0, z]
            rays = GetSolutionsSP(start, test_point)
    end = time.perf_counter()
    print("Elapsed = {}s".format((end - start_time)))



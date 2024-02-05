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

start_time = time.perf_counter()
start = [0, 0, -100]

test_point = [542.8571428571429, 0.0, -150.5]
rays = GetSolutionsSP(start, test_point)
print("Number of solutions at test point", test_point, rays.get_number_of_solutions())

test_point = [542.8571428571429, 0.0, -130.5]
rays = GetSolutionsSP(start, test_point)
print("At a point closer to the surface", test_point, rays.get_number_of_solutions())

test_point = [542.8571428571429, 0.0, -250.5]
rays = GetSolutionsSP(start, test_point)
print("At a point further from surface", test_point, rays.get_number_of_solutions())

end = time.perf_counter()
print("Elapsed = {}s".format((end - start_time)))

start_time = time.perf_counter()
start = [0, 0, -100]

test_point = [542.8571428571429, 0.0, -150.5]
rays = GetSolutionsSP(start, test_point)
print("Number of solutions at test point", test_point, rays.get_number_of_solutions())

test_point = [542.8571428571429, 0.0, -130.5]
rays = GetSolutionsSP(start, test_point)
print("At a point closer to the surface", test_point, rays.get_number_of_solutions())

test_point = [542.8571428571429, 0.0, -250.5]
rays = GetSolutionsSP(start, test_point)
print("At a point further from surface", test_point, rays.get_number_of_solutions())

end = time.perf_counter()
print("Elapsed = {}s".format((end - start_time)))


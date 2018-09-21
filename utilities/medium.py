from __future__ import absolute_import, division, print_function
import numpy as np
from NuRadioMC.utilities import units


def get_ice_model(name):
    if(name == "ARAsim_southpole"):
        return ARAsim_southpole()
    elif(name == "southpole_simple"):
        return southpole_simple()
    elif(name == "mooresbay_simple"):
        return mooresbay_simple()

class medium():

    def get_index_of_refraction(self, x):
        """
        returns the index of refraction at position x

        Parameters
        ---------
        x: 3dim np.array
            point

        Returns:
        --------
        n: float
            index of refraction
        """
        return self.n_ice - self.delta_n * np.exp(x[2] / self.z_0)


class southpole_simple(medium):

    def __init__(self):
        # define model parameters (SPICE 2015/southpole)
        self.n_ice = 1.78
        self.z_0 = 71. * units.m
        self.delta_n = 0.427
        
class ARAsim_southpole(medium):

    def __init__(self):
        # define model parameters (SPICE 2015/southpole)
        self.n_ice = 1.78
        self.z_0 = 75.75757575757576 * units.m
        self.delta_n = 0.43


class mooresbay_simple(medium):

    def __init__(self):
        self.n_ice = 1.78
        self.z_0 = 34.5 * units.m
        self.delta_n = 0.46

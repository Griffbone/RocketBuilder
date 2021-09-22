import numpy as np
import scipy.optimize as opt
import propulsion as prop
import functions as fn


class LvStage:
    def __init__(self, eng, mpl=1000, dv=1000):
        self.eng = eng

        self.mpl = mpl
        self.DV = dv
        self.isp = eng.isp
        self.single_thrust = eng.F

    def mass_fractions(self):

import constants as cn


class Fluid:
    def __init__(self, name, density, temp):
        """Initialize Fluid class
            :param density: fluid density (kg/m^3)
            :param temp: fluid temperature for given density (K)
        """

        self.name = name
        self.rho = density
        self.T = temp


class Engine:
    def __init__(self, thrust, isp, fuel, ox, MR, mass=None):
        """Initialize engine class
            :param thrust: engine thrust (N)
            :param isp: specific impulse (s)
            :param fuel: fuel
            :type fuel: Fluid
            :param ox: oxidizer
            :param MR: mixture ratio (o/f)
            :type ox: Fluid
        """

        self.F = thrust
        self.isp = isp

        if mass is None:
            self.mass = 7.81e-4*thrust + 3.37e-5*thrust*np.sqrt(30) + 59

        self.ox = ox
        self.fuel = fuel
        self.MR = MR
        self.mdot = thrust/(isp*cn.g)

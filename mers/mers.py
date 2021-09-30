"""
    This file contains numerous functions to estimate the mass major vehicle components and structures.
    These functions reference the mass estimation techniques outlined in the following studies:

    1) Rohrschneider, R. R. "Development of a Mass Estimation Relationship Database for Launch
        Vehicle Conceptual Design," Georgia Institute of Technology, April 26 2002.

    2) Heineman, W. Jr. "Mass Estimation and Forecasting for Aerospace Vehicles Based on Historical Data,"
        NASA Johnson Space Center, November 1994, JSC-26098.

    3) Akin, D. L. "Mass Estimating Relations," UMD ENAE 791 lecture, 2016.

    4) Dababneh, O. and Kipouros, T. "A Review of Aircraft Wing Mass Estimation Methods," November 8 2017.
"""

import numpy as np
import constants as cns


# =============== STRUCTURAL COMPONENT MERS =============== #
def engine_mass(T, eps, p0):
    """ Function to estimate mass of pump-fed rocket engines (with gimbals)
        Ref: Akin p. 25

        :param T: thrust (N)
        :param eps: expansion ratio
        :param p0: chamber pressure (Pa)
        :return m: mass of engine and gimbals (kg)
    """

    m = 7.81e-4*T + 3.37e-5*T*eps**(1/2) + 59
    m_g = 237.8*(T/p0)**0.9375

    return m + m_g


def thrust_struct_mass(T):
    """ Function to estimate mass of vehicle thrust structure
        Ref: Akin p. 25

        :param T: thrust (N)
        :return m: thrust structure mass
    """

    m = 2.55e-4*T
    return m


def tanks_mass(v, prop):
    """ Function to estimate mass of a propellant tank
        Ref: Akin p. 6

        :param v: propellant volume (m^3)
        :param prop: propellant type
        :return m: propellant tank mass (kg)
    """

    if prop.nam.upper() == 'LH2':
        m = 9.09*v
    else:
        m = 12.16*v

    return m


def insulation_mass(a, prop):
    """ Function to estimate tank insulation mass
        Ref: Akin p. 8

        :param a: area of the propellant tank (m^2)
        :param prop: propellant type
        :return m: insulation mass (kg)
    """

    if prop.name.upper() == 'LH2':
        m = 2.88*a
    elif prop.name.upper() == 'LOX':
        m = 1.123*a
    else:
        m = 0

    return m


def copv_mass(v):
    """ Function to estimate the mass of a COPV
        Ref: Akin p. 13

        :param v: volume of the COPV (m^3)
        :return m: mass of the COPV (kg)
    """

    m = 115.3*v + 3
    return m


def titanium_tank_mass(v):
    """ Function to estimate the mass of a titanium tank
        Ref: Akin p. 13

        :param v: volume of the tank (m^3)
        :return m: mass of the tank
    """

    m = 299.8*v + 2
    return m


def fairing_mass(a):
    """ Function to estimate the mass of a fairing
        Ref: Akin p. 20

        :param a: area of the fairing
        :return m: mass of the fairing
    """

    m = 4.95*a**1.15

    return m


# def electronic_mass(m_wet, l):
#     """ Function to estimate the mass of avionics and wiring
#         Ref: Akin p. 20
#
#         :param m_wet: wet mass of the vehicle
#         :param l: length of the vehicle
#         :return m: mass of avionics and wiring
#     """
#
#     m = 10*m_wet**0.361 + 1.058*np.sqrt(m_wet)*l**0.25
#
#     return m

def avionics_mass(m_dry):
    """ Function to determine mass of avionics.
        Ref: Rohrschneider 13-2.

        :param m_dry: vehicle dry mass (kg)
        :return m: avionics mass (kg)
    """

    m_dry *= 2.20462
    m = (710*m_dry**0.125)/2.20462

    return m


def electronic_mass(m_dry):
    """ Function to estimate mass of wiring in a vehicle
        Ref: Rohrschneider 10-4

        :param m_dry: vehicle dry mass
        :return m: vehicle electronic conversion/distribution mass
    """

    m = 0.062*m_dry
    return m


# =============== PROPELLANT MERS =============== #
def residual_mass(m_prop):
    """ Function to estimate residual propellant mass
        Ref: Rohrschneider 20-2

        :param m_prop: propellant mass (kg)
        :return m: residual propellant mass (kg)
    """

    m_prop *= 2.20462
    m = 0.05*m_prop**0.79

    return m


def reserve_prop(m_prop):
    """ Function to estimate reserve propellant mass
        Ref: Rohrschneider 25-3

        :param m_prop: propellant mass
        :return m: reserve propellant mass
    """

    m = m_prop*0.005
    return m


# =============== AERONAUTICAL MERS =============== #
def wing_area(m_dry, loading):
    """ Function to calculate wing area from loading and dry mass
        :param m_dry: dry mass of the vehicle (kg)
        :param loading: wing loading (Pa)

        :return a: wing area (m^2)
    """

    w = m_dry*cns.g
    a = w/loading

    return a


def tail_area(span, s, lvt, cvt=0.07):
    """ Function to calculate vertical stabilizer area from wing parameters
        :param span: wingspan
        :param s: wing surface area
        :param lvt: distance from quarter-chord point on wing to same point on tail
        :param cvt: tail volume coefficient

        :return svt: area of the vertical stabilizer
    """

    svt = (cvt*span*s)/lvt

    return svt


def wing_mass(s, span, m_dry, rc, trc=0.04, xlf=5):
    """ Function to estimate wing mass based on wing geometry.
        Ref: Dababneh and Kipouros equation 1.

        :param s: wing area (m^2)
        :param span: structural wing span (m)
        :param m_dry: dry mass (kg)
        :param rc: root chord (m)
        :param trc: ratio of root thickness to root chord
        :param xlf: ultimate load factor

        :return wt: mass of the wing (kg)
    """

    span *= 3.28084
    m_dry *= 2.20462
    s *= 10.7639
    rc *= 3.28084
    t_root = rc*trc

    wt = (110*m_dry*xlf*span*s**0.77)/(t_root*10e6)

    return wt/2.20462


def tail_mass(s):
    """ Function to estimate the mass of a vertical stabilizer
        Ref: Rohrschneider 2-2. Assumes aluminum stringer/skin structure.

        :param s: area of the stabilizer (m^2)
        :return m: mass of the stabilizer (kg)
    """

    s *= 10.7639
    m = 1.872*s**1.24

    return m/2.20462


def elevon_mass(s):
    """ Calculate mass of elevons on the main wing.
        Ref: Rohrschneider 1-8.

        :param s: wing area (m^2)
        :return m: mass of elevons (kg)
    """

    s *= 10.7639
    m = 9.4*(0.14*s) + 0.07*s

    return m/2.20462


def tps_mass(a_wet):
    """ Calculate TPS mass. Ref: Heineman (JSC-26098) p. A-7
        :param a_wet: wet area of spacecraft (m^2)
        :return m: mass of TPS (kg)
    """
    a_wet *= 10.7639

    m = 6.78*a_wet

    return m/2.20462


def gear_mass(m_dry):
    """ Function to estimate landing gear mass. Assumes tricycle gear.
        Ref: Rohrschneider 5-8

        :param m_dry: dry mass of the vehicle (kg)
        :return m: mass of the landing gear (kg)
    """

    m_dry *= 2.20462
    m_main = 0.00927*m_dry**1.0861
    m_nose = 0.001514*m_dry**1.0861

    return (m_main + m_nose)/2.20462


# =============== HUMAN SPACEFLIGHT MERS =============== #
def volume_cabin(n_crew, n_days, quality=1):
    """ Function to estimate crew cabin volume. Data interpolated from NASA STD-3001 Fig. 8.6.2.1-1
        :param n_crew: number of crew members
        :param n_days: number of days on-orbit
        :param quality: quality of space (1 = tolerable, 2 = performance, 3 = optimal)

        :return v: crew cabin volume (m^3)
    """

    t = n_days/30

    if quality == 1:
        v = 0.0005*t**5 - 0.0178*t**4 + 0.2376*t**3 - 1.4839*t**2 + 4.3053*t + 0.4891

        if t > 6:
            v = 5.03
    elif quality == 2:
        v = 0.0142*t**3 - 0.3856*t**2 + 3.4125*t + 0.5169

        if t > 6:
            v = 10.18
    elif quality == 3:
        v = -0.0043*t**4 + 0.1347*t**3 - 1.5625*t**2 + 8.0679*t + 2.8018

        if t > 6:
            v = 18.48
    else:
        raise ValueError("'quality' parameter must be between 1 and 3. Got {}".format(quality))

    return v*n_crew


def eclss_mass(v_cabin, n_crew, n_days, m_av):
    """ Function to determine mass of ECLSS.
        Ref: Rohrschneider 14-2

        :param v_cabin: crew cabin volume (m^3)
        :param n_crew: number of crew
        :param n_days: number of days on orbit
        :param m_av: mass of vehicle avionics (kg)

        :return m: eclss mass (kg)
    """

    v_cabin *= 35.3147
    m_av *= 2.20462

    m = 5.85*v_cabin**0.75 + 10.9*n_crew*n_days + 0.44*m_av

    return m/2.20462


def equipment_mass(n_crew, n_days):
    """ Function to estimate mass of equipment (food, water, furnishings) for a vehicle.
        Ref: Rohrschneider 17-3

        :param n_crew: number of crew
        :param n_days: number of days on orbit
        :return m: mass of consumables and equipment
    """

    m = 1176 + (311 + 23*n_days)*n_crew

    return m/2.20462


def gross_mass(n_crew, n_days, v_cabin):
    """ Function to estimate the gross mass of a crewed vehicle
        Ref: Heineman (JSC-26098) p. A-7

        :param n_crew: number of crew members
        :param n_days: number of days on-orbit
        :param v_cabin: volume of the crew cabin (m^3)

        :return m: gross mass of the crewed vehicle
    """

    v_cabin *= 35.3147
    m = (330.51*(n_crew*n_days*v_cabin)**0.3574)

    return m/2.20462


def module_mass(v_cabin):
    """ Function to estimate the structural mass of a crew module
        Ref: Heineman (JSC-26098) p. 20

        :param v_cabin: cabin volume (m^3)
        :return m: cabin structural mass (kg)
    """

    v_cabin *= 35.3147
    m = 187.064*v_cabin**0.62

    return m/2.20462


def crew_cabin_mass(n_crew, n_days, m_dry, quality=2, method='r'):
    """ Function to estimate the mass of a crew cabin (consumables/structure/ECLSS)
        :param n_crew: number of crew members
        :param n_days: number of days on orbit
        :param m_dry: vehicle dry mass (kg)
        :param quality: quality of space (1 = tolerable, 2 = performance, 3 = optimal)
        :param method: calculation method (r = Rohrschneider, h = Heineman)

        :return m: mass of crew cabin (kg)
    """

    v_cabin = volume_cabin(n_crew, n_days, quality)

    if method.upper() == 'R':
        m_av = avionics_mass(m_dry)
        m_ls = eclss_mass(v_cabin, n_crew, n_days, m_av)
        m_eq = equipment_mass(n_crew, n_days)
        m_cab = module_mass(v_cabin)

        m = m_av + m_ls + m_eq + m_cab
    elif method.upper() == 'H':
        m = gross_mass(n_crew, n_days, v_cabin)
    else:
        raise ValueError("Invalid 'method' parameter. Expected 'r' or 'h,' got: {}".format(method))

    return m
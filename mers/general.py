"""
    This file contains numerous functions to estimate the mass of vehicle aerostructures.
    These functions reference the mass estimation techniques outlined in the following studies:

    1) Rohrschneider, R. R. "Development of a Mass Estimation Relationship Database for Launch
        Vehicle Conceptual Design," Georgia Institute of Technology, April 26 2002.

    2) Heineman, W. Jr. "Mass Estimation and Forecasting for Aerospace Vehicles Based on Historical Data,"
        NASA Johnson Space Center, November 1994, JSC-26098.

    3) Akin, D. L. "Mass Estimating Relations," UMD ENAE 791 lecture, 2016.
"""

import numpy as np


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


def electronic_mass(m_wet, l):
    """ Function to estimate the mass of avionics and wiring
        Ref: Akin p. 20

        :param m_wet: wet mass of the vehicle
        :param l: length of the vehicle
        :return m: mass of avionics and wiring
    """

    m = 10*m_wet**0.361 + 1.058*np.sqrt(m_wet)*l**0.25

    return m


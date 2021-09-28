""""
    This file contains numerous functions to estimate the mass of a crewed space vehicle. 
    These functions reference the mass estimation techniques outlined in the following studies:
    
    1) Rohrschneider, R. R. "Development of a Mass Estimation Relationship Database for Launch 
        Vehicle Conceptual Design," Georgia Institute of Technology, April 26 2002.
    
    2) Heineman, W. Jr. "Mass Estimation and Forecasting for Aerospace Vehicles Based on Historical Data," 
        NASA Johnson Space Center, November 1994, JSC-26098.

    3) "Man-Systems Integration Standards, Revision B," NASA, July 1995, NASA STD-3000.
"""


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


def mass_avionics(m_dry):
    """ Function to determine mass of avionics.
        Ref: Rohrschneider 13-2.

        :param m_dry: vehicle dry mass (kg)
        :return m: avionics mass (kg)
    """

    m_dry *= 2.20462
    m = (710*m_dry**0.125)/2.20462

    return m


def mass_eclss(v_cabin, n_crew, n_days, m_av):
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


def mass_equip(n_crew, n_days):
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


def mass_module(v_cabin):
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
        m_av = mass_avionics(m_dry)
        m_ls = mass_eclss(v_cabin, n_crew, n_days, m_av)
        m_eq = mass_equip(n_crew, n_days)
        m_cab = mass_module(v_cabin)

        m = m_av + m_ls + m_eq + m_cab
    elif method.upper() == 'H':
        m = gross_mass(n_crew, n_days, v_cabin)
    else:
        raise ValueError("Invalid 'method' parameter. Expected 'r' or 'h,' got: {}".format(method))

    return m

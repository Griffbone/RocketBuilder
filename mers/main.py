import fluids as fld


def m_tank(fld, A, V):
    """ Function to calculate propellant tank mass from geometry and propellant characteristics
        Additionally calculates propellant tank insulation and baffle/anti-vortex device masses

        :param fld: fluid contained in the propellant tank
        :param A: propellant tank surface area
        :param V: propellant tank volume
    """

    if fld.name.upper() == 'LH2':
        m = 9.09*V + 2.88*A
    elif fld.name.upper() == 'LOX':
        m = 12.16*V + 1.123*A
    else:
        m = 12.16*V

    return m


def m_thrust_struct():
    """ Function to calculate thrust structure mass from thrust

    """

    pass


def m_shroud():
    """ Function to calculate mass of shrouds and fairings from surface area

    """

    pass
import numpy as np
import constants as cns


def v_circ(alt):
    """ Function to calculate circular orbit velocity from altitude
        :param alt: orbital altitude (m)
        :return v: orbital velocity (m/s)
    """

    v = np.sqrt(cns.mu/(cns.re + alt))
    return v


def v_grav(alt):
    """ Function to estimate gravity loss for launch to final altitude
        Edberg and Costa Eq. 3.13 (p. 145)

        :param alt: orbital altitude
        :return v: gravity loss
    """

    v = 0.8*np.sqrt((2*cns.g*alt)/(1 + alt/cns.re))

    return v


def v_rot(vi, lat, i):
    """ Function to calculate delta-v saved from rotation of the Earth
        :param vi: final orbit inertial velocity (m/s)
        :param lat: final orbit latitude (deg)
        :param i: final orbit inclination (deg)

        :return dv_saved: delta-v saved by rotation of the Earth (m/s)
    """

    ai = np.arcsin(np.cos(np.radians(i))/np.cos(np.radians(lat)))
    vr = ((2*np.pi*cns.re)/cns.t_rotation)*np.cos(np.radians(lat))
    vx = vi*np.sin(ai) - vr
    vy = vi*np.cos(ai)

    ar = np.arctan(vx/vy)
    dv = np.sqrt(vx**2 + vy**2)
    dv_saved = vi - dv

    return dv_saved

import numpy as np
import constants as cn
import propulsion as prop
import matplotlib.pyplot as plt
from newtonraphson import newton_raphson


def mass_fractions(isp, dv, pi_se):
    """Function to calculate mass fractions
        :param isp: specific impulse (s)
        :param dv: delta-V (m/s)
        :param pi_se: structure mass fraction
        :return pi_bo: burnout mass fraction
        :return pi_prop: propellant mass fraction
        :return pi_pl: payload mass fraction
        :return pi_se: structural mass fraction
    """
    ve = isp*cn.g
    pi_bo = np.exp(-dv/ve)

    if pi_se > pi_bo:
        # print('Structure mass fraction greater than burnout mass fraction')
        return None

    pi_pl = pi_bo - pi_se
    pi_prop = 1 - pi_bo

    return pi_bo, pi_prop, pi_pl, pi_se


def prop_budget(m_prop, engine, f_ullage=0.05, t_startup=1):
    """Function to calculate propellant masses and volumes
        :param m_prop: propellant mass (kg)
        :param engine: engine type
        :param f_ullage: ullage fraction (fraction of total tank volume)\
        :param t_startup: startup time (s)
        :type engine: Engine
        :return m_ox: oxidizer mass (kg)
        :return m_f: fuel mass (kg)
        :return v_ox: oxidizer volume (m^3)
        :return v_fuel: fuel volume (m^3)
        :return startup_losses: startup propellant losses (kg)
    """

    if f_ullage >= 1:
        print('Ullage fraction too high: less than or equal to one')
        return None
    if f_ullage < 0:
        print('Ullage fraction too low: must be over zero')

    ox = engine.ox
    fuel = engine.fuel

    m_ox_startup = (engine.mdot*t_startup*2*engine.MR)/(engine.MR + 1)
    m_ox = (engine.MR*m_prop)/(engine.MR + 1)
    v_ox = ((m_ox + m_ox_startup)/ox.rho)/(1 - f_ullage)

    m_fuel_startup = (engine.mdot*t_startup*2)/(engine.MR + 1)
    m_f = m_prop/(engine.MR + 1)
    v_f = ((m_f + m_fuel_startup)/fuel.rho)/(1 - f_ullage)

    startup_losses = m_fuel_startup + m_ox_startup

    return m_ox, m_f, v_ox, v_f, startup_losses


def size_tank(v_tank, geometry, dome_fraction=0.7, diam=3.7):
    if type(geometry) != str:
        print('Tank geometry must be ' + str(str) + ' not ' + str(type(geometry)))
        return None

    if v_tank <= 0:
        print('Unable to create tank geometry. Tank volume must be over zero')
        return None

    if geometry.upper() in ['SPHERE', 'SPHERICAL']:
        r = ((3*v_tank)/(4*np.pi))**(1/3)
        area = 4*np.pi*r**2
        height = r*2
        d = height
    elif geometry.upper() in ['ELLIPSE', 'ELLIPTICAL', 'ELLIPSOID']:
        r = diam/2
        a = r*dome_fraction

        v_caps = (4/3)*np.pi*a*r**2
        v_cyl = v_tank - v_caps
        l_cyl = v_cyl/(np.pi*r**2)

    else:
        print('Unrecognized tank geometry: ' + str(geometry))
        return None

    return 12.16*v_tank


def get_margin(engine, mpl, dv, pi_se):
    fracs = mass_fractions(engine.isp, dv, pi_se)

    if fracs is None:
        while fracs is None:
            pi_se = pi_se/2
            fracs = mass_fractions(engine.isp, dv, pi_se)

    pi_bo, pi_prop, pi_pl, pi_se = fracs
    m0 = mpl/pi_pl
    m_se = m0*pi_se
    m_prop = pi_prop*m0

    ne = np.ceil(1.2*m0*cn.g/engine.F)

    m_ox, m_f, v_ox, v_f, losses = prop_budget(m_prop, engine)
    m_act = (v_ox + v_f)*12.16 + losses + engine.mass*ne
    margin = ((m_se - m_act)/m_act * 100) - 15

    return margin, m0, ne


def size_vehicle(mpl, dv, engine):
    x1 = 0.01
    change = 1

    while abs(change) >= 1e-6:
        prev = x1

        dx = -0.001*x1
        x2 = x1 + dx

        margin = get_margin(engine, mpl, dv, x1)
        margin2 = get_margin(engine, mpl, dv, x2)

        m1 = margin[0]
        m2 = margin2[0]

        m = (m2 - m1)/dx
        x1 = (-m1/m) + x1

        change = x1 - prev

    return get_margin(engine, mpl, dv, x1)[1], margin[2]


fs = np.linspace(0.1, 0.9, 100)
ms = []
v1s = []
v2s = []
nes = []

for f in fs:
    v1 = 9000*f
    v2 = 9000*(1 - f)

    m2 = size_vehicle(1000, v2, prop.rl10)
    m1 = size_vehicle(m2[0], v1, prop.rl10)
    ms.append(m1[0])
    nes.append(m1[1] + m2[1])

    v1s.append(v1)
    v2s.append(v2)

plt.subplot(1, 2, 1)
plt.plot(fs, ms)
plt.subplot(1, 2, 2)
plt.plot(fs, nes)

plt.show()

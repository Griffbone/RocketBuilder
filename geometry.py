import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt


def revolve_integral(x, y, xmin, xmax):
    """ Function to calculate surface area and volume of an arbitrary solid of rotation about the x axis.
        Function utilized a 3D trapezoidal integration method - adds frustums of length dx together.

        :param x: x stations of the solid
        :param y: radii of the solid
        :param xmin: lower bound of integration
        :param xmax: upper bound of integration

        :return v: volume
        :return a: area
    """

    v = 0
    a = 0
    for i in range(0, len(x) - 1):
        if (xmin <= x[i]) and (xmax >= x[i]):
            r1 = y[i]
            r2 = y[i+1]
            h = x[i+1] - x[i]

            vi, ai = frustum(r1, r2, h)
            v += vi
            a += ai

    return v, a


def frustum(r1, r2, h):
    """ Function to calculate volume and curved surface area of a frustum of a cone
        :param r1: base radius
        :param r2: tip radius
        :param h: frustum height

        :return v: volume
        :return a: area
    """

    v = ((np.pi*h)/3)*(r1**2 + r2**2 + r1*r2)
    a = np.pi * (r1 + r2) * np.sqrt((r1 - r2) ** 2 + h ** 2)

    return v, a


def cylinder(r, h):
    """ Function to calculate volume and curved surface area of a cylinder
        :param r: cylinder radius
        :param h: cylinder height

        :return v: volume
        :return a: area
    """

    v = (np.pi*r**2)*h
    a = 2*np.pi*r*h

    return v, a


def tangent_ogive(L, R, f=0.1):
    """ Function to calculate volume, area, and shape of a tangent ogive nosecone
        :param L: length of nosecone
        :param R: base radius of nosecone
        :param f: nose radius as fraction of base radius

        :return v: volume
        :return a: area
        :return x: x stations of nosecone
        :return y: radii of nosecone
    """

    rho = (R**2 + L**2)/(2*R)

    rn = f*R
    x0 = L - np.sqrt((rho - rn)**2 - (rho - R)**2)
    yt = (rn*(rho - R))/(rho - rn)
    xt = x0 - np.sqrt(rn**2 - yt**2)
    xa = x0 - rn

    x = np.linspace(xt, L, 1000)
    y = np.sqrt(rho**2 - (L - x)**2) + R - rho

    x2 = np.linspace(-rn, xt-x0, 1000, )
    y2 = np.sqrt(rn**2 - x2**2)
    x2 += xa + rn

    x = np.concatenate([x2, x]) - xa
    y = np.concatenate([y2, y])

    v, a = revolve_integral(x, y, min(x), max(x))

    return v, a, x, y


def ellipsoid(r, a):
    """ Function to calculate the volume and surface area of an ellipsoid
        :param r: radius
        :param a: minor axis height

        :return v: volume
        :return sa: surface area
    """

    v = (4/3)*np.pi*a*r**2
    sa = 4*np.pi*(((r**2)**1.6 + 2*(r*a)**1.6)/3)**(1/1.6)

    return v, sa


def delta_wing(db, s, AR, k=0.1):
    """ Function to calculate the shape of a delta wing
        :param db: body diameter
        :param s: wing area
        :param AR: wing aspect ratio
        :param k: tip chord as fraction of central chord

        :return cc: central chord
        :return rc: root chord
        :return tc: tip chord
        :return b: wing span
    """

    b = np.sqrt(AR*s)
    cc = s/(b*k + (b/2)*(1-k))
    tc = k*cc

    tant = (b/2)/(cc - tc)
    lr = (db/2)/tant
    rc = cc - lr

    return cc, rc, tc, b
# v, a, x, y = tangent_ogive(6, 3.7/2, 0.25)
# plt.plot(x, y)
# plt.plot(x, -y)
#
# print(revolve_integral(x, y, 2.5, max(x)))
# plt.axis('equal')
# plt.show()

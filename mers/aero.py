"""
    This file contains numerous functions to estimate the mass of vehicle aerostructures.
    These functions reference the mass estimation techniques outlined in the following studies:
    
    1) Rohrschneider, R. R. "Development of a Mass Estimation Relationship Database for Launch 
        Vehicle Conceptual Design," Georgia Institute of Technology, April 26 2002.
    
    2) Heineman, W. Jr. "Mass Estimation and Forecasting for Aerospace Vehicles Based on Historical Data," 
        NASA Johnson Space Center, November 1994, JSC-26098.
        
    3) Dababneh, O. and Kipouros, T. "A Review of Aircraft Wing Mass Estimation Methods," November 8 2017. 
"""
import numpy as np
import constants as cns


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


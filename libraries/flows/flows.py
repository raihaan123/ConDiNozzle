
'''
Tracking the flow state for the selected nozzle geometry and pressure ratio

'''

import numpy as np


# Flow functions

def aas(m, g):
    r = 1.0 / m * (2.0 / (g + 1.0) * (1.0 + (g - 1.0) / 2.0 * m ** 2.0)) ** ((g + 1.0) / 2 / (g - 1.0))
    return r
#r=1./m.*(2/(g+1)*(1+(g-1)/2*m.^2)).^((g+1)/2/(g-1));

def pp0(m, g):
    r = (1.0 + (g - 1.0) / 2.0 * m ** 2.0) ** (-g / (g - 1.0))
    return r


def p02p01(m, g):
    r = ((g + 1.0) * m ** 2.0 / ((g - 1.0) * m ** 2.0 + 2.0)) ** (g / (g - 1.0)) * ((g + 1.0) / (2.0 * g * m ** 2.0 - (g - 1.0))) ** (1.0 / (g - 1.0))
    return r


def p2p1(m, g):
    r = 1.0 + 2.0 * g / (g + 1.0) * (m ** 2.0 - 1.0)
    return r


def nu(m, g):
    n = np.sqrt((g + 1.0) / (g - 1.0)) * np.arctan(np.sqrt((g - 1.0) / (g + 1.0) * (m ** 2.0 - 1.0))) - np.arctan(np.sqrt(m ** 2.0 - 1.0))
    return n


def m_pp0(pp0, g):
    r = np.sqrt((pp0 ** (-(g - 1.0) / g) - 1.0) * 2.0 / (g - 1.0))
    return r


def m_aas(a, g, super):
    m = np.zeros(np.size(a))
    m[a < 1.0] = np.nan
    m[a == 1.0] = 1.0   

    if super == 1:                                          # super=1 returns supersonic solutions, else subsonic
        minit = 1e5
    else:
        minit = 1e-5
    
    for n in range(np.size(a)):
        if m[n] == 0:
            m0 = 1.0
            m1 = minit

            while np.abs(m1 - m0) > 1e-6:
                m0 = m1
                f = aas(m0, g) - a[n]
                fp = (2.0 / (g + 1.0) * (1.0 + (g - 1.0) / 2.0 * m0 ** 2.0)) ** ((g + 1.0) / 2 / (g - 1.0) - 1.0) - aas(m0, g) / m0
                m1 = m0 - f / fp
                if m1 < 0:
                    m1 = m0 / 2.0
                
            m[n] = m1

    return m


def m_p02p01(r, g):
    r = np.array([r])
    m = np.zeros(np.size(r))
    m[r < 0.0] = np.nan
    m[r > 1.0] = np.nan
    m[r == 1.0] = 1.0
    
    minit = 2.0
    eps = 1e-4

    for n in range(np.size(r)):
        if m[n] == 0:
            m0 = 1.0
            m1 = minit
            while abs(m1 - m0) > eps:
                m0 = m1
                f = p02p01(m0, g) - r[n]
                f1 = p02p01(m0 + eps, g) - r[n]
                fp = (f1 - f) / eps
                m1 = m0 - f / fp
            m[n] = m1

    return m
    

def me(pbpc, aeat, g):
    meChoke = m_aas(np.array([aeat]), g, 0)
    pbpcChoke = pp0(meChoke, g)
    meDesign = m_aas(np.array([aeat]), g, 1)
    pbpcDesign = pp0(meDesign, g)
    pbpcSAE = p2p1(meDesign, g) * pbpcDesign

    if pbpc >= 1:
        me = 0
    elif pbpc >= pbpcChoke:
        me = m_pp0(pbpc, g)
    elif pbpc >= pbpcSAE:
        me = np.sqrt(-1 / (g - 1) + np.sqrt(1 / (g - 1) ** 2 + 2 / (g - 1) * (2 / (g + 1)) ** ((g + 1) / (g - 1)) / aeat ** 2 / pbpc ** 2))
    else:
        me = meDesign
    return me




def flow_state(pc_pb, ae_at, g):

    # All possible flow states
    states = ["No Flow - Increase Pressure Ratio!", "Subsonic Flow", "Shock in Nozzle", "Shock at Exit", "Overexpanded Flow", "Design Condition!", "Underexpanded Flow"]

    # Calculating the Design, Subsonic Choked and Shock at Exit flow regimes
    meD = m_aas(np.array([ae_at]), g, 1)
    pbpcD = pp0(meD, g)

    meC = m_aas(np.array([ae_at]), g, 0)
    pbpcC = pp0(meC, g)

    pbpcS = p2p1(meD, g) * pbpcD

    # Evaluating the flow state
    if pc_pb <= 1:
        state = 0                   # No flow
    elif pc_pb <= 1 / pbpcC:
        state = 1                   # Subsonic flow
    elif pc_pb <= 1 / pbpcS:
        state = 2                   # Shock in nozzle
    elif pc_pb == 1 / pbpcS:
        state = 3                   # Shock at exit
    elif pc_pb <= 1 / pbpcD:
        state = 4                   # Overexpanded flow
    elif pc_pb == 1 / pbpcD:
        state = 5                   # Design condition
    else:
        state = 6                   # Underexpanded flow
    
    return pbpcC, states[state]
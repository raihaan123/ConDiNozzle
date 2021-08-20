
'''
Flow state identifier

'''

from .flow_funcs import *


def flow_state(x, y, pc_pb, ae_at, g):

    # All possible flow states
    states = ["No Flow - Increase Pressure Ratio!", "Subsonic Flow", "Shock in Nozzle", "Shock at Exit", "Overexpanded Flow", "Design Condition!", "Underexpanded Flow"]

    # Calculating the Design, Subsonic Choked and Shock at Exit flow regimes
    meD = m_aas(np.array([ae_at]), g, 1)
    pbpcD = pp0(meD, g)

    meC = m_aas(np.array([ae_at]), g, 0)
    pbpcC = pp0(meC, g)

    pbpcS = p2p1(meD, g) * pbpcD

    # Evaluating the flow state
    m = [np.nan]
    ppc = [np.nan]

    if pc_pb <= 1:
        state = 0                   # No flow

    elif pc_pb <= 1 / pbpcC:
        state = 1                   # Subsonic flow
        mexit = m_pp0(1/pc_pb, g)
        aeas = aas(mexit, g)
        m = m_aas(y * aeas / ae_at, g, 0)
        m[y * aeas / ae_at <= 1] = 1
        ppc = pp0(m, g)
        # axes(ui.axes(2));plot(x,m,'b');ylabel('M');yl=ylim;ylim([0 yl(2)]);xlim(ui.xlim);
        # axes(ui.axes(3));plot(x,ppc,'b');ylabel('p/p_c');yl=ylim;ylim([0 yl(2)]);xlim(ui.xlim);
        # hold on;plot([x(end) ui.xlim(2)-0.5],[ppc(end) pbpc],'b:',[ui.xlim(2)-0.5 ui.xlim(2)],[pbpc pbpc],'b');hold off;

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

    
    return pbpcC, states[state], m[:-1], ppc[:-1]
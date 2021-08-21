
'''
Flow state identifier

'''

from .flow_funcs import *


def flow_state(x, y, pc_pb, ae_at, ai_at, g):

    # All possible flow states
    states = ["No Flow - Increase Pressure Ratio!", "Subsonic Flow", "Shock in Nozzle", "Shock at Exit", "Overexpanded Flow", "Design Condition!", "Underexpanded Flow"]

    # Calculating the Design, Subsonic Choked and Shock at Exit flow regimes
    meD = m_aas(np.array([ae_at]), g, 1)
    print(meD)
    pbpcD = pp0(meD, g)

    meC = m_aas(np.array([ae_at]), g, 0)
    pbpcC = pp0(meC, g)

    pbpcS = p2p1(meD, g) * pbpcD

    m = [np.nan]
    ppc = [np.nan]

    # Evaluating the flow state
    if pc_pb <= 1 / pbpcC:
        mexit = m_pp0(1/pc_pb, g)
        aeas = aas(mexit, g)
        m = m_aas(y * aeas / ae_at, g, 0)
        m[y * aeas / ae_at <= 1] = 1
        ppc = pp0(m, g)

        # Mach and Pressure graphs

        # axes(ui.axes(2));plot(x,m,'b');ylabel('M');yl=ylim;ylim([0 yl(2)]);xlim(ui.xlim);
        # axes(ui.axes(3));plot(x,ppc,'b');ylabel('p/p_c');yl=ylim;ylim([0 yl(2)]);xlim(ui.xlim);
        # hold on;plot([x(end) ui.xlim(2)-0.5],[ppc(end) pbpc],'b:',[ui.xlim(2)-0.5 ui.xlim(2)],[pbpc pbpc],'b');hold off;

        # No flow
        if pc_pb <= 1:
            state = 0

        # Subsonic flow
        else:
            state = 1
            
            # Adding flow visuals to the nozzle figure

            # axes(ui.axes(1));hold on; %plot flow
            # hflow=fill([x ui.xlim(2) ui.xlim(2) ui.xlim(1)],[y y(end) 0 0],[0.85 0.85 1]);set(hflow,'Linestyle','none');
            # hold off 


    # Shock in nozzle
    elif pc_pb <= 1 / pbpcS:
        state = 2

        mexit = me(1/pc_pb, ae_at, g)
        pep02 = pp0(mexit, g)
        p02pc = (1/pc_pb) / pep02

        m1 = m_p02p01(p02pc, g)
        a1 = aas(m1, g)

        # Sorting indicies
        up = np.where(x < 0)[0]

        md1 = np.where(x >= 0)
        md2 = np.where(y * ai_at < a1)
        md = np.intersect1d(md1, md2)

        dn1 = np.where(x > 0)
        dn2 = np.where(y * ai_at > a1)
        dn = np.intersect1d(dn1[0], dn2[0])

        m = np.hstack(( m_aas(ai_at * y[up], g, 0), m_aas(ai_at * y[md], g, 1), m_aas(ai_at * y[dn] * p02pc, g, 0) ))

        ppc = pp0(m, g)
        ppc[dn] = ppc[dn] * p02pc

        # All the graphs!

        # axes(ui.axes(2));plot(x,m,'b');ylabel('M');yl=ylim;ylim([0 yl(2)]);xlim(ui.xlim);
        # axes(ui.axes(3));plot(x,ppc,'b');ylabel('p/p_c');yl=ylim;ylim([0 yl(2)]);xlim(ui.xlim);
        # hold on;plot([x(end) ui.xlim(2)-0.5],[ppc(end) pbpc],'b:',[ui.xlim(2)-0.5 ui.xlim(2)],[pbpc pbpc],'b');hold off;
        # axes(ui.axes(1));hold on; %plot flow and shock
        # hflow=fill([x ui.xlim(2) ui.xlim(2) ui.xlim(1)],[y y(end) 0 0],[0.85 0.85 1]);set(hflow,'Linestyle','none');
        # xs=x(md(end))+(a1-y(md(end)))/(y(dn(1))-y(md(end)))*(x(dn(1))-x(md(end)));
        # hshock=plot([xs xs],[0 a1],'r');set(hshock,'linewidth',m1,'color',[1 1-tanh(m1-1) 1-tanh(m1-1)]);
        # hold off

    # Shock at exit
    elif pc_pb == 1 / pbpcS:
        state = 3       

    # Overexpanded flow
    elif pc_pb <= 1 / pbpcD:
        state = 4

    # Design condition
    elif pc_pb == 1 / pbpcD:
        state = 5

    # Underexpanded flow
    else:
        state = 6

    
    return pbpcC, states[state], m[:-1], ppc[:-1]
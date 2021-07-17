
'''
Interactive Converging-Diverging Nozzle Visualisation
---> To complement the Compressible Flow Rig!

A pythonic refactoring of CDN.m by William Devenport, Virginia Tech

===================================================================
Mechanical Engineering, Imperial College London

'''

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import plotly
import plotly.graph_objs as go


st.write("""
## Interactive Converging-Diverging Nozzle Visualisation
### Department of Mechanical Engineering, Imperial College London
""")
st.text("")

# Fixed parameters
x_max = 10
init_ae_at = 2.5
init_g = 1.4
init_pb_pc = 1.0

# Using sidebar
with st.sidebar:
    st.title("Input Parameters"); st.write("")

    # Various sliders for input
    ae_at = st.number_input("Exit / Throat Area Ratio (Ae/At)", value=init_ae_at, step=0.1)
    pb_pc = st.number_input("Back / Critical Pressure Ratio (Pb/Pc)", value=init_pb_pc, step=0.1)
    g = st.number_input("Gamma (Cp/Cv)", value=init_g)


# Calculating the nozzle geometry - comments are MATLAB snippets from CDN.m

# xc=-3:.1:0;
xc = np.arange(-3, 0, 0.1)
# yc=1+xc.^2/4.5;
yc = 1 + xc**2/4.5
# xd=0:.1:xmax;
xd = np.arange(0, x_max, 0.1)
# yd=tanh(2*xd/xmax)/tanh(2)*(aeat-1)+1;
yd = np.tanh(2*xd/x_max)/np.tanh(2)*(ae_at-1) + 1
# x=[xc xd]; y=[yc yd];
x = np.concatenate((xc, xd))
y = np.concatenate((yc, yd))

# Plotting nozzle geometry with plotly
trace = go.Scatter(
    x=x,
    y=y,
    mode='lines',
    name='Nozzle Geometry',
    line=dict(
        color='rgb(200, 0, 0)',
        width=1
    )
)
layout = go.Layout(
    title='Nozzle Geometry',
    xaxis=dict(
        title='x'
    ),

    yaxis=dict(
        title='y'
    )
)

# Set x limits for fig to be [-3, x_max]

fig = go.Figure(data=[trace], layout=layout)
st.plotly_chart(fig, use_container_width=True)

# fig, ax = plt.subplots()
# # ymax=max([3 y(end)*1.5]);
# ymax = max(3, y[-1]*1.5)
# st.write(y[-1]*1.5)
# # fill([x x(end) x(1)],[y  ymax ymax],[0.85 0.85 0.85]);
# ax.fill([x[0], x[-1], x[0], x[-1]], [y[0], ymax, ymax, y[0]], '0.85')
# # plot(x,y,'k');ylim([0 ymax]);ylabel('A/A_t');xlim(x_max);
# ax.plot(x, y, 'k')
# ax.set_ylim([0, ymax])
# ax.set_ylabel('A/A_t')
# ax.set_xlim([-3, x_max])
# # plot([x(end) x(end)],[y(end) ymax],'k');
# ax.plot([x[-1], x[-1]], [y[-1], ymax], 'k')

# # Show figure on streamlit
# st.write(fig)

# Plotting nozzle geometry - using plotly




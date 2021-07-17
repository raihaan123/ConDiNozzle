
'''
Interactive Converging-Diverging Nozzle Visualisation
---> To complement the Compressible Flow Rig!

A pythonic refactoring of CDN.m by William Devenport, Virginia Tech

===================================================================
Mechanical Engineering, Imperial College London

'''

import streamlit as st
import numpy as np
import plotly.graph_objs as go

from nozzle import nozzle

st.set_page_config(page_title='Interactive Con-Di Nozzle',
                   page_icon='media/mech.jpg',
                   layout='wide')


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

x, y, y_max = nozzle(ae_at, x_max)


# Plotting nozzle geometry with Plotly
trace1 = go.Scatter(
    x=x,
    y=y,
    mode='lines',
    name='Nozzle Geometry',
    line=dict(
        color='rgb(153, 0, 51)',
        width=5
    ),
    # fill = 'tozeroy',
    # fillcolor='rgba(0,0,0,0.1)',
    showlegend=False
)

trace2 = go.Scatter(
    x=x,
    y=np.ones(np.shape(y)) * (y_max+1),
    mode='lines',
    fill='tonexty',
    fillcolor='rgba(150,0,0,0.3)',
    showlegend=False
)

layout = go.Layout(
    title='Nozzle Geometry',
    xaxis=dict(
        title='x'
    ),
    xaxis_range=[-3, x_max+2],
    yaxis=dict(
        title='y'
    ),
    yaxis_range=[0, y_max]
)

fig = go.Figure(data=[trace1, trace2], layout=layout)
st.plotly_chart(fig, use_container_width=True)

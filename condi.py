
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

# Nozzle and flow funcions
from libraries.nozzle import nozzle_calc, nozzle_plot, x_max
from libraries.flows import states


st.set_page_config(page_title='Interactive Con-Di Nozzle',
                   page_icon='media/mech.jpg',
                   layout='wide')


st.write("""
## Interactive Converging-Diverging Nozzle Visualisation
### Department of Mechanical Engineering, Imperial College London
""")
st.text("")

# Starting parameters - no-flow state
init_ae_at = 2.5
init_g = 1.4
init_pb_pc = 1.0

# Using sidebar
with st.sidebar:
    st.header("Input Parameters"); st.write("")

    # Various sliders for input
    ae_at = st.number_input("Exit / Throat Area Ratio (Ae/At)", value=init_ae_at, step=0.1)
    pb_pc = st.number_input("Back / Critical Pressure Ratio (Pb/Pc)", value=init_pb_pc, step=0.1)
    g = st.number_input("Gamma (Cp/Cv)", value=init_g)

    # Return current state
    st.write("## Current state: ", states[0])


# Calculating the nozzle geometry - comments are MATLAB snippets from CDN.m
x, y, y_max = nozzle_calc(ae_at, x_max)

# Plotting nozzle geometry with Plotly
fig = nozzle_plot(x, y, y_max, x_max)
st.plotly_chart(fig, use_container_width=True)

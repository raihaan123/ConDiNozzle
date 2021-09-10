
'''
Interactive Converging-Diverging Nozzle Visualisation
---> Integrating with the Compressible Flow Rig!

A pythonic refactoring of CDN.m (William Devenport, Virginia Tech) by Raihaan Usman

===================================================================
Mechanical Engineering, Imperial College London

'''

import streamlit as st
import asyncio
import base64
import pandas as pd


# Nozzle and flow funcions
from libraries.nozzle import nozzle_calc, nozzle_plot, x_max
from libraries.flows import *
from libraries.utils import *


st.set_page_config(page_title='Interactive Con-Di Nozzle',
                   page_icon='media/mech.jpg',
                   layout='wide'
                )


rec_state = st.empty()

st.write("""
## Interactive Converging-Diverging Nozzle Visualisation
### Department of Mechanical Engineering, Imperial College London
""")
st.text("")

# Starting parameters - no-flow state
init_ae_at = 2.5
init_ai_at = 3.0
init_g = 1.4
init_pc_pb = 1.0

# Datalogging setup in SessionState
logger = 'logger'
if logger not in st.session_state:
    st.session_state[logger] = []

# Using sidebar
with st.sidebar:

    st.header('Demo Setup')

    status = st.empty()
    connect = st.checkbox("Connect to Flow Rig")
    record = st.empty()
    
    st.header("Analytic Parameters"); st.write("")

    # Various sliders for input
    with st.expander("Nozzle Geometry", expanded=True):
        ai_at = st.number_input("Compression Ratio (Ai/At)", value=init_ai_at, step=0.1)
        ae_at = st.number_input("Expansion Ratio (Ae/At)", value=init_ae_at, step=0.1)
        export = st.button("Export to CSV")

    with st.expander("Flow Parameters", expanded=True):
        curr_state = st.empty()
        pc_pb = st.number_input("Chamber / Back Pressure Ratio (Pc/Pb)", value=init_pc_pb, step=0.1)
        g = st.number_input("Gamma (Cp/Cv)", value=init_g)

    download = st.button("Export Results")

# Calculating the nozzle geometry - comments are MATLAB snippets from CDN.m
x, y, y_max = nozzle_calc(ae_at, ai_at, x_max)

# Evaluating the flow state
pbpcB, state, m, ppc = flow_state(x, y, pc_pb, ae_at, ai_at, g)

# Return current state
curr_state.info(state)

# Plotting nozzle geometry with Plotly
fig = nozzle_plot(x, y, y_max, x_max)
st.plotly_chart(fig, use_container_width=True)

# Pressure profile through nozzle - also includes real time data
rt_ptaps = st.empty()
if connect == False:
    analytic_pressure = plot_pressure(x, ppc)
    st.plotly_chart(analytic_pressure, use_container_width=True)

with st.expander("Pressure Data"):
    st.write(ppc)

# Mach profile through nozzle
fig3 = plot_mach(x, m)
st.plotly_chart(fig3, use_container_width=True)

with st.expander("Mach Data"):
    st.write(m)



recordKey = 'record_key'
if recordKey not in st.session_state:
    st.session_state[recordKey] = False

if st.session_state[recordKey]:
    record.button('Stop recording')
    if record:
        rec_state.empty()
        st.session_state[recordKey] = False

else:
    record.button('Start recording')
    if record:
        rec_state.info('Recording!')
        st.session_state[recordKey] = True


stub = st.empty()


# Real time data!
if connect and record:
    st.session_state[logger].append(asyncio.run(rt_dataprocessing(rt_ptaps, x, ppc, status, stub, True)))
    print(st.session_state[logger])
    # st.sidebar.write(st.session_state[logger])

elif connect:
    asyncio.run(rt_dataprocessing(rt_ptaps, x, ppc, status, False))

else:
    status.error(f"Disconnected from Flow Rig!")



# Sample code for exporting pandas dataframes to CSV

# if download:
#   'Download Started!'
#   liste= ['A','B','C']
#   df_download= pd.DataFrame(liste)
#   df_download.columns=['Title']
#   df_download
#   csv = df_download.to_csv(index=False)
#   b64 = base64.b64encode(csv.encode()).decode()  # some strings
#   linko= f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download csv file</a>'
#   st.markdown(linko, unsafe_allow_html=True)
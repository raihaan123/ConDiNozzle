
'''
Interactive Converging-Diverging Nozzle Visualisation
---> To complement the Compressible Flow Rig!

A pythonic refactoring of CDN.m (William Devenport, Virginia Tech) by Raihaan Usman

===================================================================
Mechanical Engineering, Imperial College London

'''

import streamlit as st
import base64
import pandas as pd


# Nozzle and flow funcions
from libraries.nozzle import nozzle_calc, nozzle_plot, x_max
from libraries.flows import find_state, states


st.set_page_config(page_title='Interactive Con-Di Nozzle',
                   page_icon='media/mech.jpg',
                   layout='wide')


st.write("""
## Interactive Converging-Diverging Nozzle Visualisation
### Department of Mechanical Engineering, Imperial College London
""")
st.text("")

# Return current state
st.info(states[0])

# Starting parameters - no-flow state
init_ae_at = 2.5
init_ai_at = 3.0
init_g = 1.4
init_pb_pc = 1.0

# Using sidebar
with st.sidebar:
    st.header("Input Parameters"); st.write("")

    # Various sliders for input
    with st.beta_expander("Nozzle Geometry", expanded=True):
        ai_at = st.number_input("Compression Ratio (Ai/At)", value=init_ai_at, step=0.1)
        ae_at = st.number_input("Expansion Ratio (Ae/At)", value=init_ae_at, step=0.1)
        export = st.button("Export to CSV")
    
    pb_pc = st.number_input("Chamber / Back Pressure Ratio (Pc/Pb)", value=init_pb_pc, step=0.1)
    g = st.number_input("Gamma (Cp/Cv)", value=init_g)

    download = st.button("Export Results")

# Calculating the nozzle geometry - comments are MATLAB snippets from CDN.m
x, y, y_max = nozzle_calc(ae_at, ai_at, x_max)

# Plotting nozzle geometry with Plotly
fig = nozzle_plot(x, y, y_max, x_max)
st.plotly_chart(fig, use_container_width=True)

pressures =  st.beta_expander("Pressure Distribution")
with pressures:
    st.write("Coming soon!")

with st.beta_expander("Mach Distribution"):
    st.write("Coming soon!")



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
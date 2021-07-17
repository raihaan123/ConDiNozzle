
'''
Calculating the nozzle geometry - comments are MATLAB snippets from CDN.m

Inputs: Ae_At, x_max
Outputs: x, y, y_max
'''

import numpy as np
import plotly.graph_objects as go


def nozzle_calc(ae_at, x_max):

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
    # ymax=max([3 y(end)*1.5]);
    y_max = max(3, y[-1]*1.5)

    # Adding trailing edge of nozzle
    return([np.concatenate((x, [x_max])), np.concatenate((y, [y_max])), y_max])


# Plotting nozzle geometry with Plotly
def nozzle_plot(x, y, y_max, x_max):
    
    trace1 = go.Scatter(
        x=x,
        y=y,
        mode='lines',
        name='Nozzle Geometry',
        line=dict(
            color='rgb(153, 0, 51)',
            width=3
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
        xaxis_range=[-3, x_max+2],
        yaxis=dict(
            title='A / At'
        ),
        yaxis_range=[0, y_max]
    )

    fig = go.Figure(data=[trace1, trace2], layout=layout)
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)

    
    return fig
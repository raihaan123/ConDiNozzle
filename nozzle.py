import numpy as np

# Calculating the nozzle geometry - comments are MATLAB snippets from CDN.m
# Inputs: Ae_At, x_max
# Outputs: x, y, y_max

def nozzle(ae_at, x_max):

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
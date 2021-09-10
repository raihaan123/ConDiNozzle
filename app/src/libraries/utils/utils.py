import aiohttp
from os import getenv
import plotly.graph_objects as go
import pandas as pd

from libraries.flows import *


# Lengthwise locations of the pressure sensors
ptap_locs = [-2, 0, 2, 5]


if getenv("IS_DOCKERIZED"):
    WS_CONN = "ws://wsserver/pressureTaps"
else:
    WS_CONN = "ws://localhost:8000/pressureTaps"


async def rt_dataprocessing(graph, x, ppc, status, stub, logging=False):

    df = pd.DataFrame(columns=["Tapping 1", "Tapping 2", "Tapping 3", "Tapping 4"])

    async with aiohttp.ClientSession(trust_env = True) as session:
        status.info(f"Connecting to {WS_CONN}")

        async with session.ws_connect(WS_CONN) as websocket:
            status.success(f"Connected to Flow Rig at {WS_CONN} !")

            async for message in websocket:
                data = message.json()["data"]
                fig = plot_pressure(x, ppc)
                fig.add_trace(
                    go.Scatter(
                        x=ptap_locs,
                        y=data,
                        mode='lines+markers',
                        name='Raw',
                        line=dict(
                            color='rgb(102, 255, 0)',
                            width=1
                        ),
                        showlegend=True
                    )
                )

                graph.plotly_chart(fig, use_container_width=True)

                if logging:
                    # Add list data to dataframe
                    df.loc[len(df)] = data
                    stub.write(df)

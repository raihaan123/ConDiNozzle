import aiohttp
from collections import deque, defaultdict
from functools import partial
from os import getenv
# import plotly.express as px
import plotly.graph_objects as go

from libraries.flows import *


# Lengthwise locations of the pressure sensors
ptap_locs = [-2, 0, 2, 5]


if getenv("IS_DOCKERIZED"):
    WS_CONN = "ws://wsserver/pressureTaps"
else:
    WS_CONN = "ws://localhost:8000/pressureTaps"


async def rt_dataprocessing(graph, x, ppc, status):

    # window = deque(([0 for _ in range(10)]), maxlen=10)

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
                # graph.plotly_chart(px.line(data))

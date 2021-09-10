from fastapi import FastAPI, WebSocket
import asyncio
import numpy as np


app = FastAPI()

@app.websocket("/pressureTaps")

# This is where the serial sensor data integrates to the Streamlit app using websockets
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.send_json({
            "data": list(np.random.uniform(0.5,0.95, size=4))
            }
        )
        await asyncio.sleep(0.1)

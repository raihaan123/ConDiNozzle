from fastapi import FastAPI, WebSocket
# from random import choice, randint
import asyncio
import numpy as np


app = FastAPI()

@app.websocket("/pressureTaps")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.send_json({
            "data": list(np.random.uniform(0.5,0.95, size=4))
            }
        )
        await asyncio.sleep(0.1)

# numpy random array of length 4

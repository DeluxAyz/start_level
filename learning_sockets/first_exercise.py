# check out logic journal and void extended v2 for stuff on Websockets to see logs

# first exercise - echopipe

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
 
echo_app = FastAPI()

@echo_app.websocket("/echo")
async def websocket_endpoint(websocket: WebSocket):

    # accepting the connection, completing the handshake
    await websocket.accept()
    print("Client Connected")


    try:
        while True:
            # an indefinitely rummng loop, waiting for messages from the client
            echo_data = await websocket.receive_text()
            # await pauses the function until the message is received
            
            # echoing the data back across the open connection (the echo pipe)
            await websocket.send_text(f"Server Echo: {echo_data}")

    except WebSocketDisconnect:
        # Connection seems to be closed; so cleaning up (using normal print now, no more sending data)
        print("Client Echoes no more")
        
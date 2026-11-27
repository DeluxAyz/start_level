# check out logic journal and void extended v2 for stuff on Websockets to see logs

# second exercise - an in memory connection manager
# largely helped by the Fast API docs here

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

connection_app = FastAPI()

class ConnectionManager:
    # using a constructor to maintain an internal list of active connections
    def __init__(self):
        self.activeConnections: dict[str, WebSocket] = {}
        # using type hints for validation to make sure it's a list of WebSocket objects
        # oh actually changed to dict rather than list, to also include client id
        # but we didn't inherit from any pydantic class, so does the validation work?
        # answer from Gemini, no it's just a regular type hint

    # a connect method to accept and register websockets
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.activeConnections[client_id] = websocket
    # i'm guessing async useful here because we don't want to proceed till we connect

    # a disconnect method, obviously, to remove sockets when users leave
    def disconnect(self, client_id: str):
        # so we assume it's already disconnected, so just cleanup
        self.activeConnections.pop(client_id, None)
        # since it's after the websocket closes, it doesn't need to await

    # a broadcast method, to iterate over all socket and send a message
    async def broadcast(self, message: str):
        for connection in self.activeConnections.values():
            await connection.send_text(message)

    # learnt from the docs, not part of exercise but trying to send a personal message
    async def transmit_personal(self, message: str, client_id: str):
        websocket = self.activeConnections.get(client_id)
        if websocket is not None:
            await websocket.send_text(message)


manager_object = ConnectionManager()

# an HTTP endpoint to send a message to a specific client
@connection_app.post("/send/{client_id}")
async def post(client_id: str, message: str):
    await manager_object.transmit_personal(message, client_id)
    return {"status": "sent", "to": client_id}

# a /chat endpoint created with the manager
@connection_app.websocket("/chat/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager_object.connect(websocket, client_id=client_id)
    try:
        while True:
            # read and echo back what the client sends
            data = await websocket.receive_text()
            await manager_object.broadcast(f"{client_id}: {data}")
            await manager_object.transmit_personal(f'Client {client_id} says: ', data)
    except WebSocketDisconnect:
        manager_object.disconnect(client_id)
        await manager_object.broadcast(f"{client_id} left the chat")
    

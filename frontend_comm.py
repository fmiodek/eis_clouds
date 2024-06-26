import websockets
import asyncio
import json
from game_logic import balloons, daily_record, season_record

HOST = "localhost"
WEBSOCKET_PORT = 8080

async def send_data(websocket):
    try:
        while True:
            data = [balloon.score for balloon in balloons]
            data.append(daily_record)
            data.append(season_record)
            await websocket.send(json.dumps(data))
            await asyncio.sleep(0.5)  # 500ms interval (optional)
    except Exception as e:
        print("Error in sending data to frontend")
        await websocket.close()

start_server = websockets.serve(send_data, HOST, WEBSOCKET_PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

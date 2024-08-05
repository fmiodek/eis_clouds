

"""
async def send_data(websocket, path):
    while True:
        try:
            data = game_logic.currentScores
            await websocket.send(json.dumps(data))
            await asyncio.sleep(0.5)  # 500ms interval (optional)
        except Exception as e:
            print("Error in sending data to frontend")
            await websocket.close()

start_server = websockets.serve(send_data, HOST, WEBSOCKET_PORT)
loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()


import websockets
import asyncio
import json
import sys

HOST = "192.168.76.152"
WEBSOCKET_PORT = 2207


async def websocket_handler(websocket, path):
    global currentScores
    while True:
        try:
            # Prepare the message (e.g., replace this with actual data retrieval)
            message = currentScores
            # Send the message
            await websocket.send(json.dumps(message))
            # Print confirmation and flush the output
            print("sent")
            sys.stdout.flush()
            # Wait for the next interval
            await asyncio.sleep(1)  # Send data every second
        except Exception as e:
            print(f"Error: {e}")
            sys.stdout.flush()
            break  # Exit the loop if there is an error

async def main():
    async with websockets.serve(websocket_handler, HOST, WEBSOCKET_PORT):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
"""
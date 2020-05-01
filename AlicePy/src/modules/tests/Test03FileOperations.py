#!/usr/bin/env python3
import asyncio
import pathlib
import websockets

#'wss://ant.aliceblueonline.com/hydrasocket/v2/websocket/pKbXDMubx1UEhg4__ufy2_YOvf0iOOvjIjrlQkc0950.VGBPVlWTJn3td7KS1D5ErhuhyAQ5ter2gOPzYeIExLY'

async def consumer_handler(websocket) -> None:
	async for message in websocket:
		print(message)
async def consume(hostname: str):
	websocket_resource_url = f"wss://ant.aliceblueonline.com/hydrasocket/v2/websocket/pKbXDMubx"
	async with websockets.connect(websocket_resource_url) as websocket:
		await consumer_handler(websocket)

loop = asyncio.get_event_loop()
loop.run_until_complete(consume('wss://ant.aliceblueonline.com/hydrasocket/v2/websocket/pKbXDM'))
loop.run_forever()
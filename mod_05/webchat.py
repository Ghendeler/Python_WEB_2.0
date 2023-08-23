import asyncio
import logging

import names
import websockets
from currency_rate import get_currency_rate
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK

logging.basicConfig(level=logging.INFO)


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            await self.send_to_clients(f"{ws.name}: {message}")
            if message.startswith('exchange'):
                data = message.split(' ')
                await self.get_echange_rate(data[1])

    async def get_echange_rate(self, data):
        message = 'Курс валют в Привате:'

        bot = "currency bot"
        currency_rate = await get_currency_rate(int(data))
        for k, v in currency_rate.items():
            message += f'<br>{k}'
            for cur, rate in v.items():
                message += f'<br>{cur}: {rate["purchase"]} - {rate["sale"]}'

        await self.send_to_clients(f"{bot}: {message}")


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())

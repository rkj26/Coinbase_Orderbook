'''
Basic Use Case to test the orderbook class
'''
import asyncio
from src.orderbook import OrderBook


async def logic():
    while True:
        result = await orderbook.get_top(10)
        print(result)


async def main(logic):
    await orderbook.connect()
    await asyncio.wait([orderbook.run_loop(), logic()])


if __name__ == "__main__":
    orderbook = OrderBook()
    asyncio.get_event_loop().run_until_complete(main(logic))

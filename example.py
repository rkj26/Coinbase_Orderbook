'''
Basic Use Case to test the orderbook class
'''
import asyncio
from src.orderbook import OrderBook

async def main():
    await client.connect()
    while True:
        await client.run_loop()
        top = await client.get_top()
        print(top)
        
if __name__ == "__main__":
    client = OrderBook(depth=10)
    print(client)
    asyncio.get_event_loop().run_until_complete(main())
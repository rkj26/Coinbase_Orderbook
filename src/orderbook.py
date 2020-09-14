'''
Class for maintaining orderbook, and storing training data
'''
from collections import OrderedDict
import asyncio
import json
import numpy as np
import websockets


class OrderBook:
    '''
    Orderbook Class for maintaining
    '''

    def __init__(self, depth=10):
        '''
        Basic initialisation Parameters
        '''
        self.state = OrderedDict({'bids': {}, 'asks': {}})
        self.last_update = None
        self.training_data = []
        self.uri = 'wss://ws-feed.pro.coinbase.com'
        self.socket = websockets
        self.depth = depth
    async def connect(self, product_id='BTC-USD'):
        'Connects to CoinBase Websocket'
        print('Completed this!')
        self.socket = await websockets.connect(self.uri, ping_interval=None)
        message = {
            "type": "subscribe",
            "product_ids": [product_id],
            "channels": ["level2"],
        }
        await self.socket.send(json.dumps(message))

    async def run_loop(self):
        while True:
            received = await self.socket.recv()
            received = json.loads(received)
            # print(received)
            # top = await self.get_top()
            # print(top)
            await self.update(received)

    def add_side(self, elements, side):
        for element in elements:
            price = float(element[0])
            volume = float(element[1])
            self.state[side][price] = volume

    def update_side(self, changes):
        if changes[0] == "buy":
            side = 'bids'
        if changes[0] == 'sell':
            side = 'asks'
        price = float(changes[1])
        volume = float(changes[2])
        if volume != 0:
            self.state[side][price] = volume
        else:
            del self.state[side][price]

    async def update(self, message):
        if message['type'] == 'snapshot':
            bids = message['bids']
            asks = message['asks']
            self.add_side(bids, 'bids')
            self.add_side(asks, 'asks')
        if message['type'] == 'l2update':
            self.last_update = message['time']
            change = message['changes'][0]
            self.update_side(change)
        await self.build_record()

    async def build_record(self):
        record = await self.get_top()
        await self.build_training_data(100, record)

    async def build_training_data(self, timestep, record):
        '''
        Update training data
        '''
        N = len(self.training_data)
        self.training_data.append(record)
        if N > timestep:
            self.training_data.append(record)
            self.training_data = self.training_data[-timestep:]

    def get_training_data(self, timestep):
        '''
        Get training data
        '''
        if len(self.training_data) == timestep:
            return self.training_data
        return None

    async def get_top(self):
        bids = sorted(self.state['bids'].keys(), reverse=True)[:self.depth]
        asks = sorted(self.state['asks'].keys())[:self.depth]
        bid_volumes = [self.state['bids'][x] for x in bids]
        ask_volumes = [self.state['asks'][x] for x in asks]
        record = bids+asks+bid_volumes+ask_volumes
        record = np.array(record)
        return record

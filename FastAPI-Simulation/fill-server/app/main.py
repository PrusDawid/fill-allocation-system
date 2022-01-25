import uvicorn
from fastapi import FastAPI
import httpx
import asyncio
import random
import simplejson as json


app = FastAPI()  # initialize FastAPI application


pass_dict = ['AXA', 'AMD', 'MSFT', 'TSLA', 'NVDA',
             'AAPL', 'GOOG', 'FB', 'NFLX', 'INTC', 'PYPL']


@app.on_event('startup')
async def make_stock_call():
    while 1:

        tmp_obj = {'ticker': random.choice(pass_dict),
                   'price': round(random.uniform(1.0, 999.9), 2),
                   'quantity': random.randrange(1, 999)}
        await asyncio.sleep(random.randint(1, 5))  # Async Sleep
        async with httpx.AsyncClient() as client:
            r = await client.post('http://controller-server:8000/stock',
                                  data=json.dumps(tmp_obj))

if __name__ == "__main__":
    uvicorn.run("main:app", port=8082, reload=True)

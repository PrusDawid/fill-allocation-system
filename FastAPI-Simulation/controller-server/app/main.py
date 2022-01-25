import uvicorn
import httpx

from fastapi import FastAPI
from fastapi_utils import tasks

import pandas as pd

from .models.models import AccountOperationList, PostResponse, StockOperation
from .db.fake_db import Accounts, Positions, StockVal

app = FastAPI()  # initialize FastAPI application

stock_db = StockVal()
account_db = Accounts()
positions_db = Positions()


@app.post('/stock', response_model=PostResponse)
async def post_stock(stock: StockOperation):
    '''
    POST method to append stock value data to database

    stock: StockOperation
    return: PostResponse 
    '''
    fk_tmp = pd.DataFrame({
        'ticker': [stock.ticker],
        'price': [stock.price],
        'quantity': [stock.quantity],
        'total': [stock.price*stock.quantity]})
    stock_db.append(fk_tmp)
    total_filter = stock_db.db[(stock_db.db.ticker == stock.ticker)]
    positions_db.compute(account_db.accounts, stock,
                         total_filter.sum()['total'])
    return {'success': True}


@app.post('/accounts')
async def post_accounts(accounts: AccountOperationList):

    account_db.add_accounts(accounts.accounts)


@app.on_event('startup')
@tasks.repeat_every(seconds=10)
async def send_data():

    async with httpx.AsyncClient() as client:
        r = await client.post('http://position-server:8000/position',
                              data=positions_db.db.to_json())


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)

import uvicorn
from fastapi import FastAPI
from fastapi_utils import tasks
import httpx
import random
import simplejson as json

MAX_NUMBER_OF_ACCOUNTS_GENERATED = 10

app = FastAPI()  # initialize FastAPI application


async def accounts():

    # Max accounts numbers, can be changed.
    rand_numb = random.randint(1, MAX_NUMBER_OF_ACCOUNTS_GENERATED)
    r = [random.uniform(1.0, 999999.9) for i in range(rand_numb)]
    s = sum(r)
    r = [(i/s)*100 for i in r]
    # Return in format needed by task -> accountn: x%
    accounts = list(({"account": f"account{pos}", "percent": f"{round(v,2)}%"})
                    for pos, v in enumerate(r))
    return json.dumps({"accounts": accounts})


@app.on_event('startup')
@tasks.repeat_every(seconds=30)
async def make_stock_call():

    val = await accounts()
    async with httpx.AsyncClient() as client:
        r = await client.post('http://controller-server:8000/accounts',
                              data=val)
if __name__ == "__main__":
    uvicorn.run("main:app", port=8088, reload=True)

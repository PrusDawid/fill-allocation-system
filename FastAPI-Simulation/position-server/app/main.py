import uvicorn
from fastapi import FastAPI
import pandas as pd


app = FastAPI()  # initialize FastAPI application


@app.post('/position')
async def print_data(data: dict):
    
    # Map to DataFrame for better visibility of data
    df_data =pd.DataFrame(data)
    print(df_data)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8089, reload=True)

from typing import List, Literal, Optional
from pydantic import BaseModel, validator

# * Stocks Models


class StockOperation(BaseModel):
    '''
    Validate input of Stock 
    '''
    ticker: Literal['AXA', 'AMD', 'MSFT', 'TSLA', 'NVDA',
                    'AAPL', 'GOOG', 'FB', 'NFLX', 'INTC', 'PYPL']
    price: float
    quantity: int
    total: float

    def __init__(__pydantic_self__, price: float, quantity: int, **data):
        super().__init__(total=round(price*quantity, 2),
                         price=price, quantity=quantity, **data)

    @validator('price')
    def price_positive(cls, v: float):
        return abs(v)

    @validator('quantity')
    def quantity_positive(cls, v: int):
        return abs(v)

# * Accounts Models


class AccountOperation(BaseModel):
    '''

    '''
    account: str
    percent: float

    def __init__(__pydantic_self__, account: str, percent: str):
        if not type(percent) is str:
            raise TypeError(
                f"Percent {percent} ({type(percent)} should be 'str' )")
        if not percent[-1] == '%':
            raise ValueError(
                f"Percent {percent} should have '%' sign at the end of string")
        perc_str = percent[:-1]
        super().__init__(account=account, percent=round(float(perc_str), 2))


class AccountOperationList(BaseModel):
    accounts: List[AccountOperation]

    @validator('accounts')
    def check_full(cls, v: List[AccountOperation]):
        # Due to the round of percent some of requests will not pass the validator
        if sum(round(i.percent) for i in v) != 100:
            raise ValueError(
                f"Sum of accounts {sum(round(i.percent) for i in v)} percents is not equal to 100%")
        return v

# * Support Models


class PostResponse(BaseModel):
    success: bool
    msg: Optional[str]

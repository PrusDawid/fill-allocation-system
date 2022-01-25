from typing import List
import pandas as pd

from ..models.models import AccountOperation, StockOperation

pass_dict = ['account', 'AXA_quant', 'AXA_tval', 'AMD_quant', 'AMD_tval', 'MSFT_quant', 'MSFT_tval', 'TSLA_quant', 'TSLA_tval', 'NVDA_quant', 'NVDA_tval',
             'AAPL_quant', 'AAPL_tval', 'GOOG_quant', 'GOOG_tval', 'FB_quant', 'FB_tval', 'NFLX_quant', 'NFLX_tval', 'INTC_quant', 'INTC_tval', 'PYPL_quant', 'PYPL_tval']


class StockVal:
    def __init__(self):
        self.db = pd.DataFrame({
            'ticker': [],
            'price': [],
            'quantity': [],
            'total': []
        })

    def append(self, val: dict):
        self.db = self.db.append(val, ignore_index=True)

    def retrieve_index(self, ind: str):
        return self.db.loc[ind]

    def filter_tickers(self, key: str):
        return self.db[(self.db.ticker == key)]

    def drop_indexes(self, indexes: List[int]):
        self.db = self.db.drop(indexes)


class Accounts:
    def __init__(self):
        self.accounts: List[AccountOperation] = []
        
    def add_accounts(self, acc: List[AccountOperation]):
        self.accounts = acc


class Positions:
    def __init__(self):
        self.db = pd.DataFrame(columns=pass_dict)

    def compute(self, accounts: List[AccountOperation], stock: StockOperation, total_sum: float):

        for acc in accounts:
            val_column = f"{stock.ticker}_tval"
            quant_column = f"{stock.ticker}_quant"

            acc_filter = self.db[(self.db.account == acc.account)]
            account_total = acc_filter.sum()[val_column]
            math_percent = acc.percent*0.01
            align_val = total_sum*math_percent
            needed_val = align_val-account_total
            quants_to_acc = abs(round(needed_val/stock.price, 0))
            value_to_acc = quants_to_acc*stock.price
            
            self.db = self.db.append({
                'account': acc.account,
                val_column: value_to_acc,
                quant_column: quants_to_acc}, ignore_index=True)
            
            self.db = self.db.groupby(['account'], as_index=False).agg('sum')


class StockValue:

    def __init__(self):
        self.db = []

    def __str__(self):
        return pd.DataFrame(self.db, columns=['ticker', 'price', 'quantity']).to_string()

    def add(self, ticker: str, price: float, quantity: int):
        self.db.append(
            {'ticker': ticker, 'price': price, 'quantity': quantity})

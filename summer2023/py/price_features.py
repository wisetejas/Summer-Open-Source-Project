#%%
from datetime import datetime
import numpy as np
import pandas as pd

#%%
def get_price(df:pd.DataFrame, outlier_cutoff = 0.01) -> pd.DataFrame:
    monthly_prices = df.loc[:, "close"].unstack("ticker")
    data = pd.DataFrame()
    lags = [1, 2, 3, 6, 9, 12]
    for lag in lags:
        data[f'return_{lag}m'] = (monthly_prices
                            .pct_change(lag)
                            .stack()
                            .pipe(lambda x: x.clip(lower=x.quantile(outlier_cutoff),
                            upper=x.quantile(1-outlier_cutoff)))
                            .add(1)
                            .pow(1/lag)
                            .sub(1)
                            )
    data = data.swaplevel()
    out = df.join(data)
    return(out)

#%%

def format_schema_price(data: pd.DataFrame) -> pd.DataFrame:    
    data = data.reset_index()
    cnames = list(data.columns)
    cnames = [x.lower().replace(" ", "_").replace("%", "")\
        for x in cnames]
    data.columns = cnames
    data = data.rename(columns = {"symbol": "ticker"})
    ##########
    #Make sure ticker date combination is unique
    data = data.drop_duplicates(subset = ["date", "ticker"])
    #Create index
    data = data.set_index(keys = ["date", "ticker"])
    return(data)

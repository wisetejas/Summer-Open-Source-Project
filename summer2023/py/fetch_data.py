#%%
import pandas as pd
import yfinance as yf
# %%
def get_price(symbols, start_date, end_date, interval = "1mo") -> pd.DataFrame:
    df = (yf
        .download(symbols,
                  group_by='Ticker',
                  start = start_date,
                  end = end_date,
                  interval = interval,
                  keepna = True,
                  actions = True

                  )
        )
    df = (
        df.stack(level=0)
        .rename_axis(['Date', 'Ticker'])
        .reset_index(level=1)
    )
    return(df)
# %%

#%%
import os,sys
import warnings
warnings.filterwarnings('ignore')

#%%
# Load Modules
from datetime import datetime
from py.price_features import *
from py.fetch_data import *
from py.stock_selection import *
# %%
print("starting work with base dir {}".format(os.getcwd()))
%load_ext autoreload
%autoreload 2
# %%
fpath = "data/index/ind_nifty200list.csv"
index200 = pd.read_csv(fpath)
# %%
index200 = index200.assign(
    nse_ticker = index200.Symbol.apply(lambda x: x + ".NS")
)
index200_tickers = index200.nse_ticker.to_list()
# %%
# Now fetch the data 
# Change start date
start_date = datetime(2012, 6, 13)
end_date = datetime.today()
index200_price = get_price(index200_tickers, start_date, end_date)
# %%
# Save file in parquet format
tstamp = datetime.today().strftime("%Y%m%d")
out_file = "data/index200_price{}.parquet".format(tstamp)
index200_price.to_parquet(out_file)
# %%

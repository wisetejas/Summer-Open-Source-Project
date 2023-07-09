# %%
import numpy as np
import pandas as pd
# %%

#Calculate 12 month, 6 month Momentum ratio(MR)
def calc_12_mon_momentum(df:pd.DataFrame) -> pd.DataFrame:
    df['12_Mon-Return'] = (df['Price'].shift(1)/df['Price'].shift(13)-1)
    df['log_Returns'] = np.log(1+df['Returns'])
    df['annualized_std_dev'] = df['log_Returns'].rolling(window=12).std() *np.sqrt(12) #calculating monthly std dev instead of daily
    df['MR_12'] = df['12_Mon-Return'] / df['annualized_std_dev']
    return df
# %%

def calc_6_mon_momentum(df:pd.DataFrame) -> pd.DataFrame:
    df['6_Mon-Return']=(df['Price'].shift(1)/df['Price'].shift(7)-1)
    df['log_Returns']=np.log(1+df['Returns'])
    df['annualized_std_dev']=df['log_Returns'].rolling(window=12).std() *np.sqrt(12) #calculating monthly std dev instead of daily
    df['MR_6']=df['6_Mon-Return']/df['annualized_std_dev']
    return df
# %%

def calc_12_mon_z_score(df:pd.DataFrame) -> pd.DataFrame:
    mean_MR_12=df['MR_12'].mean()
    std_MR_12=df['MR_12'].std()
    df['z-sc_MR-12'] = (df['MR_12'] - mean_MR_12) / std_MR_12
    return df
# %%

def calc_6_mon_z_score(df:pd.DataFrame) -> pd.DataFrame:
    mean_MR_6=df['MR_6'].mean()
    std_MR_6=df['MR_6'].std()
    df['z-sc_MR-6']=(df['MR_6'] - mean_MR_6) / std_MR_6
    return df
# %%

def normalized_momentum_score(df:pd.DataFrame) -> pd.DataFrame:
    df['weighted_avg_z-sc']=0.5*df['z-sc_MR-12'] + 0.5*df['z-sc_MR-6']
    df['norm_Mom-sc']=np.where(df['weighted_avg_z-sc']>=0,[(1+df['weighted_avg_z-sc']), 1/(1+df['weighted_avg_z-sc'])])
    return df
# %%

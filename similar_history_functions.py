import numpy as np

def RngCalc(series):
    """Returns the maximum range of a series."""
    return series.max() - series.min()

def RngMin(value_in_series, series):
    """Returns value (which is any value in the series) - the series minimum"""
    return value_in_series - series.min()

def PctDistribution(value_in_series, series):
    """Returns % to reflect ranking within the historic range in series"""
    return RngMin(value_in_series, series) / RngCalc(series)

def PctDistArray(df):
    """Returns the same df, but with % to reflect the ranking for each value within its given series"""
    for colName in df.columns:
        df[colName] = df.apply(lambda row: PctDistribution(row[colName], df[colName]), axis=1)
    return df.dropna(how='all')

def similaritySeries(df, mean_or_last='last'):
    """Returns a series with a % value that represents the similarity of either the last or mean values for the
    dataframe (mean_or_last)"""
    df_pct = PctDistArray(df)
    if mean_or_last == 'last':
        compare_series = df_pct.iloc[-1]
        df_pct = df_pct.iloc[:-1]
    elif mean_or_last == 'mean':
        compare_series = df_pct.mean(axis=0)
    else:
        print (f"{mean_or_last} is not a valid entry for the mean_or_last field")
        return

    delta_df = df_pct - compare_series
    norm_df = delta_df.apply(np.linalg.norm, axis=1)
    return norm_df

def getSimilarRecord(df, mean_or_last='last'):
    """Returns the most similar row the either the last or the mean of a dataframe."""
    norm_series = similaritySeries(df, mean_or_last)
    return df.loc[norm_series.idxmin()]

# FSA Crop Acreage Data

Hey all, I went ahead and brought the FSA data toghether for you all. As a warning, all the years together are 11,508,905 rows, so I chunked it up by year and stored it as a parquuet.

I stored it as parquet because GitHub has storage rules, and also this data is so big you need a more efficient data storage method than csv (for context, stored as a csv this data is 1.17 gigabytes vs. .2 gigabytes as parquet)


## How to Read This Data

Reading parquet from GitHub is basically the same as csv, except you use the read parquet function in pandas. See example below

'''
import pandas as pd

df_2012 = pd.read_parquet('https://github.com/JackOgozaly/Hurricane_Crop_Acreage/blob/main/Data/Crop_Data/df_2012.parquet.gzip?raw=true')

'''




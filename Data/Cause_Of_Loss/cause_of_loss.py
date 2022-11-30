#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 19:21:16 2022

@author: jackogozaly
"""

import pandas as pd
import numpy as np


#https://www.rma.usda.gov/en/Information-Tools/Summary-of-Business/Cause-of-Loss


cols = ['commodity_year_identifier',
        'state_code', 'state_abbreviation', 'county_code',
        'county_name', 'commodity_code', 'commodity_name', 'insurance_plan_code',
        'insurance_plan_name_abbreviation', 'coverage_category', 'stage_code',
        'cause_of_loss_code', 'cause_of_loss_description', 'month_of_loss',
        'month_of_loss_name', 'year_of_loss', 'policies_earning_premium',
        'policies_identified', 'net_planted_quantity', 'net_endorsed_acres',
        'liability', 'total_premium', 'producer_paid_premium', 
        'subsidy', 'state/private_subsidy', 'additional_subsidy', 'efa_premium_discount',
        'net_determined_quantity',
        'indemnity_amount', 'loss_ratio']

df_list = []

for i in range(2001, 2023):
    df = pd.read_csv(f'/Users/jackogozaly/Desktop/Python_Directory/Hurricane/Data/loss_data/colsom_{i}.zip', 
                           delimiter='|',  header=None, low_memory=False)

    df.columns = cols
    df_list.append(df)


total_df = pd.concat(df_list)

df_obj = total_df.select_dtypes(['object'])
total_df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

total_df['state_code'] = total_df['state_code'].astype(str).str.pad(width=2, side='left', fillchar= '0')
total_df['county_code'] = total_df['county_code'].astype(str).str.pad(width=3, side='left', fillchar= '0')
total_df['GEOID'] = total_df['state_code'] + total_df['county_code']
total_df = total_df.drop(['state_abbreviation', 'county_name', 'month_of_loss_name'], axis=1)

final_df = np.array_split(total_df, 6)

for i in range(len(final_df)):
    final_df[i].to_parquet(f'/Users/jackogozaly/Desktop/Python_Directory/Hurricane/Data/loss_data/crop_loss_data_{i}.parquet.gzip', index=None)


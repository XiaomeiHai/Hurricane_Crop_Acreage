# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
print(pd.__version__)
import numpy as np
import os
import seaborn as sns

cause_of_loss_0 = pd.read_parquet('https://github.com/JackOgozaly/Hurricane_Crop_Acreage/blob/main/Data/Cause_Of_Loss/crop_loss_data_0.parquet.gzip?raw=true')

print(cause_of_loss_0)

dff = cause_of_loss_0[(cause_of_loss_0["stage_code"]=="FL")]

cause_of_loss_0.columns #Print the column labels of the DataFrame.

cause_of_loss_0.info(verbose=True, show_counts=True) #Print a concise summary of a DataFrame.

cause_of_loss_0.index #The index (row labels) of the DataFrame.

cause_of_loss_0.isna().sum() #calculate null value in the dataset

for_plot = cause_of_loss_0.commodity_name.value_counts()
for_plot = pd.DataFrame(for_plot)
for_plot = for_plot[for_plot["commodity_name"]>10000]
sns.set(rc={'figure.figsize':(20,10)})
sns.barplot(x=for_plot.index, y = for_plot["commodity_name"])

#analyze which crop has the biggest acre of grow and present it as a figure
#doubts: how to determine the range of y axis? I just choose > 10000 to make the graphic more readable but I am not sure if this is proper


sns.set_theme(style="darkgrid")
df = cause_of_loss_0
sns.displot(
    df, x="commodity_year_identifier", col="commodity_name", row="producer_paid_premium",
    binwidth=4, height=4, facet_kws=dict(margin_titles=True),
)

#doubts: I want to create a line chart presesnting the change by time of insurance investments in different crops




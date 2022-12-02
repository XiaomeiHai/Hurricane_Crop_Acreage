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

for_plot = cause_of_loss_0.commodity_name.value_counts()
for_plot = pd.DataFrame(for_plot)
for_plot = for_plot[for_plot["commodity_name"]>10000]
sns.set(rc={'figure.figsize':(20,10)})
sns.barplot(x=for_plot.index, y = for_plot["commodity_name"])



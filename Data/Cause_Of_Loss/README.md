# Cause of Loss Data

Hey all, I cleaned and combined all the cause of loss together for you all. I chunked it up so GitHub would accept the upload (total size combined is 2.8 million rows.

If you want to know more about cause of loss, go here: https://www.rma.usda.gov/SummaryOfBusiness/CauseOfLoss


# How to read the data into python

Same deal as before, the data is stored as a parquet and can be read in as such:

```
import pandas as pd

cause_of_loss_0 = pd.read_parquet('https://github.com/JackOgozaly/Hurricane_Crop_Acreage/blob/main/Data/Cause_Of_Loss/crop_loss_data_0.parquet.gzip?raw=true')

```

Oh, if you might need to install pyarrow. See link below for details. https://arrow.apache.org/docs/python/install.html

'''
This script transforms historical hurricane data into a more usable format

How to Interpert This Data:
https://www.nhc.noaa.gov/data/hurdat/hurdat2-format-atl-1851-2021.pdf

NOAA Data Site:
https://www.nhc.noaa.gov/data/#hurdat
'''

import pandas as pd
import numpy as np


#Read in our data
df = pd.read_csv(r'https://www.nhc.noaa.gov/data/hurdat/hurdat2-1851-2021-100522.txt')

#Save the misplaced column values
col_vals = list(df.columns)[0:3]

#Reset our index but keep the columns
df = df.reset_index(drop=False)

#Concat our tables together
data = []
data.insert(0, {'level_0': col_vals[0], 'level_1': col_vals[1], 'level_2': col_vals[2]})
df = pd.concat([pd.DataFrame(data), df], ignore_index=True)

#The raw version of this data comes in such that every cyclone is
#Essentially a sub table within the df. We want to create a tidy dataframe,
#So we'll go through, extract sub-df, append a column signifying the storm, and then
#We will concat it together

#Create an index of where every sub-table starts
df_index = list(df[df['level_0'].str.startswith('AL')].index)

#Empty list for us to store our dataframes in
df_list = []
#Loop through, slice the dataframe for the sub-table rows, and make the table tidy
for i in range(len(df_index)):
    if i < len(df_index)-1:
        sub_df = df.iloc[df_index[i]:df_index[i+1]-1,].reset_index(drop=True)
    else:
        sub_df = df.iloc[df_index[i]:,:].reset_index(drop=True)
    
    #Add the header values as tidy column values
    sub_df['ID'] = sub_df.iloc[0, 0]
    sub_df['Name'] = sub_df.iloc[0, 1].strip()
    sub_df['num_best_track_entries'] = sub_df.iloc[0, 2]
    #Get rid of the header row now
    sub_df = sub_df.iloc[1:, :]
    #Append our dataframe to our list
    df_list.append(sub_df)


#Concat our values back into one table
df = pd.concat(df_list)

df.columns = ['ymd', 'minutes', 'record_identifier', 'status_of_system',
              'latitude', 'longitude', 
              'max_sustained_wind', 'max_pressure', 
              '34kt_wind_radii_NE_quad', '34kt_wind_radii_SE_quad', '34kt_wind_radii_SW_qud', '34kt_wind_radii_NW_qud',
              '50kt_wind_radii_NE_quad', '50kt_wind_radii_SE_quad', '50kt_wind_radii_SW_qud', '50kt_wind_radii_NW_qud',
              '64kt_wind_radii_NE_quad', '64kt_wind_radii_SE_quad', '64kt_wind_radii_SW_qud', '64kt_wind_radii_NW_qud',
              'radius_max_wind', 'id', 'name', 'num_best_track_entries']

#NOAA classifies null values with these values, so we'll just replace them with null
df = df.replace(-999, np.nan)
df = df.replace(-99, np.nan)


#Make a datetime column by combining the ymd column and minutes
df['date'] = df['ymd'].str[:4] + '-' + df['ymd'].str[4:6] + '-' + df['ymd'].str[6:] + ' ' + df['minutes'].str[:3] + ':' + df['minutes'].str[3:]
df['date'] = pd.to_datetime(df['date'])


#Create a hemisphere value
df['hemishphere_east_west'] = np.where(df["longitude"].str.contains('E'), 
                             'Eastern', 'Western')
df['hemishphere_north_south'] = np.where(df["latitude"].str.contains('N'), 
                             'North', 'South')


#Fix lat and long
df["longitude"] = df["longitude"].str.replace('E', '', regex=False)
df["longitude"] = df["longitude"].str.replace('W', '', regex=False)
df["longitude"] = pd.to_numeric(df["longitude"])
df["latitude"] = df["latitude"].str.replace('N', '', regex=False)
df["latitude"] = df["latitude"].str.replace('S', '', regex=False)
df["latitude"] = pd.to_numeric(df["latitude"])
#Convert the normal values to negative or positive depending on hemisphere
df['longitude'] = np.where(df['hemishphere_east_west'] == 'Western',
                          df["longitude"] *-1, df["longitude"])

df['latitude'] = np.where(df['hemishphere_north_south'] == 'South',
                          df["latitude"] *-1, df["latitude"])


#Remap the record identifier so it's a text description
record_identifier_remap = {'C':'Closest approach to a coast, not followed by a landfall',
                           'G': 'Genesis',
                           'I': 'An intensity peak in terms of both pressure and wind',
                           'L': 'Landfall (center of system crossing a coastline)',
                           'P': 'Minimum in central pressure',
                           'R': 'Provides additional detail on the intensity of the cyclone when rapid changes are underway',
                           'S': 'Change of status of the system',
                           'T': 'Provides additional detail on the track (position) of the cyclone',
                           'W': 'Maximum sustained wind speed '}
#Do the reamp
df['record_identifier_desc'] = df['record_identifier'].str.strip().replace(record_identifier_remap)


#Remape status system into a text description
status_system_remap = {'TD': 'Tropical cyclone of tropical depression intensity (< 34 knots)',
                       'TS': 'TS – Tropical cyclone of tropical storm intensity (34-63 knots)',
                       'HU': 'HU – Tropical cyclone of hurricane intensity (> 64 knots)',
                       'EX': 'EX – Extratropical cyclone (of any intensity)',
                       'SD': 'Subtropical cyclone of subtropical depression intensity (< 34 knots)',
                       'SS': 'SS – Subtropical cyclone of subtropical storm intensity (> 34 knots)',
                       'LO': 'A low that is neither a tropical cyclone, a subtropical cyclone, nor an extratropical cyclone (of any intensity)',
                       'WV': 'Tropical Wave (of any intensity)',
                       'DB': 'Disturbance (of any intensity)'}
                       
#Do the remap
df['status_of_system_desc'] = df['status_of_system'].str.strip().replace(status_system_remap)

#Rearrange our columns
df = df[['name', 'date', 'id', 'status_of_system_desc', 'record_identifier_desc',
         'latitude', 'longitude', 'max_sustained_wind', 'max_pressure', 
         '34kt_wind_radii_NE_quad', '34kt_wind_radii_SE_quad', '34kt_wind_radii_SW_qud', '34kt_wind_radii_NW_qud',
         '50kt_wind_radii_NE_quad', '50kt_wind_radii_SE_quad', '50kt_wind_radii_SW_qud', '50kt_wind_radii_NW_qud',
         '64kt_wind_radii_NE_quad', '64kt_wind_radii_SE_quad', '64kt_wind_radii_SW_qud', '64kt_wind_radii_NW_qud',
         'radius_max_wind', 'ymd', 'minutes', 'num_best_track_entries',
         'status_of_system', 'record_identifier', 'hemishphere_east_west', 'hemishphere_north_south']]

#Write to csv
df.to_csv(r'/Users/jackogozaly/Desktop/Python_Directory/Hurricane/historical_hurricane_date.csv',
          index=False)



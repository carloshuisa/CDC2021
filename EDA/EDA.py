# Load libraries
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import missingno as msno

# Define working directory
os.chdir('C:/Users/james/OneDrive/Desktop/Coding/Jupyter Notebook/cdc_datasets/social science')

# Import original data (csv file)
svi = pd.read_csv('svi.csv')

# Read in data
svi.head()

# Statistic summary for continuous variables
svi.describe()

# Check null values, data type, and unique values in each column
null = svi.isnull().sum().to_frame(name='nulls').T
dtype = svi.dtypes.to_frame(name='dtypes').T
nunique = svi.nunique().to_frame(name='unique').T
pd.concat([null, dtype, nunique], axis=0)

# Check value of -999
svi[svi.eq(-999).any(1)]

# Update dataset by changing -999 to 0 
svi = svi.replace([-999], 0)

# Check conversion
svi[svi.eq(-999).any(1)]


#2. Subset dataset into each theme
# (1) Socioeconomics (Theme 1)
svi_soc = svi.loc[:, ['ST_ABBR', 'COUNTY', 'LOCATION', 'AREA_SQMI', 'E_TOTPOP', 'E_HU', 'E_HH', 
                     'E_POV', 'E_UNEMP', 'E_PCI', 'E_NOHSDP',
                     'EP_POV', 'EP_UNEMP', 'EP_PCI', 'EP_NOHSDP', 
                     'EPL_POV', 'EPL_UNEMP', 'EPL_PCI', 'EPL_NOHSDP',
                     'SPL_THEME1', 'RPL_THEME1',
                     'F_POV', 'F_UNEMP', 'F_PCI', 'F_NOHSDP', 'F_THEME1']]

# Filter by NC
svi_soc_nc = svi_soc.loc[svi_soc['ST_ABBR'] == 'NC']
svi_soc_nc.head()

# Compute sum of each flag category
sums = [('F_POV', svi_soc_nc["F_POV"].sum()),
        ('F_UNEMP', svi_soc_nc["F_UNEMP"].sum()),
        ('F_PCI', svi_soc_nc['F_PCI'].sum()),
        ('F_NOHSDP', svi_soc_nc['F_NOHSDP'].sum())]

df_ft1 = pd.DataFrame(sums, columns = ['category', 'total'])

# Compute percentage of each flag category
pct = [(svi_soc_nc["F_POV"].sum()/svi_soc_nc['F_THEME1'].sum())*100,
       (svi_soc_nc["F_UNEMP"].sum()/svi_soc_nc['F_THEME1'].sum())*100,
       (svi_soc_nc["F_PCI"].sum()/svi_soc_nc['F_THEME1'].sum())*100,
       (svi_soc_nc["F_NOHSDP"].sum()/svi_soc_nc['F_THEME1'].sum())*100]


# (2) Household Composition / Disability (Theme 2)
svi_hcd = svi.loc[:, ['ST_ABBR', 'COUNTY', 'LOCATION', 'AREA_SQMI', 'E_TOTPOP', 'E_HU', 'E_HH', 
                     'E_AGE65', 'E_AGE17', 'E_DISABL', 'E_SNGPNT',
                     'EP_AGE65', 'EP_AGE17', 'EP_DISABL', 'EP_SNGPNT',
                     'EPL_AGE65', 'EPL_AGE17', 'EPL_DISABL', 'EPL_SNGPNT',
                     'SPL_THEME2', 'RPL_THEME2',
                     'F_AGE65', 'F_AGE17', 'F_DISABL', 'F_SNGPNT', 'F_THEME2']]

# Filter by NC
svi_hcd_nc = svi_hcd.loc[svi_hcd['ST_ABBR'] == 'NC']
svi_hcd_nc.head()
df_ft1["percent"] = [round(num, 2) for num in pct]
df_ft1

# Barplot - total percentage of each category across NC 
fig = px.bar(df_ft1, x = 'category', y = 'percent', color = 'category', title = '% of flag category in SOC across NC')
fig.show()

# Group dataset by county and compute sum of flags for each county
df_ft1_cty = svi_soc_nc.groupby('COUNTY').agg({'F_POV':'sum', 'F_UNEMP':'sum', 
                                               'F_PCI':'sum', 'F_NOHSDP':'sum', 
                                               'F_THEME1':'sum'})

df_ft1_cty = df_ft1_cty.loc[df_ft1_cty['F_THEME1'] != 0]
df_ft1_cty.index.name = 'County'
df_ft1_cty.reset_index(inplace = True)

ft1_srt = df_ft1_cty.sort_values(by = ['F_THEME1', 'F_UNEMP'], ascending = [False, False]).head(n = 10)
ft1_srt

# Barplot - Top 10 Counties by number of flags for Theme 1
fig = px.bar(ft1_srt, x = 'County', y = 'F_THEME1', color = 'County', title = 'Top 10 Counties in NC')
fig.show()

# Compute sum of each flag category
sums = [('F_AGE65', svi_hcd_nc["F_AGE65"].sum()),
        ('F_AGE17', svi_hcd_nc["F_AGE17"].sum()),
        ('F_DISABL', svi_hcd_nc['F_DISABL'].sum()),
        ('F_SNGPNT', svi_hcd_nc['F_SNGPNT'].sum())]

df_ft2 = pd.DataFrame(sums, columns = ['category', 'total'])

# Compute percentage of each flag category
pct = [(svi_hcd_nc["F_AGE65"].sum()/svi_hcd_nc['F_THEME2'].sum())*100,
       (svi_hcd_nc["F_AGE17"].sum()/svi_hcd_nc['F_THEME2'].sum())*100,
       (svi_hcd_nc["F_DISABL"].sum()/svi_hcd_nc['F_THEME2'].sum())*100,
       (svi_hcd_nc["F_SNGPNT"].sum()/svi_hcd_nc['F_THEME2'].sum())*100]

df_ft2["percent"] = [round(num, 2) for num in pct]
df_ft2

# Barplot - Total percentage of each category across NC 
fig = px.bar(df_ft2, x = 'category', y = 'percent', color = 'category', title = '% of flag category in HCD across NC')
fig.show()

# Group dataset by county and compute sum of flags for each county
df_ft2_cty = svi_hcd_nc.groupby('COUNTY').agg({'F_AGE65':'sum', 'F_AGE17':'sum', 
                                               'F_DISABL':'sum', 'F_SNGPNT':'sum', 
                                               'F_THEME2':'sum'})

df_ft2_cty = df_ft2_cty.loc[df_ft2_cty['F_THEME2'] != 0]
df_ft2_cty.index.name = 'County'
df_ft2_cty.reset_index(inplace = True)

ft2_srt = df_ft2_cty.sort_values(by = ['F_THEME2', 'F_DISABL'], ascending = [False, False]).head(n = 10)
ft2_srt

# Barplot - Top 10 counties by Number of Flags for Theme 2
fig = px.bar(ft2_srt, x = 'County', y = 'F_THEME2', color = 'County', title = 'Top 10 Counties in NC')
fig.show()


# (3) Minority Status / Language (Theme 3)
svi_ml = svi.loc[:, ['ST_ABBR', 'COUNTY', 'LOCATION', 'AREA_SQMI', 'E_TOTPOP', 'E_HU', 'E_HH', 
                     'E_MINRTY', 'E_LIMENG', 
                     'EP_MINRTY', 'EP_LIMENG', 
                     'EPL_MINRTY', 'EPL_LIMENG',
                     'SPL_THEME3', 'RPL_THEME3',
                     'F_MINRTY', 'F_LIMENG', 'F_THEME3']]

svi_ml_nc = svi_ml.loc[svi_ml['ST_ABBR'] == 'NC']
svi_ml_nc.head()

# Compute sum of each flag category
sums = [('F_MINRTY', svi_ml_nc["F_MINRTY"].sum()),
        ('F_LIMENG', svi_ml_nc["F_LIMENG"].sum())]

df_ft3 = pd.DataFrame(sums, columns = ['category', 'total'])

# Compute percentage of each flag category
pct = [(svi_ml_nc["F_MINRTY"].sum()/svi_ml_nc['F_THEME3'].sum())*100,
       (svi_ml_nc["F_LIMENG"].sum()/svi_ml_nc['F_THEME3'].sum())*100]

df_ft3["percent"] = [round(num, 2) for num in pct]
df_ft3['percent'].sum()
df_ft3

# Barplot - total percentage of each category across NC 
fig = px.bar(df_ft3, x = 'category', y = 'percent', color = 'category', title = '% of flag category in ML across NC')
fig.show()

# Group dataset by county and compute sum of flags for each county
df_ft3_cty = svi_ml_nc.groupby('COUNTY').agg({'F_MINRTY':'sum', 'F_LIMENG':'sum', 'F_THEME3':'sum'})

df_ft3_cty = df_ft3_cty.loc[df_ft3_cty['F_THEME3'] != 0]
df_ft3_cty.index.name = 'County'
df_ft3_cty.reset_index(inplace = True)

ft3_srt = df_ft3_cty.sort_values(by = 'F_THEME3', ascending = False).head(n = 10)
ft3_srt

# Barplot - Top 10 counties by Number of Flags for Theme 3
fig = px.bar(ft3_srt, x = 'County', y = 'F_THEME3', color = 'County', title = 'Top 10 counties in NC')
fig.show()

# (4) Housing / Transportation (Theme 4)
svi_ht = svi.loc[:, ['ST_ABBR', 'COUNTY', 'LOCATION', 'AREA_SQMI', 'E_TOTPOP', 'E_HU', 'E_HH', 
                     'E_MUNIT', 'E_MOBILE', 'E_CROWD', 'E_NOVEH', 'E_GROUPQ', 
                     'EP_MUNIT', 'EP_MOBILE', 'EP_CROWD', 'EP_NOVEH', 'EP_GROUPQ',
                     'EPL_MUNIT', 'EPL_MOBILE', 'EPL_CROWD', 'EPL_NOVEH', 'EPL_GROUPQ',
                     'SPL_THEME4', 'RPL_THEME4',
                     'F_MUNIT', 'F_MOBILE', 'F_CROWD', 'F_NOVEH', 'F_GROUPQ', 'F_THEME4']]

svi_ht_nc = svi_ht[svi_ht['ST_ABBR'] == 'NC']
svi_ht_nc.head()

# Compute sum of each flag category
sums = [('F_MUNIT', svi_ht_nc['F_MUNIT'].sum()),
        ('F_MOBILE', svi_ht_nc['F_MOBILE'].sum()),
        ('F_CROWD', svi_ht_nc['F_CROWD'].sum()),
        ('F_NOVEH', svi_ht_nc['F_NOVEH'].sum()),
        ('F_GROUPQ', svi_ht_nc['F_GROUPQ'].sum())]

df_ft4 = pd.DataFrame(sums, columns = ['category', 'total'])

# Compute percentage of each flag category
pct = [(svi_ht_nc['F_MUNIT'].sum()/svi_ht_nc['F_THEME4'].sum())*100,
       (svi_ht_nc['F_MOBILE'].sum()/svi_ht_nc['F_THEME4'].sum())*100,
       (svi_ht_nc['F_CROWD'].sum()/svi_ht_nc['F_THEME4'].sum())*100,
       (svi_ht_nc['F_NOVEH'].sum()/svi_ht_nc['F_THEME4'].sum())*100,
       (svi_ht_nc['F_GROUPQ'].sum()/svi_ht_nc['F_THEME4'].sum())*100]

df_ft4["percent"] = [round(num, 2) for num in pct]
df_ft4['percent'].sum()
df_ft4

# Barplot - Total percentage of each category across NC 
fig = px.bar(df_ft4, x = 'category', y = 'percent', color = 'category', title = '% of flag category in HT across NC')
fig.show()

# Group dataset by county and compute sum of flags for each county
df_ft4_cty = svi_ht_nc.groupby('COUNTY').agg({'F_MUNIT':'sum', 'F_MOBILE':'sum', 
                                              'F_CROWD':'sum', 'F_NOVEH':'sum',
                                              'F_GROUPQ':'sum', 'F_THEME4':'sum'})

df_ft4_cty = df_ft4_cty.loc[df_ft4_cty['F_THEME4'] != 0]
df_ft4_cty.index.name = 'County'
df_ft4_cty.reset_index(inplace = True)

ft4_srt = df_ft4_cty.sort_values(by = 'F_THEME4', ascending = False).head(n = 10)
ft4_srt

# Barplot - Top 10 counties by Number of Flags for Theme 3
fig = px.bar(ft4_srt, x = 'County', y = 'F_THEME4', color = 'County', title = 'Top 10 counties in NC')
fig.show()


# Combine all F_ variables
svi_fvars = svi.loc[:, ['ST_ABBR', 'COUNTY', 'LOCATION', 'AREA_SQMI', 'E_TOTPOP', 'E_HU', 'E_HH',
                        'F_POV', 'F_UNEMP', 'F_PCI', 'F_NOHSDP', 'F_THEME1',
                        'F_AGE65', 'F_AGE17', 'F_DISABL', 'F_SNGPNT', 'F_THEME2',
                        'F_MINRTY', 'F_LIMENG', 'F_THEME3',
                        'F_MUNIT', 'F_MOBILE', 'F_CROWD', 'F_NOVEH', 'F_GROUPQ', 'F_THEME4']]

svi_fvars_nc = svi_fvars[svi_fvars['ST_ABBR'] == 'NC']
svi_fvars_nc
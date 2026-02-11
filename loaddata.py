import pandas as pd
from database import engine,query
import datetime as dt
import numpy as np
pd.options.display.float_format = '{:.2f}'.format

df_event = pd.read_sql(query, engine)

columns_str = ['name', 'district']
columns_numeric = ['eventcount']
columns_datime = ['eventsdatetime']

for column in columns_str: df_event[column] = df_event[column].astype(str)
for column in columns_numeric: df_event[column] = pd.to_numeric(df_event[column], errors='coerce')
for column in columns_datime: df_event[column] = pd.to_datetime(df_event[column],format="%Y-%m-%d")


df_event.sort_values("eventsdatetime", inplace=True)


print(df_event.head())
df_event.info()
print(df_event.head().T)


df_region = df_event.groupby('district' ).agg({'eventcount': 'sum'}).reset_index()
df_region.info()
print(df_region.head().T)

df_time = df_event.groupby('eventsdatetime' ).agg({'eventcount': 'sum'}).reset_index()
df_time.info()
print(df_time.head().T)

df_type = df_event.groupby('name' ).agg({'eventcount': 'sum'}).reset_index()
df_type.info()
print(df_type.head().T)

min_date = df_time['eventsdatetime'].dt.date.min()

print(f"минимальная дата наблюдения: {min_date}")
print(f"тип минимальной даты {type(min_date)}")

max_date = df_time['eventsdatetime'].dt.date.max()

print(f"Максимальная дата наблюдения: {max_date}")
print(f"тип максимальной даты {type(max_date)}")









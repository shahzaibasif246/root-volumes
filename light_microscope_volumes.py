import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_excel('PRFB_2B_anatomy.xlsx', sheet_name='Measurements_all_totals')

df = df.iloc[:79]
df = df[['sample_id', 'conversion_rate_px_per_mm', 'root_area', 'stele_area', 'length']]


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

index_list  = df.index.tolist()

df['length'] = df['length']/3
df['root_volume'] = (df['root_area'] / (df['conversion_rate_px_per_mm'] ** 2)) * df['length'] * 10


print(df)

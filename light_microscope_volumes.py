import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re


def get_samples_names(volume_dict):
    samples = list()
    calculated_volumes = list()
    for key in volume_dict:
        samples.append(key)
        calculated_volumes.append(volume_dict[key])
    return samples, calculated_volumes





df = pd.read_excel('Light_microscopy_volumes.xlsx')

df = df.iloc[:79]
df = df[['sample_id', 'conversion_rate_px_per_mm', 'root_area', 'stele_area', 'length']]


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

index_list  = df.index.tolist()


df['root_volume'] = (df['root_area'] / (df['conversion_rate_px_per_mm'] ** 2)) * df['length'] * 10
df['sample_id'] = df['sample_id'].str.replace('_[a-z]*_[0-9]X.JPG$', '', regex=True)


volumes = dict()
sample_id = None
volume = 0
previous_sample_number = 0
for index in index_list:
    if sample_id is None or not sample_id == df.loc[index, 'sample_id']:
        sample_id = df.loc[index, 'sample_id']
    
    if previous_sample_number == 0 or previous_sample_number == re.findall('[0-9]+', sample_id)[1]:
        volume = float(volume + df.loc[index, 'root_volume'])
    else:
        
        volume = 0
        volume = float(volume + df.loc[index, 'root_volume'])
    

    volumes[sample_id] = volume
    previous_sample_number = re.findall('[0-9]+', sample_id)[1]


print(df)
samples, total_volumes = get_samples_names(volumes)
print(volumes)

volumes_df = pd.DataFrame({'sample_id': samples, 'total_volume_light_microscopy': total_volumes})

volumes_df.to_excel('final_volumes.xlsx', index=False)






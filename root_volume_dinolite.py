import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_excel('PRFB_2B_anatomy.xlsx', sheet_name='B73 Total per section')

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

index_list  = df.index.tolist()



# volume will be lower than true value for roots with na data
def reimann_sum(column):
    delta_x = 20
    df[column] = pd.to_numeric(df[column], errors='coerce')
    area_mm2 = column + '_mm2'
    df[area_mm2] = df[column] * (df['conversion_rate_mm_per_px'] **2)
    volume = column + '_volume'

    df[volume] = df[area_mm2] * delta_x
    
  

    return df


def get_dict(df, name):
    sample_id = None
    volumes = dict()
    for index in index_list:
        
        if sample_id is None:
            sample_id = df.loc[index, 'sample_id']
            total_volume = 0
        if not df.loc[index, 'sample_id'] == sample_id:
            volumes[sample_id] = float(total_volume)
            sample_id = df.loc[index, 'sample_id']
            total_volume = 0
        if np.isnan(df.loc[index, name]):
            continue
        total_volume = total_volume + df.loc[index, name]
        if index == len(index_list)-1:
            volumes[sample_id] = float(total_volume)
    return volumes

def get_samples_names(volume_dict):
    samples = list()
    calculated_volumes = list()
    for key in volume_dict:
        samples.append(key)
        calculated_volumes.append(volume_dict[key])
    return samples, calculated_volumes




def bar_graph(n, samples, calculated_volumes):
    plt.figure(n)
    bars = plt.bar(samples, calculated_volumes)
    plt.xticks(rotation=90)

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x()
            + bar.get_width()/2,
            height,
            str(height),
            ha='center',
            va='bottom',
            rotation=90
        )


reimann_sum('root_area')
root_area_dict = get_dict(reimann_sum('root_area'), 'root_area_volume')
stele_area_dict = get_dict(reimann_sum('stele_area'), 'stele_area_volume')
pith_area_dict = get_dict(reimann_sum('pith_area'), 'pith_area_volume')

print(root_area_dict)
print(stele_area_dict)
print(pith_area_dict)
root_samples, root_total_volumes = get_samples_names(root_area_dict)
root_samples, stele_total_volumes = get_samples_names(stele_area_dict)
root_samples, pith_total_volumes = get_samples_names(pith_area_dict)


bar_graph(1, root_samples, root_total_volumes)
bar_graph(2, root_samples, stele_total_volumes)
bar_graph(3, root_samples, pith_total_volumes)

plt.show()







import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_excel('PRFB_2B_anatomy.xlsx', sheet_name='B73 Total per section')



index_list  = df.index.tolist()

print(len(index_list))

# volume will be lower than true value for roots with na data
def reimann_sum(column):
    sample_id = None
    delta_x = 20
    volumes = dict()
    volume = 0
    for index in index_list:
        if sample_id is None:
            sample_id = df.loc[index, 'sample_id']
    
        if not df.loc[index, 'sample_id'] == sample_id:
            volumes[sample_id] = volume
            sample_id = df.loc[index, 'sample_id']
            volume = 0
        if df.loc[index, column] == 'na':
            continue

        
        cross_section_area_pixel2 = df.loc[index, column]
        conversion_rate = float(df.loc[index, 'conversion_rate_mm_per_px'] ** 2)
        cross_section_area_mm2 = float(cross_section_area_pixel2 * conversion_rate)

        
        volume = volume + (cross_section_area_mm2 * delta_x)

        if index == len(index_list)-1:
            volumes[sample_id] = volume

        print(sample_id, index, volume, cross_section_area_mm2 * delta_x)
    return volumes

#print(reimann_sum('root_area'))

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


root_area_dict = reimann_sum('root_area')
#stele_area_dict = reimann_sum('stele_area')
#pith_area_dict = reimann_sum('pith_area')


print(root_area_dict)
root_samples, root_total_volumes = get_samples_names(root_area_dict)
#root_samples, stele_total_volumes = get_samples_names(stele_area_dict)
#root_samples, pith_total_volumes = get_samples_names(pith_area_dict)

#bar_graph(1, root_samples, root_total_volumes)
#bar_graph(2, root_samples, stele_total_volumes)
#bar_graph(3, root_samples, pith_total_volumes)

plt.show()







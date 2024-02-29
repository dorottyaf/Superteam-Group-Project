import pandas as pd
import geopandas as gpd
import pathlib
import seaborn as sns
import matplotlib.pyplot as plt
from data_analysis.geomatching import TRACT_2000, TRACT_2010, TRACT_2020, \
   COMM_AREAS, shape_matcher
from pprint import pprint

variables = ["age", "ethnicity", "household", "educ", "gender", "income", "race"]
COLS_TO_DROP = ['NAME', 'state', 'county', 'tract', 'population', 'period']
COLS_TO_DROP2 = ['NAME', 'state', 'county', 'population']
COLS_TO_DROP3 = ['area', 'area_num_1', 'area_numbe', 'comarea', 'comarea_id', 'perimeter', 'shape_area', 'shape_len']

# given a variable name, load in corresponding percentage data
def load_data(name:str):
    csv_name = name + "_percentage_data.csv"
    filename = pathlib.Path(__file__).parent.parent / "data" / "clean_data" / csv_name
    data = pd.read_csv(filename)
    return data

# getting the shape file for community areas in chicago
def get_chi_shape():
    shp_file = "Boundaries - Community Areas (current)"
    shp_file_path = pathlib.Path(__file__).parent.parent / "data_analysis" / 'Location Information' / shp_file
    chi_comm = gpd.read_file(shp_file_path)
    chi_comm = chi_comm.to_crs(epsg = 32617)
    # mask for only cook county
    return chi_comm



#get cook shape file
chi_comm = get_chi_shape()

# pick a variable and load in the data
var = 'race'
df = load_data(var)

# cleaning up columns, changing column name for matching
df = df.drop(columns= COLS_TO_DROP2)
df = df.rename(columns={'community_area' : 'community'})

# merging on column, cleaning up extra columns once again
df_merge = df.merge(chi_comm, on= 'community', how= 'left')
df_sub = df_merge.drop(columns= COLS_TO_DROP3)

# doing just one period

period = '2005-2009'
df_plot = df_sub[df_sub['period'] == period]
df_plot = gpd.GeoDataFrame(df_plot)
print(df_plot)

# Create subplots
fig, ax = plt.subplots(1, 1, figsize = (20, 10))
df_plot.plot(column = "white",
                ax = ax,
                cmap = "RdPu",
                legend = True)
# Stylize plots
plt.style.use('bmh')

# Set title
ax.set_title('Percentage of Population that is White by Tract for ' + period, fontdict = {'fontsize': '25', 'fontweight' : '3'})
plt.show()

period = '2010-2014'
df_plot = df_sub[df_sub['period'] == period]
df_plot = gpd.GeoDataFrame(df_plot)
print(df_plot)

# Create subplots
fig, ax = plt.subplots(1, 1, figsize = (20, 10))
df_plot.plot(column = "white",
                ax = ax,
                cmap = "RdPu",
                legend = True)
# Stylize plots
plt.style.use('bmh')

# Set title
ax.set_title('Percentage of Population that is White by Tract for ' + period, fontdict = {'fontsize': '25', 'fontweight' : '3'})
plt.show()
plt.clf()













'''
# for exporatory, getting tracts with greatest changes for each of 7 variables
for var in variables:
    df = load_data(var)
    group = df.groupby("tract")
    if var == "age":
        for name, data in group:
            if name in age_top_10:
                for time in set(data['period']):
                    data_by_time = data[data['period'] == time]
                    data_by_time = data_by_time.drop(columns = COLS_TO_DROP)
                    data_by_time_t = data_by_time.transpose()
                    plt.plot(data_by_time_t.index, data_by_time_t.values, marker='o', linestyle='-', label = time)
                plt.xlabel('Age Range')
                plt.ylabel('Percentage of Population in Age Range')
                plt.title("Changes in Age Distribution Over Time for Tract: " + str(name))
                plt.legend()
                png_name = str(name) + "_age_plot.png"
                direc = pathlib.Path(__file__).parent / 'temp_graphs' / png_name
                plt.savefig(direc)
                plt.clf()
    if var == "ethnicity":
        for name, data in group:
            if name in eth_top_10:
                for time in set(data['period']):
                    data_by_time = data[data['period'] == time]
                    data_by_time = data_by_time.drop(columns = COLS_TO_DROP)
                    data_by_time_t = data_by_time.transpose()
                    plt.plot(data_by_time_t.index, data_by_time_t.values, marker='o', linestyle='-', label = time)
                plt.xlabel('Ethnicity')
                plt.ylabel('Percentage of Population of Ethnicity')
                plt.title("Changes in Ethnicity Distribution Over Time for Tract: " + str(name))
                plt.legend()
                png_name = str(name) + "_ethnicity_plot.png"
                direc = pathlib.Path(__file__).parent / 'temp_graphs' / png_name
                plt.savefig(direc)
                plt.clf()
                '''
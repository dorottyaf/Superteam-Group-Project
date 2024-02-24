import pandas as pd
import pathlib
import seaborn as sns
import matplotlib.pyplot as plt
import pprint

variables = ["age", "ethnicity", "household", "educ", "gender", "income", "race"]
COLS_TO_DROP = ['NAME', 'state', 'county', 'tract', 'population', 'period']
age_top_10 = [835700, 611800, 834600, 670100, 251700, 835600, 690500, 380500, 830201, 841400]
eth_top_10 = []
hh_top_10 = []
educ_top_10 = []
gender_top_10 = []
inc_top_10 = []
race_top_10 = []


def load_data(name:str):
    csv_name = name + "_percentage_data.csv"
    filename = pathlib.Path(__file__).parent.parent / "data" / "clean_data" / csv_name
    data = pd.read_csv(filename)
    return data

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
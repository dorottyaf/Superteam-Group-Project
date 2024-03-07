import pandas as pd
import pathlib
from clean_process import variables

def load_data(name:str):
    csv_name = name + "_percentage_data.csv"
    filename = pathlib.Path(__file__).parent / "clean_data" / csv_name
    data = pd.read_csv(filename)
    print(data)

for var in variables:
    load_data(var)
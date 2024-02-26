from exploring_data import load_dataset, find_top_k, detailed_top_k

# Data entry

def explore(dataset:str, period1: str, period2:str, num_results:int, column = "total_change", further = False):

    data = load_dataset(dataset)
    to_print = find_top_k(data, period1, period2, column, num_results)
    print(to_print)

    if further:
        result = detailed_top_k(to_print, period1, period2, dataset)
        for r in result:
            print(r)

explore("income", "2005-2009", "2018-2022", 1, further=True)

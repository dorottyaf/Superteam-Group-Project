from data_analysis.biggest_change import readable_change_simple, readable_change_complex

def run():
    k = input("Hello! Please give me a number and I'll show you the top k demographic changes in Chicago! ")
    k = int(k)
    readable_change_simple(k)
    is_variable = input("Would you like to see the changes for a specific demogrpahic variable? Yes or No? ")
    if is_variable == "No":
        text = "Sad to see you go. Goodbye!"
        return text
    variable = input("Pick a variable to explore from this list - income, age, educ, ethnicity, gender, household, race :")

    readable_change_complex(k, variable)

    is_graph = input("Would you like to see a graph for one of the changes? If so, give me the number of the line of the change you want to see, if not, type No ")
    if is_graph == "No":
        text = "Sad to see you go. Goodbye!"
        return text
    
    is_graph = int(is_graph)


run()
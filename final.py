from data_analysis.biggest_change import readable_change_simple, readable_change_complex
from visualization.explore import given_values_make_plot

def run():
    k = input("Hello! Please give me a number and I'll show you the top k demographic changes in Chicago! ")
    k = int(k)
    readable_change_simple(k)
    is_variable = input("Would you like to see the changes for a specific demographic variable? Yes or No? ")
    if is_variable == "No":
        text = "Sad to see you go. Goodbye!"
        return text
    variable = input("Pick a variable to explore from this list - income, age, educ, ethnicity, gender, household, race :")

    lst_of_changes = readable_change_complex(k, variable)

    is_graph = input("Would you like to see a graph for one of the changes? If so, give me the number of the line of the change you want to see, if not, type No ")
    if is_graph == "No":
        text = "Sad to see you go. Goodbye!"
        return text
    
    is_graph = int(is_graph)
    for change in lst_of_changes:
        if change[0] == is_graph:
            given_values_make_plot(variable, change[2], change[3], change[1])
    print("Cool! Your graphs are in visualization/finished_graphs")

    is_secondary = input("Would you like to explore how a secondary data changes along the changes you discovered?")
    if is_secondary == "No":
        text = "Sad to see you go. Goodbye!"
        return text
    
    print("Lovely!")
    secondary_input =  input("Pick a secondary data source from DePaul_Index, etc. :")
    print("Here you go!")
    readable_change_complex(k, variable, secondary = secondary_input)

    print("That was our app, thanks for playing! Have a great day!")

run()
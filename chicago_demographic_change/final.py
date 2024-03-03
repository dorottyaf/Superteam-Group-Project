from .data_analysis.biggest_change import readable_change_simple, readable_change_complex
from .visualization.explore import given_values_make_plot

def run():
    k = input("Hello! Please give me a number and I'll show you the top k " \
              "demographic changes in Chicago! ")
    k = int(k)
    readable_change_simple(k)

    user_smart = False
    while not user_smart:
        is_variable = input("Would you like to see the changes for a specific " \
                            "demographic variable? Yes or No? ")
        if is_variable not in ["yes", "no", "Yes", "No"]:
            print("Please give a yes or no answer!")
        else:
            user_smart = True

    if is_variable == "No" or is_variable == "no":
        return "Sad to see you go. Goodbye!"
    
    user_smart = False
    while not user_smart:
        variable = input("Pick a variable to explore from this list - income, " \
                         "age, educ, ethnicity, gender, household, race: ")
        if variable not in ["income", "age", "educ", "ethnicity", "gender", \
                            "household", "race"]:
            print("Please chose from the available variables")
        else:
            user_smart = True

    lst_of_changes = readable_change_complex(k, variable)

    user_smart = False
    while not user_smart:
        is_graph = input("Would you like to see a graph for one of the changes?"
                         " If so, give me the number of the line of the change "
                         "you want to see, if not, type No ")
        if is_graph.isdigit():
            is_graph = int(is_graph)
            if is_graph > len(lst_of_changes):
                print("Your number is too big! \
                      Give a valid number from the list! ")
                continue
            user_smart = True
            continue
        if is_graph == "No" or is_graph == "no":
            return "Sad to see you go. Goodbye!"
        else:
            print("Please chose either a number or type 'No' ")
    
    for change in lst_of_changes:
        if change[0] == is_graph:
            given_values_make_plot(variable, change[2], change[3], change[1])
    print("Cool! Your graphs are in visualization/finished_graphs")

    user_smart = False
    while not user_smart:
        is_secondary = input("Would you like to explore how a secondary data " 
                             "changes along the changes you discovered? ")
        if is_secondary not in ["yes", "no", "Yes", "No"]:
            print("Please give a yes or no answer!")
        else:
            user_smart = True

    if is_secondary == "No" or is_secondary == "no":
        return "Sad to see you go. Goodbye!"
    
    print("Lovely!")

    user_smart = False
    while not user_smart:
        secondary_input =  input("Pick a secondary data source from DePaul_Index," \
                                 " etc. : ")
        if secondary_input not in ["DePaul_Index"]:
            print("Please give a valid secondary data source name!")
        else:
            user_smart = True
        
    print("Here you go!")
    readable_change_complex(k, variable, secondary = secondary_input)

    print("That was our app, thanks for playing! Have a great day!")


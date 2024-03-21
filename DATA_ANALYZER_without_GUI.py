def CSV_import():
    import csv
    Dictionary = {}
    path = input("Directory: ")
    with open(path, 'r') as csv_file:
        csv_dict = csv.DictReader(csv_file)
        Array_Dicts = []
        Field_Names = csv_dict.fieldnames
        for row in csv_dict:
            Array_Dicts.append(row)
    data_types = []
    for i in range(len(Field_Names)):
        x = str(Array_Dicts[0][Field_Names[i]])
        if x.strip('-').isnumeric():
            data_types.append('numerical')
        elif is_date(x):
            data_types.append('date')
        else:
            data_types.append('string')
    return Array_Dicts, Field_Names, data_types


def CSV_export(dictionary):
    import csv
    path = str(input("Directory: "))
    with open(path, 'w', newline='') as csv_file:
        csv_dict = csv.DictWriter(csv_file, fieldnames=field_names)
        csv_dict.writeheader()
        csv_dict.writerows(dictionary)


def is_date(date):
    import re
    regular_expression = r"^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$"

    if re.match(regular_expression, date):
        return True
    else:
        return False


def export_stats_csv(statistics):
    import csv
    field_names = []
    for i in statistics[0]:
        field_names.append(i)
    with open(input("Directory: "), 'w', newline='') as stats_file:
        csv_stats = csv.DictWriter(stats_file, fieldnames=field_names)
        csv_stats.writeheader()
        csv_stats.writerows(statistics)


def Manual_import(Type):
    if Type == 'write':
        while True:
            try:
                num_var = int(input("Enter number of variables: "))
                if num_var > 0:
                    break
                else:
                    print("Error, please enter a valid integer")
            except:
                print("Error, please enter a valid integer")
        Array_Dictionary = []
        Field_names = []
        var_data_types = []
        accepted_data_types = ["string", "numerical", "date"]
        for i in range(num_var):
            variable_name = str(input(f"Enter Field name for column {str(i + 1)}: "))
            while variable_name in Field_names:
                variable_name = str(
                    input(f"You cannot reuse the same field name twice. Enter Field name for column {str(i + 1)}: "))
            Field_names.append(variable_name)
            x = str(input("Date type [string,numerical,date]: "))
            while True:
                if x in accepted_data_types:
                    var_data_types.append(x)
                    break
                else:
                    x = input("Error, enter valid data type [string,numerical,date]: ")
        while True:
            Array_Dictionary.append(manual_input(var_data_types, Field_names))
            con = input("Continue?(yes/no) ")
            if con == 'no':
                break
            else:
                while con != 'yes':
                    con = input("Error, enter yes or no: ")
        return Array_Dictionary, Field_names, var_data_types
    if Type == 'append':
        while True:
            dictionary.append(manual_input(data_types, field_names))
            while True:
                con = input("Continue?(yes/no) ")
                if con == 'no':
                    return
                elif con == 'yes':
                    break
                else:
                    print("Error. Enter yes or no: ")

    if Type == 'change':
        return manual_input(data_types, field_names)


def manual_input(var_data_types, field_names):
    temporary_dictionary = {}
    for i in range(len(field_names)):
        x = input(f"{field_names[i]}: ")
        while True:
            if var_data_types[i] == "numerical":
                if x.strip('-').isnumeric():
                    x = float(x)
                    break
                else:
                    x = input("Error, enter valid number: ")
            elif var_data_types[i] == "string":
                x = str(x)
                break
            elif var_data_types[i] == "date":
                x = str(x)
                if is_date(x):
                    break
                else:
                    x = input("Error, enter valid date: ")
        temporary_dictionary[field_names[i]] = x
    return temporary_dictionary


def CSV_lookup():
    filtered_list = dictionary.copy()
    while True:
        filtered_variable = input(f"Enter variable name from {str(field_names)}: ")
        while True:
            if filtered_variable not in field_names or data_types[field_names.index(filtered_variable)] == 'date':
                filtered_variable = input("Error, enter a valid variable name (cannot be a date): ")
            else:
                break
        filter_con = input("Enter condition: ")
        try:
            if len(filtered_list) > 0:
                filtered_list = apply_filter(filtered_list, filtered_variable, filter_con)
                if len(filtered_list) == 0:
                    print("N/A")
            else:
                print("No data available.")
        except:
            print("Error, invalid condition")
        while True:
            user_input = input("What would you like to do? [print, continue, edit, export, end]: ")
            while user_input not in ['print', 'continue', 'edit', 'end', 'export']:
                user_input = input("Please enter a valid option: ")

            if user_input == 'print':
                print(filtered_list)
            elif user_input == 'continue':
                break
            elif user_input == 'edit':
                edit = input('What would you like to do? [change, delete]: ')
                while edit not in ['change', 'delete']:
                    edit = input("Please enter a valid option: ")

                if edit == 'change':
                    if len(filtered_list) == 1:
                        change_value(filtered_list[0])
                    else:
                        print('You can only change one item at a time. Please filter and select one item.')
                elif edit == 'delete':
                    delete_items(filtered_list)
                    filtered_list = dictionary.copy()
            elif user_input == 'export':
                CSV_export(filtered_list)
            elif user_input == 'end':
                return


def apply_filter(data, variable, condition):
    filtered_data = []
    for item in data:
        if data_types[field_names.index(variable)] == 'numerical':
            if eval(str(item[variable]) + condition):
                filtered_data.append(item)
        elif data_types[field_names.index(variable)] == 'string':
            if item[variable] == condition:
                filtered_data.append(item)
    return filtered_data


def change_value(item):
    for key in item.keys():
        new_value = input(f"Enter new value for {key}: ")
        while not validate_input(key, new_value):
            new_value = input(f"Error, enter a valid value for {key}: ")
        item[key] = new_value


def validate_input(variable, value):
    if data_types[field_names.index(variable)] == 'numerical':
        return value.strip('-').isnumeric()
    elif data_types[field_names.index(variable)] == 'string':
        return isinstance(value, str)
    elif data_types[field_names.index(variable)] == 'date':
        return is_date(value)


def delete_items(items):
    for item in items:
        dictionary.remove(item)


def troubleshoot():
    tool = input('What would you like to do?\n["redefine data types","check data types"]')
    if tool == "redefine data types":
        for i in range(len(field_names)):
            data_types[i] = input("enter data type for " + str(field_names[i] + ':'))
    elif tool == "check data types":
        zero = input('Would you like to replace empty strings with zero for numerical data?')
        while zero not in ['yes', 'no']:
            zero = input('Error. Please enter yes or no. \n'
                         'Would you like to replace empty strings with zero for numerical data?')
        for i in range(len(field_names)):
            for j in range(len(dictionary)):
                condition = 0
                if data_types[i] == "string":
                    if str(dictionary[j][field_names[i]]) != dictionary[j][field_names[i]]:
                        if zero == 'yes' and dictionary[j][field_names[i]] == '':
                            dictionary[j][field_names[i]] = 0
                        else:
                            condition = 1
                elif data_types[i] == "numerical":
                    if not str(dictionary[j][field_names[i]]).strip('-').isnumeric():
                        condition = 1
                elif data_types[i] == "date":
                    if not (is_date(dictionary[j][i])):
                        condition = 1

                if condition == 1:
                    print(f'The value \'{dictionary[j][field_names[i]]}\', of {field_names[i]} for row number {j + 1} '
                          f'does not satisfy the {data_types[i]} condition')
                    replace_value = input("Would you like to replace this value?")
                    while replace_value not in ['yes', 'no']:
                        replace_value = input("Please enter yes or no. Would you like to replace this value?")
                    if replace_value == 'yes':
                        x = str(input(f"Enter the new value for {field_names[i]} row {j + 1}"))
                        while True:
                            if data_types[i] == "numerical":
                                if x.strip('-').isnumeric():
                                    x = float(x)
                                    break
                                else:
                                    x = input("Error, enter valid number")
                            elif data_types[i] == "string":
                                break
                            elif data_types[i] == "date":
                                if is_date(x):
                                    break
                                else:
                                    x = input("Error, enter valid date")
                        dictionary[j][field_names[i]] = x
        print("No other mismatches found")


def sort(item_key, method):
    if data_types[field_names.index(item_key)] == 'numerical':
        quicksort(0, len(dictionary) - 1, item_key)
        sorted_dictionary = dictionary
    elif data_types[field_names.index(item_key)] == 'date':
        print("Date sorting does not work properly on formats other than yyyy/dd/mm")
        sorted_dictionary = sorted(dictionary, key=lambda k: k[item_key])
    elif data_types[field_names.index(item_key)] == 'string':
        sorted_dictionary = sorted(dictionary, key=lambda k: k[item_key])
    if method == 'dec':
        sorted_dictionary.reverse()
    return sorted_dictionary


def CSV_append():
    x = Manual_import('append')
    [dictionary.append(i) for i in x]


def data_entry_meth():
    x = str(input("Do you want to import csv or enter manually?(Import/Manual) "))
    while x not in ['import', 'manual', 'Import', 'Manual']:
        x = str(input("Error, enter import or manual: "))
    if x == "import" or x == "Import":
        return CSV_import()
    elif x == "manual" or x == "Manual":
        return Manual_import('write')


def quicksort_partition(bot, top, key):
    pivot = dictionary[top][key]
    i = bot - 1
    for j in range(bot, top):
        if dictionary[j][key] <= pivot:
            i = i + 1
            dictionary[i][key], dictionary[j][key] = dictionary[j][key], dictionary[i][key]
    dictionary[i + 1][key], dictionary[top][key] = dictionary[top][key], dictionary[i + 1][key]
    return i + 1


def quicksort(bot, top, key):
    if bot < top:
        pivot = quicksort_partition(bot, top, key)
        quicksort(bot, pivot - 1, key)
        quicksort(pivot + 1, top, key)


def plot(graph_type):
    import plotly.graph_objects as plg
    x_key = input("enter x axis variable." + str(field_names))
    y_key = input("enter y axis variable." + str(field_names))
    while True:
        if (x_key in field_names) and (y_key in field_names):
            break
        else:
            print("Error, enter valid fields.")
            x_key = input(f"enter x axis variable {field_names}: ")
            y_key = input(f"enter y axis variable {field_names}: ")
    x = []
    y = []
    quicksort(0, len(dictionary) - 1, y_key)
    for i in range(len(dictionary)):
        x.append(dictionary[i][x_key])
        y.append(dictionary[i][y_key])
    while True:
        if graph_type == "Bar Graph":
            figure = plg.Figure([plg.Bar(x=x, y=y)])
            break
        elif graph_type == "Line Graph":
            figure = plg.Figure([plg.Scatter(x=x, y=y, mode='lines')])
            break
        elif graph_type == "Scatter Graph":
            figure = plg.Figure([plg.Scatter(x=x, y=y, mode='markers')])
            break
        else:
            graph_type = input("Error. Enter valid Graph type.[Bar Graph,Line Graph,Scatter Graph]")

    figure.update_layout(xaxis_title=x_key, yaxis_title=y_key)
    if figure:
        figure.show()


def cum_plot():
    import plotly.graph_objects as plg
    key = input("Enter the variable for the cumulative frequency graph: ")
    while key not in field_names:
        key = input("Error. Enter a valid variable name: ")

    quicksort(0, len(dictionary) - 1, key)

    values = []
    cumulative_freq = []
    frequency = 0

    for i in range(len(dictionary)):
        value = dictionary[i][key]
        if value not in values:
            values.append(value)
            frequency += 1
        cumulative_freq.append(frequency)

    figure = plg.Figure(data=[plg.Scatter(x=values, y=cumulative_freq, mode='lines')])
    figure.update_layout(xaxis_title=key, yaxis_title='Cumulative Frequency')
    figure.show()


def central_tend(key):
    import math
    length = len(dictionary)
    quicksort(0, length - 1, key)
    x = []
    for i in range(length):
        x.append(float(dictionary[i][key]))
    summation = sum(x)
    mean = summation / length
    if length // 2 == 0:
        median = 0.5 * (x[length / 2] + x[length / 2 + 1])
    else:
        median = x[math.floor(length / 2) + 1]
    sum_variance = 0
    for i in x:
        sum_variance += (i - mean) ** 2
    std_dev = math.sqrt(sum_variance / length)
    values = []
    accumulation = []
    j = 1
    for i in range(length):
        i = int(i)
        if i >= 1:
            if x[i - 1] == x[i]:
                j = j + 1
            else:
                values.append(x[i])
                accumulation.append(j)
                j = 1
        else:
            values.append(x[i])
    mode = values[accumulation.index(max(accumulation))]
    maximum = max(x)
    minimum = min(x)
    field_range = maximum - minimum
    return length, summation, mean, median, std_dev, mode, values, accumulation, maximum, minimum, field_range


if __name__ == "__main__":

    import sys
    sys.setrecursionlimit(10000)
    dictionary, field_names, data_types = data_entry_meth()
    statistics = []
    while True:
        user_input = input("What would you like to do? [plot, analyze, export csv, show statistics, "
                           "export statistics, troubleshoot, lookup, append, sort, print] ")
        while True:
            try:
                if user_input == 'analyze':
                    try:
                        key = input("field name?" + str(field_names))
                        x = -1
                        while True:
                            if key not in field_names:
                                key = input("Error. Enter valid field name." + str(field_names))
                            else:
                                break
                        for i in range(len(statistics)):
                            if statistics[i]['fieldname'] == key:
                                x = i
                                break
                        if x == -1:
                            l = central_tend(key)
                            list = [key]
                            for i in l:
                                list.append(i)
                            cent_list = ['fieldname', 'length', 'summation', 'mean', 'median', 'std_dev', 'mode',
                                         'values', 'accumulation', 'maximum', 'minimum', 'range']
                            temp_dict = {}
                            for i in range(len(cent_list)):
                                temp_dict[cent_list[i]] = list[i]
                            statistics.append(temp_dict)
                            print(temp_dict)
                            break
                        else:
                            print(statistics[x])
                            break
                        break
                    except:
                        print("invalid variable")
                        break
                elif user_input == 'plot':
                    while True:
                        user_input = input('What would you like to plot?\n[Bar Graph,Line Graph,Scatter Graph,'
                                           'Cumulative Frequency Graph]')
                        try:
                            if user_input in ['Bar Graph', 'Line Graph', 'Scatter Graph']:
                                plot(user_input)
                                break
                            elif user_input == 'Cumulative Frequency Graph':
                                cum_plot()
                                break
                        except:
                            print('invalid variables, try again.')
                            break
                    break
                elif user_input == 'export csv':
                    CSV_export(dictionary)
                    break
                elif user_input == 'show statistics':
                    print(statistics)
                    break
                elif user_input == 'export statistics':
                    export_stats_csv(statistics)
                    break
                elif user_input == 'troubleshoot':
                    troubleshoot()
                    break
                elif user_input == 'lookup':
                    CSV_lookup()
                    break
                elif user_input == 'sort':
                    try:
                        key = input(f'Enter the variable you want to sort with?\n{field_names}')
                        if key not in field_names:
                            while key not in field_names:
                                key = input('Error, enter a valid field name')
                        method = input('asc or dec?')
                        if method not in ['asc', 'dec']:
                            while method not in ['asc', 'dec']:
                                method = input('Error. Please enter asc or dec?')
                        dictionary = sort(key, method)
                    except:
                        print("Something went wrong. Please try again.")
                    break
                elif user_input == 'print':
                    print(dictionary)
                    break
                elif user_input == 'append':
                    Manual_import('append')
                    break
                else:
                    print("Error,enter valid task")
                    user_input = input("What would you like to do? [plot, analyze, export csv, show statistics, "
                                       "export statistics, troubleshoot, lookup, append, plot cumulative frequency]: ")
            except:
                print('Error! Some thing broke somewhere.')
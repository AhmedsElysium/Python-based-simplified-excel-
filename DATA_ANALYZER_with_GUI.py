import tkinter as tk
from tkinter import filedialog
import csv
import plotly.graph_objects as plg
from tkinter import messagebox
from tkinter import simpledialog

root = tk.Tk()

dictionary = []
field_names = []
data_types = {}  # Dictionary to store data types for fields

def import_csv():
    global dictionary, field_names, data_types

    csv_file_path = filedialog.askopenfilename()

    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        field_names = reader.fieldnames
        for row in reader:
            dictionary.append(row)

    data_types = {field_name: "string" for field_name in field_names}

    update_dropdown_menus()

def update_dropdown_menus():
    x_var.set('')
    x_menu['menu'].delete(0, 'end')
    for choice in field_names:
        x_menu['menu'].add_command(label=choice, command=tk._setit(x_var, choice))

    y_var.set('')
    y_menu['menu'].delete(0, 'end')
    for choice in field_names:
        y_menu['menu'].add_command(label=choice, command=tk._setit(y_var, choice))

    analysis_var.set('')
    analysis_menu['menu'].delete(0, 'end')
    for choice in field_names:
        analysis_menu['menu'].add_command(label=choice, command=tk._setit(analysis_var, choice))

    sort_var.set('')
    sort_menu['menu'].delete(0, 'end')
    for choice in field_names:
        sort_menu['menu'].add_command(label=choice, command=tk._setit(sort_var, choice))

def is_date_format(date_str):
    import re
    pattern = r"\d{4}/\d{2}/\d{2}"  # yyyy/dd/mm
    return re.match(pattern, date_str) is not None

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
        if key in field_names and all(is_date_format(dictionary[i][key]) for i in range(bot, top + 1)):
            pivot = quicksort_partition(bot, top, key)
            quicksort(bot, pivot - 1, key)
            quicksort(pivot + 1, top, key)

        else:
            pivot = quicksort_partition(bot, top, key)
            quicksort(bot, pivot - 1, key)
            quicksort(pivot + 1, top, key)

        sorted_dates = [dictionary[i][key] for i in range(bot, top + 1)]
        print("Sorted Dates:", sorted_dates)


def plot(x_key, y_key, graph_type):
    if (x_key in field_names) and (y_key in field_names):
        x = []
        y = []
        for i in range(len(dictionary)):
            x.append(dictionary[i][x_key])
            y.append(dictionary[i][y_key])
        if graph_type == "Bar Graph":
            figure = plg.Figure([plg.Bar(x=x, y=y)])
        elif graph_type == "Line Graph":
            figure = plg.Figure([plg.Scatter(x=x, y=y, mode='lines')])
        elif graph_type == "Scatter Graph":
            figure = plg.Figure([plg.Scatter(x=x, y=y, mode='markers')])
        figure.update_layout(xaxis_title=x_key, yaxis_title=y_key)
        if figure:
            figure.show()
    else:
        print("Invalid axes selection")

def central_tend(key):
    import math
    length = len(dictionary)
    quicksort(0, length - 1, key)
    x = []
    for i in range(length):
        x.append(float(dictionary[i][key]))
    summation = sum(x)
    mean = summation / length
    if length % 2 == 0:
        median = 0.5 * (x[length // 2] + x[length // 2 - 1])
    else:
        median = x[length // 2]
    sum_variance = 0
    for i in x:
        sum_variance += (i - mean) ** 2
    std_dev = math.sqrt(sum_variance / length)
    values = []
    accumulation = []
    j = 1
    for i in range(length):
        if i >= 1:
            if x[i - 1] == x[i]:
                j = j + 1
            else:
                values.append(x[i - 1])
                accumulation.append(j)
                j = 1
        else:
            values.append(x[i])
    mode = values[accumulation.index(max(accumulation))]
    maximum = max(x)
    minimum = min(x)
    field_range = maximum - minimum
    return length, summation, mean, median, std_dev, mode, values, accumulation, maximum, minimum, field_range

def plot_button_clicked():
    x_key = x_var.get()
    y_key = y_var.get()
    graph_type = graph_type_var.get()
    plot(x_key, y_key, graph_type)

def analyze_button_clicked():
    key = analysis_var.get()
    if key in field_names:
        result = central_tend(key)
        result_text = f"Length: {result[0]}\n" \
                      f"Summation: {result[1]}\n" \
                      f"Mean: {result[2]}\n" \
                      f"Median: {result[3]}\n" \
                      f"Standard Deviation: {result[4]}\n" \
                      f"Mode: {result[5]}\n" \
                      f"Values: {result[6]}\n" \
                      f"Accumulation: {result[7]}\n" \
                      f"Maximum: {result[8]}\n" \
                      f"Minimum: {result[9]}\n" \
                      f"Field Range: {result[10]}"
        messagebox.showinfo("Analysis Result", result_text)
    else:
        print("Invalid analysis variable")

def sort_button_clicked():
    key = sort_var.get()
    if key in field_names:
        quicksort(0, len(dictionary) - 1, key)
        messagebox.showinfo("Sort Complete", f"Data sorted by {key} successfully!")
    else:
        print("Invalid sort variable")

import_btn = tk.Button(master=root, text="Import CSV", command=import_csv)
import_btn.pack()

x_var = tk.StringVar(root)
x_menu = tk.OptionMenu(root, x_var, '')
x_menu.pack()

y_var = tk.StringVar(root)
y_menu = tk.OptionMenu(root, y_var, '')
y_menu.pack()

graph_type_var = tk.StringVar(root)
graph_types = ["Bar Graph", "Line Graph", "Scatter Graph"]
graph_type_var.set(graph_types[0])
graph_menu = tk.OptionMenu(root, graph_type_var, *graph_types)
graph_menu.pack()

plot_btn = tk.Button(master=root, text="Plot Data", command=plot_button_clicked)
plot_btn.pack()

analysis_var = tk.StringVar(root)
analysis_menu = tk.OptionMenu(root, analysis_var, '')
analysis_menu.pack()

analyze_btn = tk.Button(master=root, text="Analyze", command=analyze_button_clicked)
analyze_btn.pack()

sort_var = tk.StringVar(root)
sort_menu = tk.OptionMenu(root, sort_var, '')
sort_menu.pack()

sort_btn = tk.Button(master=root, text="Sort Data", command=sort_button_clicked)
sort_btn.pack()

def redefine_data_types():
    for field_name in field_names:
        data_type = simpledialog.askstring("Redefine Data Types", f"Enter data type for {field_name}:")
        data_types[field_name] = data_type


def check_data_types():
    zero = messagebox.askquestion("Check Data Types",
                                  "Would you like to replace empty strings with zero for numerical data?")

    for field_name in field_names:
        for i in range(len(dictionary)):
            condition = 0
            if data_types[field_name] == "string":
                if str(dictionary[i][field_name]) != dictionary[i][field_name]:
                    if zero == 'yes' and dictionary[i][field_name] == '':
                        dictionary[i][field_name] = 0
                    else:
                        condition = 1
            elif data_types[field_name] == "numerical":
                if not str(dictionary[i][field_name]).strip('-').isnumeric():
                    condition = 1
            elif data_types[field_name] == "date":
                if not is_date(dictionary[i][field_name]):
                    condition = 1
                    messagebox.showinfo(
                        "Data Type Mismatch",
                        f"The value '{dictionary[i][field_name]}' of {field_name} for row number {i + 1} does not satisfy the {data_types[field_name]} condition."
                    )
                    replace_value = messagebox.askquestion("Replace Value", "Would you like to replace this value?")
                    if replace_value == 'yes':
                        new_value = simpledialog.askstring("Enter New Value",
                                                           f"Enter the new value for {field_name} row {i + 1}")
                        while True:
                            if data_types[field_name] == "numerical":
                                if new_value.strip('-').isnumeric():
                                    new_value = float(new_value)
                                    break
                                else:
                                    new_value = simpledialog.askstring("Invalid Number", "Error: Enter a valid number")
                            elif data_types[field_name] == "string":
                                break
                            elif data_types[field_name] == "date":
                                if is_date(new_value):
                                    break
                                else:
                                    new_value = simpledialog.askstring("Invalid Date", "Error: Enter a valid date")
                        dictionary[i][field_name] = new_value

                messagebox.showinfo("Data Type Check", "No other mismatches found.")
def troubleshoot():
    tool = messagebox.askquestion("Troubleshooting",
                                  "What would you like to do?\n\n- Redefine data types\n- Check data types")

    if tool == "yes":
        redefine_data_types()
    elif tool == "no":
        check_data_types()


def troubleshoot_button_clicked():
    troubleshoot()


troubleshoot_btn = tk.Button(master=root, text="Troubleshoot", command=troubleshoot_button_clicked)
troubleshoot_btn.pack()

root.mainloop()


def CSV_export():
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

        user_input = input("What would you like to do? [print, continue, edit, end]: ")
        while user_input not in ['print', 'continue', 'edit', 'end']:
            user_input = input("Please enter a valid option: ")

        if user_input == 'print':
            print(filtered_list)
        elif user_input == 'continue':
            continue
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
        elif user_input == 'end':
            break


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
        for i in range(len(field_names)):
            for j in range(len(dictionary)):
                condition = 0
                if data_types[i] == "string":
                    if str(dictionary[j][field_names[i]]) != dictionary[j][field_names[i]]:
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


# ADD SORTING FOR DATES AND SORTING FOR STRINGS
def sort(key, method):
    if data_types[field_names.index(key)] == 'numerical':
        if method == 'asc':
            return quicksort(0, len(dictionary) - 1, key)
        elif method == 'dec':
            return quicksort(0, len(dictionary) - 1, key).reverse
        else:
            print('invalid method of sorting for this data type')
    # elif data_types[field_names.index(key)] == 'date':
    # TO BE DONE
    # elif data_types[field_names.index(key)] == 'string':
    #


def CSV_append():
    x = Manual_import('append')
    [dictionary.append(i) for i in x]


def data_entry_meth():
    x = str(input("Do you want to import csv or enter manually?(Import/Manual) "))
    while x not in ['import', 'manual', 'Import', 'Manual']:
        x = str(input("Error, enter import or manual: "))
    if x == "import" or x == "Import":
        return import_csv()
    elif x == "manual" or x == "Manual":
        return Manual_import('write')




def quicksort(bot, top, key):
    if bot < top:
        pivot = quicksort_partition(bot, top, key)
        quicksort(bot, pivot - 1, key)
        quicksort(pivot + 1, top, key)


def plot(x_key, y_key, graph_type):
    print(x_key, y_key, graph_type)
    import plotly.graph_objects as plg

    if x_key not in field_names or y_key not in field_names:
        print("Error, invalid fields.")
        return

    x = []
    y = []
    quicksort(0, len(dictionary) - 1, y_key)
    for i in range(len(dictionary)):
        x.append(dictionary[i][x_key])
        y.append(dictionary[i][y_key])

    if graph_type == "Bar Graph":
        figure = plg.Figure([plg.Bar(x=x, y=y)])
    elif graph_type == "Line Graph":
        figure = plg.Figure([plg.Scatter(x=x, y=y, mode='lines')])
    elif graph_type == "Scatter Graph":
        figure = plg.Figure([plg.Scatter(x=x, y=y, mode='markers')])
    else:
        print("Error. Invalid graph type.")
        return

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

    dictionary, field_names, data_types = data_entry_meth()
    statistics = []
    while True:
        user_input = input("What would you like to do? [plot, analyze, export csv, show statistics, "
                           "export statistics, troubleshoot, lookup, append, plot cumulative frequency] ")
        while True:
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
                        cent_list = ['fieldname', 'length', 'summation', 'mean', 'median', 'std_dev', 'mode', 'values',
                                     'accumulation', 'maximum', 'minimum', 'range']
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
                try:
                    plot(dictionary)
                except:
                    print('invalid variables, try again.')
                    break
            elif user_input == "plot cumulative frequency":
                try:
                    cum_plot(dictionary)
                except:
                    print('invalid variables, try again.')
                    break
            elif user_input == 'export csv':
                CSV_export()
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
            # UNDER CONSTRUCTION
            elif user_input == 'lookup':
                CSV_lookup()
                break
            elif user_input == 'append':
                Manual_import('append')
                break
            else:
                print("Error,enter valid task")
                user_input = input("What would you like to do? [plot, analyze, export csv, show statistics, "
                                   "export statistics, troubleshoot, lookup, append, plot cumulative frequency]: ")

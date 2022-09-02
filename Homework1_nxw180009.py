# Homework1
# Author: Nebil Weber
# NetID: nxw180009
# Class: CS 4395.001 - Human Language Technologies - F22


# imports
import pathlib
import sys
import pickle
import re


class Person:
    """
        Person class with fields last, first, mi, id, and phone
    """

    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    # output each person to the console
    def display(self):
        print('Employee id: ', self.id)
        print('\t', self.first, '', self.mi, '', self.last)
        print('\t', self.phone, '\n')


def regrex(result, index, index2):
    """
       Uses regrex to modify data to applicable form

       Args:
           result: employee list
           index: location of id
           index2: location of phone number

       Returns:
           result (list) with id and phone number attribute corrected.
       """

    # Modify id using regex
    for i in result:
        while re.match('[A-Za-z][A-Za-z]\d{4}', i.__getitem__(index)) is None:
            print(i.__getitem__(index), " is not a valid ID")
            print('ID is two letters followed by 4 digits')
            i[index] = input('Please enter a valid id: ')

        # Modify phone number
        while re.match('\w{3}-\w{3}-\w{4}', i.__getitem__(index2)) is None:
            print('Phone: ', i.__getitem__(index2), ' is not valid')
            print('Enter phone number in form 123-456-7890')
            i[index2] = input('Enter phone number: ')

    # return to parseData
    return result


def parseData(emp):
    """
    Parses the data file to applicable structure.

    Args:
        emp: the csv file that contains the unstructured data

    Returns:
        dic of person with id as the key
    """

    # list to store the structured employee format
    result = []

    # split on comma and add to list
    for employee in emp:
        result.append(employee.split(","))

    result = capitalize_name(result, 0, 1)
    result = middle_initial(result, 2)
    result = regrex(result, 3, 4)

    persons = {}

    for i in result:
        person = Person(i.__getitem__(0), i.__getitem__(1), i.__getitem__(2), i.__getitem__(3), i.__getitem__(4))

        # validate that key is unique
        if i.__getitem__(3) in persons:
            print("ID: ", i.__getitem__(3), " has already been used. Ending the Program.")
            exit()

        persons[i.__getitem__(3)] = person

    # return to main
    return persons


def capitalize_name(emp, index, index2):
    """
       Capitalize the first and last name of each Employee.

       Args:
           emp: employee list
           index: index location of the last name
           index2: index location of the first name

       Returns:
           emp list with names corrected.
       """

    for i in emp:
        i[index] = i.__getitem__(index).capitalize()
        i[index2] = i.__getitem__(index2).capitalize()

    # return to parseData
    return emp


def middle_initial(emp, index):
    """
       Capitalize middle to single char and use X if initial is not provided

       Args:
           emp: employee list
           index: location of middle name

       Returns:
           emp list with middle initial corrected.
       """

    for i in emp:
        # if middle initial is missing use X
        if i[index] == "":
            i[index] = "X"
        # else if initial is not single char use first char and make it capital
        elif len(i[index]) > 1:
            i[index] = i[index].__getitem__(0)
            i[index] = i.__getitem__(index).capitalize()
        # else make it capital
        else:
            i[index] = i.__getitem__(index).capitalize()

    # return to parseData
    return emp


# run main
if __name__ == '__main__':
    # print error if no argument was passed and abort the program.
    if len(sys.argv) < 2:
        print('Please enter a data.csv file as system arg')
        quit()
    else:
        # csv file
        data_file = sys.argv[1]

        # validate the file name
        if not (data_file.__eq__("data/data.csv")):
            print("Error with the data file. Aborting the program.")
            quit()

    # open file for reading
    with open(pathlib.Path.cwd().joinpath(data_file), 'r') as f:
        # read the first line and remove it
        f.readline()
        # read the rest of the file
        data = f.read().splitlines()

    employees = {}

    employees = parseData(data)

    # save the dictionary as a pickle file
    pickle.dump(employees, open('employees.pickle', 'wb'))
    # Open the pickle file for reading
    employees_pickle = pickle.load(open('employees.pickle', 'rb'))

    # Print each person
    print('\nEmployee list:\n')
    for id in employees_pickle.keys():
        employees_pickle[id].display()

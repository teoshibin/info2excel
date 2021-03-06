
### Credits ###
# by Shi Bin Teo
# https://github.com/teoshibin

### Imports ###

import os
from numpy import double
import pandas as pd
import sys, getopt
from shutil import copyfile
from openpyxl import load_workbook

### Main Functions ###

# convert delta f opt from different files into 2d array
def infoTo2dlist(dataset_folder, name, extensions, number_benchmarks):
    paths = getPaths(dataset_folder, name, extensions, number_benchmarks)
    dimensions = getDimensions(paths[0]);
    line_to_read = [x*3+2 for x in range(0, dimensions)]
    data = []

    # get data
    for i in range(0, number_benchmarks):
        a_file = open(paths[i])
        for position, line in enumerate(a_file):
            if position in line_to_read:
                data.append(line.rstrip())

    # process data (remove unnecessary data)
    for i, element in enumerate(data):
        element = element.split(', ')
        element.pop(0)
        for j, el in enumerate(element):
            element[j] = el.split('|', 1)[1]
        data[i] = element

    return data


# select certain dimension
def querySpecificDimension(data, number_benchmarks, selected_dimension_id):
    new_data = []
    number_dimensions = len(data) / number_benchmarks
    benchmark_count = 0
    for i, instances in enumerate(data):
        if i == selected_dimension_id + number_dimensions*benchmark_count:
            new_data.append(instances)
        if (i+1) % number_dimensions == 0:
            benchmark_count += 1
    return new_data


# convert 2d list to pandas dataframe
def createDataframe(datalist):
    number_instance = len(datalist[0])
    number_benchmarks = len(datalist)
    mycolumns = ['Instance ' + str(x) for x in range(1, number_instance + 1)]
    myindex = ['f' + str(x) for x in range(1, number_benchmarks + 1)]
    df = pd.DataFrame(datalist, columns=mycolumns, index=myindex)
    return df


# insert values into exisiting excel template
def generateExcel(df, path):

    copyfile(os.path.join(os.path.dirname(__file__), 'template.xlsx'), path)

    book = load_workbook(path)
    writer = pd.ExcelWriter(path, engine='openpyxl') 
    writer.book = book

    writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
    df.to_excel(writer, 'Sheet1', index=False, header=False, startcol=1, startrow=1)
    writer.save()


### Helper Functions ###

# generate all the paths to each file
def getPaths(folder, name, extensions, number_benchmarks):
    paths = []
    for i in range(1, number_benchmarks + 1):
        paths.append(os.path.join(folder, name + str(i) + extensions))
    return paths


# get total number of dimensions
def getDimensions(path):
    return  int(countLine(path) / 3)


# count number of lines in file
def countLine(path):
    file = open(path, "r")
    line_count = 0
    for line in file:
        if line != "\n":
            line_count += 1
    file.close()
    return line_count


# main function
def main(argv):

    ### Main Parameters ###
    ## benchmarks ##
    dimensions = [2, 3, 5, 10 , 20, 40]
    number_benchmarks = 24
    dimension = 5
    minimum_delta = 1e-14
    maximum_delta = 1e+3

    ## preset IO folder name ##
    dir = os.path.dirname(__file__) # path = ./
    dataset_folder = os.path.join(dir, os.pardir, 'Datasets') # path = ../Datasets/[actual datasets]
    output_folder = os.path.join(dir, os.pardir, 'ExcelScore') # path = ../ExcelScore/[excels]
    algorithm_name = ''
    excelname = ''

    ### Main script ###
    ## error msg ##
    wrong_syntax_msg = ('info2excel.py -i [ALGONAME] -d [DIMENSION] -o [EXCELNAME] -u [UPPER_BOUND] -l [LOWER_BOUND]\n'
                        'info2excel.py -i [ALGONAME]\n')
    wrong_dimensions_msg = '--dimension not found in' + str(dimensions)

    ## parse in args ##
    try:
        opts, args = getopt.getopt(argv,"i:d:u:l:o:",["ifile=", "dimension=", "ofile=", "upperbound=", "lowerbound="])
    except getopt.GetoptError:
        print(wrong_syntax_msg)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            algorithm_name = arg
        elif opt in ("-d", "--dimension"):
            dimension = abs(int(arg))
        elif opt in ("-u", "--upperbound"):
            maximum_delta = abs(double(arg))
        elif opt in ("-l", "--lowerbound"):
            minimum_delta = abs(double(arg))
        elif opt in ("-o", "--ofile"):
            excelname = arg
    
    ## validation ##
    if len(algorithm_name) == 0:
        print(wrong_syntax_msg)
        sys.exit(2)

    if not(dimension in dimensions):
        print(wrong_dimensions_msg)
        sys.exit(2)

    if len(excelname) == 0:
        excelname = algorithm_name + '_' + str(dimension) + 'D'

    ## data retrieval ##
    full_dataset_path = os.path.join(dataset_folder, algorithm_name)
    full_output_path = os.path.join(output_folder, excelname + '.xlsx')

    data = infoTo2dlist(full_dataset_path, 'bbobexp_f', '.info', number_benchmarks)
    data = querySpecificDimension(data, number_benchmarks, dimensions.index(dimension))

    data = double(data) # convert string to double
    df = createDataframe(data)
    
    print("\n\n=== Raw Data ===\n")
    print(df)

    df.where(df >= minimum_delta, minimum_delta, inplace=True)
    df.where(df <= maximum_delta, maximum_delta, inplace=True)
    # when df <= maximum_delta then do not replace
    # when df > maximum_delta then replace with maximum_delta
    
    print("\n\n=== Manipulated Data ===\n")
    print(df)

    # data output
    generateExcel(df, full_output_path)

if __name__ == "__main__":
    main(sys.argv[1:])
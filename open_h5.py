#!/usr/bin/env python


'''

Read a CanSAS file and extracts a dictionary per each sas_entry.
Per each sas_entry produces another dictionary that relates each data set observable with the corresponding data. 

e.g.

in a python shell:

import open_h5 as oh
x = oh.main("a_cansas_file.h5")
print x
print x['entry01']


'''

# to continue:
# extract sas_entry from file
# optimise script
# rename functions

import tables
import os
import numpy as np
import h5py
import sys
import numpy as np


def CanSAS_file_exists(file_to_read):
    if os.path.isfile(file_to_read):
        return True
    else:
        print "File %s not found"%(file_to_read)

def h5_get_structure(file_to_read):
    h5file = tables.open_file(file_to_read, driver="H5FD_CORE")
    content_h5 = str(h5file)
    h5file.close()
    return content_h5    

def dsets_extract(content_h5):
    content_split = content_h5.split("\n")
    dsets_in_file = []
    for item in content_split:
        if "Array" in item:
            dsets_in_file.append(item.split(" ")[0])
    return dsets_in_file

def dsets_id_extract(content_h5):
    content_split = content_h5.split("\n")
    dsets_id = []
    for item in content_split:
        if "Array" in item:
            dsets_id.append(item.split(" ")[0].split('/')[-1])
    return dsets_id    
    
def shapes_extract(content_h5):
    content_split = content_h5.split("\n")
    shape_dsets = []
    for item in content_split:
        if "Array" in item:
            shape_dsets.append(item.split("Array")[1].split("(")[1].split(")")[0])
    return shape_dsets

def data_extract(file_to_read = '', dset_name = ''):
    f = h5py.File(file_to_read,'r')
    data = f[dset_name][:]
    f.close()
    return data
    
def file_structure_print(file_to_read):
    content_h5 = h5_get_structure(file_to_read)
    list_of_dsets = dsets_extract(content_h5)
    dsets_in_file = []
    for i,item in enumerate(list_of_dsets):
        dsets_in_file.append(item)

def dictionary_dset_data(list_of_dsets = [],list_of_data = []):
    if len(list_of_dsets) == len(list_of_data):
        dictionary_dset_data = dict(zip(list_of_dsets, list_of_data))
        return dictionary_dset_data
    else:
        print "number of datasets and data do not coincide"
    
def dictionary_global(entries = ['entry01'],dictionary_data_h5 = [{},{}]):       
    total_dictionary = {}
    for i, item in enumerate(entries):
        total_dictionary[item] = dictionary_data_h5[i]
    
    return total_dictionary

def main(file_to_read):

    if CanSAS_file_exists(file_to_read):

        content_h5 = h5_get_structure(file_to_read)
        list_of_dsets = dsets_extract(content_h5)
        list_of_dsets_id = dsets_id_extract(content_h5)
        list_of_shapes = shapes_extract(content_h5)
        list_of_data = []

        for i,item in enumerate(list_of_dsets):
            list_of_data.append(data_extract(file_to_read, item))

        dictionary_data = dictionary_dset_data(list_of_dsets_id, list_of_data)
        dictionary_list = [dictionary_data,{}]
        complete_dictionary = dictionary_global(['entry01'], dictionary_list)  # need to extract these entries from the file_to_read

        print "dictionary created"
        #print complete_dictionary
        return complete_dictionary
    else:
        print "Could not do it. Check main() or the file you introduced."


def print_files_available():
        
        print "Files available:"
        for i,filenames in enumerate(os.listdir(os.getcwd())):            
            if filenames.endswith(".hdf5"):
                print filenames
            if filenames.endswith('.h5'):
                print filenames
        return filenames
        
if __name__ == '__main__':
    
    if len(sys.argv) == 1:
        print_files_available()        
        file_to_read = raw_input("Write file to read: ")
        main(file_to_read)

    if len(sys.argv) == 2:
        file_to_read = sys.argv[1]
        if os.path.isfile(file_to_read):
            main(file_to_read)
        else:
            print "File %s not found."%file_to_read
            file_to_read = raw_input("Write file to read: ")
            if os.path.isfile(file_to_read):
                main(file_to_read)
            

            

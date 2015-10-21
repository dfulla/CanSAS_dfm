#!/usr/bin/env python


'''

Read a CanSAS file and extracts a dictionary per each sas_entry.
Per each sas_entry produces another dictionary that relates each data set observable with the corresponding data. 

e.g.

in a python shell:

import open_h5_class as oh
x = oh.DictionaryH5(file_to_read).write_dictionary_h5("")
print x
print x['entry01']
print x['entry01']['I']


'''

# to continue:
# extract sas_entry from file
# optimise script
# rename functions
# Check if shapes are correct
# include entry01 automatic
# lacks magnetic field

import tables
import os
import numpy as np
import h5py
import sys


class H5Extractor:

    def __init__(self, file_to_read):
        self.file_to_read = file_to_read
         
    def CanSAS_file_exists(self, file_to_read):
        if os.path.isfile(self.file_to_read):
            return True
        else:
            print "File %s not found"%(self.file_to_read)
        
    def h5_get_structure(self, file_to_read):
            h5file = tables.open_file(self.file_to_read, driver="H5FD_CORE")
            content_h5 = str(h5file)
            h5file.close()
            return content_h5    

    def dsets_extract(self, content_h5):
            content_split = content_h5.split("\n")
            dsets_in_file = []
            for item in content_split:
                if "Array" in item:
                    dsets_in_file.append(item.split(" ")[0])
                    
            return dsets_in_file

    def dsets_id_extract(self, content_h5):
            content_split = content_h5.split("\n")
            dsets_id = []
            for item in content_split:
                if "Array" in item:
                    dsets_id.append(item.split(" ")[0].split('/')[-1])
            
            return dsets_id    
    
    def shapes_extract(self, content_h5):
            content_split = content_h5.split("\n")
            shape_dsets = []
            for item in content_split:
                if "Array" in item:
                    shape_dsets.append(item.split("Array")[1].split("(")[1].split(")")[0])
            return shape_dsets
        
    def data_extract(self, file_to_read, dset_name):
            f = h5py.File(self.file_to_read,'r')
            data = f[dset_name][:]
            f.close()
            return data
    
    def file_structure_print(self, file_to_read): #not being used?
            content_h5 = h5_get_structure(file_to_read)
            list_of_dsets = dsets_extract(content_h5)
            dsets_in_file = []
            for i,item in enumerate(list_of_dsets):
                dsets_in_file.append(item)

    def dictionary_dset_data(self, list_of_dsets = [],list_of_data = []):
            if len(list_of_dsets) == len(list_of_data):
                dictionary_dset_data = (zip(list_of_dsets, list_of_data))
                return dictionary_dset_data
            else:
                print "number of datasets and data do not coincide"
    
    def dictionary_global(self, entries = ['entry01','entry02'],dictionary_data_h5 = [{},{}]):
            total_dictionary = {}
            for i, item in enumerate(entries):
                total_dictionary[item] = dictionary_data_h5[i]
            
            return total_dictionary

class DictionaryH5(H5Extractor):
    def write_dictionary_h5(self,file_to_read):
        self.CanSAS_file_exists(file_to_read)
        content_h5 = self.h5_get_structure(file_to_read)
        list_of_dsets = self.dsets_extract(content_h5)
        list_of_dsets_id = self.dsets_id_extract(content_h5)
        self.shapes_extract(content_h5)
        list_of_data = []
        for i,item in enumerate(list_of_dsets):
            list_of_data.append(self.data_extract(file_to_read, item))
        
        dictionary_data = self.dictionary_dset_data(list_of_dsets_id, list_of_data)
        dictionary_list = [dictionary_data,{}]
        complete_dictionary = self.dictionary_global(['entry01','entry02'], dictionary_list)
        return complete_dictionary

        
if __name__ == '__main__':

    if len(sys.argv) == 1:
        file_to_read = raw_input("Write file to read: ")
        DictionaryH5(file_to_read).write_dictionary_h5("")
    
        
    if len(sys.argv) == 2:
        file_to_read = sys.argv[1]
        if os.path.isfile(file_to_read):
            DictionaryH5(file_to_read).write_dictionary_h5("")
        
        else:
            print "here"
            print "File %s not found."%file_to_read
            file_to_read = raw_input("Write file to read: ")
            if os.path.isfile(file_to_read):
                DictionaryH5(file_to_read).write_dictionary_h5("")
                
            

            

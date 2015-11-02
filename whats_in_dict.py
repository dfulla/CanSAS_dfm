import open_h5 as oh
import os
import numpy as np

def print_files_available():
        
        print "Files available:"
        files_h5 = []
        for i,filenames in enumerate(os.listdir(os.getcwd())):            
            if filenames.endswith(".hdf5"):
                files_h5.append(filenames)
            if filenames.endswith('.h5'):
                files_h5.append(filenames)
        return files_h5

def which_file():

    print_h5_files = print_files_available()
    print print_h5_files
    
    file_to_read = raw_input("Introduce file to read (file.h5): ")

    if file_to_read =='':
        if len(print_h5_files) != 0:
            print 'Loading file %s by default'%print_h5_files[0]
            print print_h5_files
            file_to_read = print_h5_files[0]
           
    
    if file_to_read.find('.h5') == -1 and file_to_read.find('.hdf5') == -1:
        print 'File %s has no .h5 nor .hdf5 extensions.'%file_to_read
        file_to_read = raw_input("Introduce file to read (file.h5): ")
        print file_to_read


    return file_to_read

def make_dict():

    file_to_read = which_file()        
    dictionary = oh.main(file_to_read)

    if dictionary != None:

        all_dictionary = dictionary.keys()

        #print all_dictionary
        
        first_entry = dictionary.get('entry01')
        return first_entry

    else:
        print 'Dictionary was not produced'

def get_parameters(index_M,index_Ix,index_Iy):

    first_entry = make_dict()
    
    Qx = first_entry.get('Qx')
    Qy = first_entry.get('Qy')
    Qz = first_entry.get('Qz')
    I = first_entry.get('I')
    M = first_entry.get('M')
    C = [I, M, Qx, Qy, Qz]


    print "I  =  %f"%C[0][index_M][index_Ix][index_Iy]
    print "M  = %f"%C[1][index_M]
    print "Qx = %f"%C[2][index_Ix][index_Iy]
    print "Qy = %f"%C[3][index_Ix][index_Iy]
    print "Qz = %f"%C[4][index_Ix][index_Iy]
    return C


def get_keys():
        
    first_entry = make_dict()
    return first_entry, first_entry.keys()

def get_type(object):
        if type(object) == np.ndarray:
                return object.shape, object.size
        else:
                type_object = str(object)
                print '%s not an array'%type_object
    
if __name__ == '__main__':
    
    #get_parameters(0,60,100)
    keys = get_keys()
    print keys[1]
    
    for i, key in enumerate(keys[1]):
            one_key = keys[1][i]
            #get_type(one_key)
            key_length = len(keys[0].get(one_key))
            get_type(keys[0].get(one_key))
            shape = str(get_type(keys[0].get(one_key))[0])
            size = str(get_type(keys[0].get(one_key))[1])
            print '%s has shape %s and size %s'%(one_key, shape, size)

            

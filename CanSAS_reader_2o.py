
import numpy as np
import h5py

'''

### script under development ###

User writes 3 inputs:
1) name of an h5 or hdf5 file with a CanSAS structure (e.g. "generic2dtimetpseries.h5" )
2) path to a dataset (e.g. "sasentry01/sasdata01")
3) set of parameters (e.g. (2,2,1,0,0))

Script returns a dictionary with the data corresponding to the parameters input from the user.

Under development:

- UNDER DEVELOPMENT: Return errors/warnings when the file structure is not correct
- ONGOING: Script needs to be tested
- Develop a script that scans all possible values and check their types

instruction to execute (2 object):

in python:

from CanSAS_reader_2o import CANSASDATA     #####
x = CANSASDATA('generic2dtimetpseries.h5')
print x('sasentry01/sasdata01', (2,2,1,0,0))

'''


class INFOEXTRACTOR(object):

    def __init__(self, file_to_read):
        
        self.file_to_read = file_to_read
        self.subgroup =self. get_subgroups()

    def open_h5_file(self):
        self.f = h5py.File(self.file_to_read,  "r")
        return self.f

    def get_subgroups(self):
        self.open_h5_file()
        maingroup = self.f['/']
        groups = []
        subgroup = []
        
        for group in maingroup:
            groups.append(group)
        for item in groups:

            for member in self.f['/%s'%item]:
                subgroup.append('%s/%s'%(item,member))

        self.groups = groups
        self.subgroup = subgroup
        return self.subgroup

    def get_observables(self):

        self.dict_observables = {}
        self.dict_observables_path = {}

        for sub in self.subgroup:

            self.list_observables = []
            self.list_observables_path = []

            for item in self.f[sub]:

                self.list_observables.append(item)
                self.list_observables_path.append('%s/%s'%(sub,item))

            self.dict_observables[sub] = self.list_observables
            self.dict_observables_path[sub] = self.list_observables_path

        return self.list_observables_path

    def get_subgroup_attributes(self):

        self.dict_all_subgroups_attributes = {}
        self.dict_subgroups_attributes = {}

        for sub in self.subgroup:
        
            for member in self.f[sub].attrs:

                self.dict_subgroups_attributes[member] = self.f[sub].attrs.__getitem__(member)
            self.dict_all_subgroups_attributes[sub] = self.dict_subgroups_attributes

        return self.dict_all_subgroups_attributes

    def get_observable_attributes(self):

        self.get_observables()
        self.dict_observables_attributes = {}
        self.dict_subgroups_observables_attributes = {}

        for sub in self.subgroup:

            self.dict_observables_attributes = {}

            for item in self.dict_observables[sub]:

                dict = {}
                observable_path = '%s/%s'%(sub,item)
                dict['units'] = self.f[observable_path].attrs.__getitem__('units')
                self.dict_observables_attributes[item] = dict

            self.dict_subgroups_observables_attributes[sub] = self.dict_observables_attributes

    def get_data_dsets(self,path):

        sasentry = path.split('/')[0]
        sasdata = path.split('/')[1]

        self.get_observables()
        self.dict_data_dsets2 = {}
        self.dict_data_dsets = []
        self.dict_data_dsets3 = {}   # restructure dictionary
        self.dict_data_dset4 = {}
        self.delivery_dict = {}

        for sub in self.subgroup:

            for item in self.dict_observables_path[sub]:

                dict = {}
                values = []

                for data in self.f[item]:

                    self.dict_data_dset4[item] = data
                    values.append(data)

                dict[item] = np.array(values)

                self.dict_data_dsets.append(dict)

            self.dict_data_dsets2[sub] = self.dict_data_dsets

        for element in self.groups:

            list_subgroups_per_group = []
            for sub in self.subgroup:

                for concept in sub.split('/'):
                    if element in concept:
                        list_subgroups_per_group.append(sub)

            self.dict_data_dsets3[element] = list_subgroups_per_group

        for key in self.dict_data_dset4.keys():

            if '%s/%s'%(sasentry,sasdata) in key:

                self.delivery_dict[key] = self.dict_data_dset4[key]

        try:
            return self.dict_data_dsets2[path][0]['%s/I'%path].shape

        except:

            return self.delivery_dict['%s/I'%path].shape

    def object_assembler(self,path):

        self.open_h5_file()
        self.get_subgroup_attributes()
        self.get_observables()
        self.get_observable_attributes()
        self.get_data_dsets(path)
        self.main_object_list = [self.subgroup, self.dict_observables, self.dict_observables_path, self.dict_subgroups_attributes, self.dict_subgroups_observables_attributes ,self.dict_data_dsets2,self.delivery_dict]

        return self.main_object_list

    def input_parameters(self,path):   # parameters to input, better name?
        self.object_assembler(path)

        axes = self.main_object_list[3]
        for item in axes:
            if 'I_axes' in item:
                self.I_axes = []
                
                if type(axes[item]) == np.ndarray:
                    for element in axes[item]:
                        self.I_axes.append(element)

                if type(axes[item]) == str:
                    
                    if axes[item].split(',') > 1:
                        for element in axes[item].split(','):
                            self.I_axes.append(element)

                return self.I_axes


class CANSASDATA(object):

    def __init__(self, file_to_read):
        self.file_to_read = file_to_read

    def __call__(self, sasentry, sasdata ,given_parameters):

        self.path = '%s/%s'%(sasentry,sasdata)

        self.given_parameters = given_parameters

        self.I_axes = INFOEXTRACTOR(self.file_to_read).input_parameters(self.path)
        the_shape = INFOEXTRACTOR(self.file_to_read).get_data_dsets(self.path)

        print 'I_axes: %s. Insert %i parameters with shape: %s'%(self.I_axes,len(self.I_axes),the_shape)

        # it allows user to correct wrong input parameters (only once)

        if len(self.I_axes) != len(self.given_parameters):

            print 'ERROR: given %i parameters (%s) but allowed parameters %i'%(len(self.given_parameters),self.given_parameters,len(self.I_axes))
            new_parameters = raw_input('Introduce %i parameters e.g. (0,0...0))\n'%len(self.I_axes))
            self.given_parameters = ()
            for element in new_parameters:

                try:
                    int(element)
                    self.given_parameters = self.given_parameters + (int(element),)

                except:
                    pass

        self.verify_input()
        self.main_object_list = INFOEXTRACTOR(self.file_to_read).object_assembler(self.path)
        self.list_observables_path = INFOEXTRACTOR(self.file_to_read).get_observables()

        return self.get_I_value(self.path,self.given_parameters)


    def verify_input(self):

        self.I_axes = INFOEXTRACTOR(self.file_to_read).input_parameters(self.path)

        if len(self.I_axes) == len(self.given_parameters):

            the_shape = INFOEXTRACTOR(self.file_to_read).get_data_dsets(self.path)
            for i,element in enumerate(the_shape):
                if element <= self.given_parameters[i]:
                    print 'ERROR: Given parameter %i should be smaller than %i'%(self.given_parameters[i],element)

                else:
                    pass

            return self.given_parameters

    def get_I_value(self, path, given_parameters):

        self.main_object_list = INFOEXTRACTOR(self.file_to_read).object_assembler(path)
        self.dict_subgroups_observables_attributes = self.main_object_list[4]
        self.delivery_dict = self.main_object_list[6]
        self.dict_data_dset2 = self.main_object_list[5]

        #print self.delivery_dict
        #print self.delivery_dict
        self.dict_all_subgroups_attributes = INFOEXTRACTOR(self.file_to_read).get_subgroup_attributes()

        dict_return = {}
        dict_parameters = {}

        for k,parameter in enumerate(self.given_parameters):

            dict_parameters['%s:%i'%(self.I_axes[k],k)] = self.given_parameters[k]

        # extracting I ####

        for i,item in enumerate(self.given_parameters):

            if '%s/I'%path in self.main_object_list[2][path]:

                value_I = self.dict_data_dset2[path]#['%s/I'%path]

                for k, thing in enumerate(value_I):

                    if '%s/I'%path in thing:
                        value_I = value_I[k]['%s/I'%path]


                j = 0
                for t in range(len(value_I.shape)):

                    value_I = value_I[self.given_parameters[j]]

                    j = j+1

                unit = self.dict_subgroups_observables_attributes[path]['I']
                dict_return['I'] = {'%f'%value_I: '%s'%unit}

            if '%s/I'%path not in self.main_object_list[2][path]:
                print 'ERROR: No intensity in data selected.'

        # working the Q problem

        dict_q_dset = {}
        dict_q_axes = {}

        for i, item in enumerate(self.main_object_list[2][path]):

            if self.main_object_list[2][path][i].split('/')[-1][0] == 'Q':
                dict_q_dset['%s:%i'%(self.main_object_list[2][path][i],i)] = self.main_object_list[2][path][i].split('/')[-1]

        number_of_q = self.I_axes.count('Q')
        #print 'number of q is : %i'%number_of_q

        for i,item in enumerate(self.I_axes):

            if item == 'Q':
                dict_q_axes['%s_index:%i'%(item, i)] = '%s_parameter:%i'%(item,self.given_parameters[i])


        for dict in self.main_object_list[5][path]:

            if dict.keys()[0] == '%s/Q'%path:

                value_Q = dict['%s/Q'%path]
                for i,element in enumerate(value_Q.shape):

                    index_of_q = self.dict_all_subgroups_attributes[path]['Q_indices'][i]
                    value_Q = value_Q[self.given_parameters[index_of_q]]

                self.value_Q = value_Q

        # specific case of Qx,Qy,Qz

        if 'Qx' in self.main_object_list[1][path]:

            for item in dict_q_dset:

                one_q = dict_q_dset.get(item)
                q_first_index = int(dict_q_axes.get('Q_index:1').split(':')[-1])
                q_second_index = int(dict_q_axes.get('Q_index:2').split(':')[-1])

                for i,elements in enumerate(self.main_object_list[5][path]):

                    one_q = dict_q_dset.get(item)
                    if '%s/%s'%(path,one_q) in self.main_object_list[5][path][i]:

                        unit = self.dict_subgroups_observables_attributes[path][one_q]
                        dict_return['%s'%one_q] = {'%f'%self.main_object_list[5][path][i]['%s/%s'%(path,one_q)][q_first_index][q_second_index]:'%s'%unit}

        # extracting the rest of the parameters

        for i,item in enumerate(self.given_parameters):

            if '%s/%s'%(path,self.I_axes[i]) in self.main_object_list[2][path]:

                for j, dicts in enumerate(self.main_object_list[5][path]):
                    if dicts.keys()[0] == '%s/%s'%(path,self.I_axes[i]):
                        value = self.main_object_list[5][path][j]['%s/%s'%(path,self.I_axes[i])]
                        unit = self.dict_subgroups_observables_attributes[path][self.I_axes[i]]

                        for key in dict_parameters.keys():

                            if key.split(':')[0] == self.I_axes[i]:

                                if self.I_axes[i][0] != 'Q':
                                    dict_return[self.I_axes[i]] = {'%f'%value[dict_parameters[key]]:'%s'%unit}
                                else:
                                    # under development:
                                    dict_return[self.I_axes[i]] = {'%s'%self.value_Q:'%s'%unit}



        print ''
        for key, value in dict_return.items():
            print key, value
        print ''

        return dict_return



x = CANSASDATA('generic2dtimetpseries.h5')
print x('sasentry01','sasdata01',(0,0,0,0,0))

#x = CANSASDATA('D2O_100pc_two_entries.hdf5')
#print x('sasentry02','sasdata01',(1,0,0))



# problems (challenges) of file generic2dtimetpseries.h5. This can be used to rise errors or warnings:

# problem 1 - Q_indices are (1,3,4) but:
#                                        Q matrix has shape 7x3x3
#                                        Range of the first index should be 7
#                                        index 1 corresponds to time (Time_indices = 1), that has range 3
#           -solution: Q_indices should be (0,3,4). 0 corresponds to Temperature and temperature has range 7.

# problem 2 - some units are wrong. Units for Pressure, Temperature and Time are all ms (milliseconds)

# problem (or challenge) 3 - I_axes are given in this file as a list. Other files like D2O_100pc_two_entries.hdf5 I_axes are given as a numpy array.
# I have solved this problem by converting all I_axes into a list but I could expect other formats (dictionaries, tuples etc...)


# problems (challenges) of file D2O_100pc_two_entries.hdf5
# I have generated this file to allow arbitrary number of entries and datasets. This is necessary to allow reading from a general file structure

# problem 1. Values of Q in I_axes do not correspond to name of datasets Qx,Qy,Qz. Working on how to relate Qs and Qx,y,z


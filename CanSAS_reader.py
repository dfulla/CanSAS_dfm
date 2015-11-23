
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

- split the current structure into two objects
- Reading of Q values or Qx,Qy,Qz values need to be implemented
- Return errors/warnings when the file structure is not correct
- Propose user number of possible parameters and range
- Script needs to be tested
- Develop a script that scans all possible values and check their types



instruction to execute:

in python:

from CanSAS_reader import CANSASDATA
x = CANSASDATA('generic2dtimetpseries.h5','sasentry01/sasdata01', (2,2,1,0,0))
print x()

'''


class CANSASDATA(object):

    def __init__(self, file_to_read,a,b):
        
        self.file_to_read = file_to_read
        self.subgroup =self. get_subgroups()
        self.a = a
        self.b = b

    def __call__(self):

        return self.get_I_value(self.a,self.b)

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

    def get_subgroup_attributes(self):

        self.dict_all_subgroups_attributes = {}
        self.dict_subgroups_attributes = {}

        for sub in self.subgroup:
        
            for member in self.f[sub].attrs:
                self.dict_subgroups_attributes[member] = self.f[sub].attrs.__getitem__(member)
            self.dict_all_subgroups_attributes[sub] = self.dict_subgroups_attributes

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

    def get_data_dsets(self):
        self.get_observables()
        self.dict_data_dsets2 = {}

        for sub in self.subgroup:

            self.dict_data_dsets = []
            for item in self.dict_observables_path[sub]:
                dict = {}
                values = []
                for data in self.f[item]:
                    values.append(data)

                dict[item] = np.array(values)
                self.dict_data_dsets.append(dict)

            self.dict_data_dsets2[sub] = self.dict_data_dsets

    def object_assembler(self):
        self.open_h5_file()
        self.get_subgroup_attributes()
        self.get_observables()
        self.get_observable_attributes()
        self.get_data_dsets()
        self.main_object_list = [self.subgroup, self.dict_observables, self.dict_observables_path, self.dict_subgroups_attributes, self.dict_subgroups_observables_attributes ,self.dict_data_dsets2]

    def input_parameters(self):   # parameters to input, better name?
        self.object_assembler()

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
                        
                print 'I_axes: %s. Insert %i parameters'%(self.I_axes,len(self.I_axes))


    def get_parameter_indices(self):

        for item in self.I_axes:  # is this function necessary?
            indices = '%s_indices'%item

    def check_given_parameters(self):

        self.input_parameters()
        self.get_parameter_indices() # decide where to call it
    
        if len(self.given_parameters) != len(self.I_axes):
            print 'ERROR: need %i parameters. Got %i parameters instead'%(len(self.I_axes),len(self.given_parameters),)

        else:

            for i,data in enumerate(self.main_object_list[5]):
                if 'I' in self.list_observables_path[i]:
                    for j, parameter in enumerate(data[self.list_observables_path[i]].shape):
                        if parameter <= self.given_parameters[j]:
                            print 'ERROR: input %s and maximum should be %s'%(self.given_parameters,data[self.list_observables_path[i]].shape)

    def get_I_value(self, a, given_parameters):

        self.given_parameters = given_parameters
        self.object_assembler()   #?
        self.input_parameters()
        self.get_parameter_indices()
        dict_return = {}
        print self.given_parameters
        dict_parameters = {}

        for k,parameter in enumerate(self.given_parameters):
            dict_parameters['%s:%i'%(self.I_axes[k],k)] = self.given_parameters[k]

        # for I ####

        for i,item in enumerate(self.given_parameters):

            if '%s/I'%a in self.main_object_list[2][a]:
                value_I = self.main_object_list[5][a][0]['%s/I'%a] #[self.main_object_list[2][a]]

                for j,index in enumerate(self.given_parameters):
                    value_I = value_I[self.given_parameters[j]]

                unit = self.dict_subgroups_observables_attributes['%s'%a]['I']
                dict_return['I'] = {'%f'%value_I: '%s'%unit}

        for i,item in enumerate(self.given_parameters):

            if '%s/%s'%(a,self.I_axes[i]) in self.main_object_list[2][a]:

                for j, dicts in enumerate(self.main_object_list[5][a]):
                    if dicts.keys()[0] == '%s/%s'%(a,self.I_axes[i]):
                        value = self.main_object_list[5][a][j]['%s/%s'%(a,self.I_axes[i])]
                        unit = self.dict_subgroups_observables_attributes[a][self.I_axes[i]]['units']

                        for key in dict_parameters.keys():

                            if key.split(':')[0] == self.I_axes[i]:
                                if self.I_axes[i] != 'Q':
                                    dict_return[self.I_axes[i]] = {'%f'%value[dict_parameters[key]]:'%s'%unit}

                                else:
                                    dict_return[self.I_axes[i]] = {'no value yet. working on it':'%s'%unit}



        print ''
        for key, value in dict_return.items():
            print key, value
        print ''

        return dict_return



#a_point = CANSASDATA('D2O_100pc_two_entries.hdf5', 'sasentry01/sasdata01',(1,0,0))

a_point = CANSASDATA('generic2dtimetpseries.h5','sasentry01/sasdata01', (2,2,1,0,0))
print 'this is just an example:'
print a_point()

#.get_I_value('sasentry01/sasdata01',(0,0,0,0,0))



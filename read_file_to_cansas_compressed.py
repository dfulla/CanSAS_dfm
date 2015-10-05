import numpy as np
import h5py
import os
import sys
import inspect
import traceback
import time


'''
Reads and extracts data from one reduced experimental SAXS file (H2O_100pc_2D_0.051kG.ABS). 
Creates a new hdf5 file with CanSAS format (H2O_100pc_2D_0.051kG.ABS.hdf5).   
Writes the information from the experimental file to the hdf5-CanSAS file.

'''



#files:

path = "/home/marsa/Desktop/files CANSAS test/"

#file1 = path + "D2O_100pc_2D_0.051kG.ABS"
#file2 = path + "D2O_100pc_2D_15_5kG.ABS"
file3 = path + "H2O_100pc_2D_0.051kG.ABS"
#file4 = path + "H2O_100pc_2D_15.5kG.ABS"

file_to_convert = file3.split("/")[-1]

FILE_TIMESTAMP = time.strftime("%Y-%m-%dT%H:%M:%S")
FILE_TIMESTAMP += '%+03d%02d' % (-time.timezone/60/60, abs(time.timezone/60) % 60)
FILE_PRODUCER = "canSAS"

class ExampleFile:

	def __init__(self, name, **keywords):
		#self.name = name
		self.name = "%s.hdf5"%file_to_convert
		self.keywords = keywords

	def createFile(self):
		self.f = h5py.File(self.name, "w")
		self.f.attrs['file_name'] = self.name
		self.f.attrs['file_time'] = FILE_TIMESTAMP
		self.f.attrs['producer'] = FILE_PRODUCER

	def closeFile(self):
		self.f.close()

	def createEntry(self, name):
		self.sasentry = self.f.create_group(name)
		self.sasentry.attrs["NX_class"] = "SASentry"
		self.sasentry.attrs["version"] = "1.0"
	
	def createTitle(self, title):
		self.sasentry.create_dataset('Title', (), data=title)
	
	def createData(self, name, qi, ii, mi=None, attributes=None):
		self.sasdata = self.sasentry.create_group(name)
		self.sasdata.attrs["NX_class"] = "SASdata"
		self.sasdata.attrs["Q_indices"] = qi
		self.sasdata.attrs["I_axes"] = ii
		if mi != None:
			self.sasdata.attrs["Mask_indices"] = mi
		if attributes != None:
			for key in attributes.keys():
				self.sasdata.attrs[key] = attributes[key]

	def createDataSet(self, name, array, attributes=None):
		ds = self.sasdata.create_dataset(name, array.shape, data=array)
		if attributes != None:
			for key in attributes.keys():
				ds.attrs[key] = attributes[key]


# reads experimental file

def file_r(exp_file = file_to_convert):

    file_open = (open(exp_file).readlines())
    return exp_file,file_open

# extracts and return data from columns

def get_columns(file_content = ""): 
    
    start_columns = file_content.index("Data columns are Qx - Qy - I(Qx,Qy) - err(I) - Qz - SigmaQ_parall - SigmaQ_perp - fSubS(beam stop shadow)\r\n")
    data_columns = file_content[start_columns+4:]    
    Qx, Qy, I, err_I, Qz, SigmaQ_parall, SigmaQ_perp, fSubS = [],[],[],[],[],[],[],[]
	
    for line in data_columns:
	column_split = line.split("\t")
    	Qx.append(column_split[0])
	Qy.append(column_split[1])
	I.append(column_split[2])
	err_I.append(column_split[3])
	Qz.append(column_split[4])
	SigmaQ_parall.append(column_split[5])
	SigmaQ_perp.append(column_split[6])
	fSubS.append(column_split[7].split("\r\n")[0])
        
    return Qx, Qy, I, err_I, Qz, SigmaQ_parall, SigmaQ_perp, fSubS

def list_to_np(a_list = []):

   import numpy as np
   Qx_np = np.asarray(a_list)
   return Qx_np
   
def createFile(self):
    self.f = h5py.File(self.name, "w")
    self.f.attrs['file_name'] = self.name
    self.f.attrs['file_time'] = FILE_TIMESTAMP
    self.f.attrs['producer'] = FILE_PRODUCER
   
def main(exp_file = file_to_convert):

    #text = file_r(exp_file)
    text = file_r(exp_file)
    
    name_of_file = text[0]
    content_of_file = text[1]
    data_in_columns = get_columns(content_of_file)
    Qx_data = data_in_columns[0]
    Qy_data = data_in_columns[1]
    
    return list_to_np(Qx_data), list_to_np(Qy_data)

if __name__ == "__main__":
  
    file1 = "H2O_100pc_2D_0.051kG.ABS"
    #file2 = "D2O_100pc_2D_15_5kG.ABS"
    
    list_of_files = [file1]
    for file_i in list_of_files:
      print file_i
      print main(file_i)
     
      Qx_h5 = main()[0]
      Qy_h5 = main()[1]
    
      print Qx_h5.shape
      print type(Qy_h5)==type(np.random.rand(100,))
  
      class ConvertCansas(ExampleFile):
        def write(self):  
		self.createFile()
		self.createEntry("sasentry01")
		self.createData("sasdata01_%s"%file_i, np.array([0]), "Q")
		print "sasdata01_%s"%file_i
		self.createDataSet("Qx", Qx_h5, {"units": "1/A"})
		self.createDataSet("I", np.random.rand(100,), {"units": "1/cm"})
		self.createDataSet("Qy", Qy_h5, {"units": "1/A"})
		self.closeFile()

      ConvertCansas(ExampleFile).write()

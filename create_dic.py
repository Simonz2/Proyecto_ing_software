import json
import os

class CreateDict:

    def __init__(self):
        self.path=r"data/paths.json"
        self.data_directory=r"data"

        if os.path.exists(self.path):
            self.dic=json.load(open(self.path))    
        
        else:
            self.dic={}
            self.get_paths()
            self.save_dic()
        


    def get_paths(self):#get the paths for all the files on the data directory, and append them to the dictionary
        if os.path.exists(self.data_directory):
            files=os.listdir(self.data_directory)
            for f in files:
                a=f.split(r".")[0]
                if a!=r"paths":
                    paths=os.path.join(self.data_directory,f)
                    self.dic[a]=paths
    
    def save_dic(self):#save self.dic to a json file
        if os.path.exists(self.path):
            os.remove(self.path)
        json.dump(self.dic,open(self.path,"w"))
    
    def update_dic(self,key,value):#update or add a new key to the dic and save the dic
        self.dic[key]=value
        self.save_dic
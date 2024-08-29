from create_dic import CreateDict
import pandas as pd
import os

class PathsFinder:
    def __init__(self):
        self.dic_creator=CreateDict()
        self.file_path=self.dic_creator.dic.get("save_paths")#get the path for file that stores folder paths
        self.df=pd.read_csv(filepath_or_buffer=self.file_path,sep=";")#read dataframe containing dates, 
        self.df["Date"]=pd.to_datetime(self.df["Date"]).dt.date#transform the data column into proper type

    def get_file_path(self,date):
        try:
            if date is None:#if date is not in dataframe
                raise Exception
            else:#if data is in dataframe
                self.date=pd.to_datetime(date).date()#set the date into suitable type yyyy-mm-dd
                self.folder_path=self.df.loc[self.df["Date"]==self.date,"Path"]#get the first path

                return self.folder_path.iloc[0]#return path
        except Exception as e:
            raise ValueError("Error parsing date: {}".format(e))
    
    def save_folder_path(self,date,folder):#append a new path 
        self.date=pd.to_datetime(date).date()#convert and normalize the date
        self.folder_path=folder#path to the folder
        new_row={"Date":self.date,"Path":self.folder_path}#perpare the new row with date and path
        self.df.loc[len(self.df)]=new_row#append the new row to the dataframe

        self.df.drop_duplicates(subset=["Date"],keep="last",inplace=True)#drop duplicates based on the date column keeping the las occurrence
        self.df.sort_values(by="Date",inplace=True)
        self.df.reset_index(drop=True,inplace=True)
        
        if os.path.isfile(self.file_path):#delete the previous file(is not necesary can be improve, but nah, perhaps to a dic and save in a json)
            os.remove(self.file_path)
        self.df.to_csv(self.file_path,sep=";",index=False)#save df to csv file
        


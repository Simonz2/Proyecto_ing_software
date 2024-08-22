from create_dic import CreateDict
import pandas as pd

class PathsFinder:
    def __init__(self):
        self.dic_creator=CreateDict()
        self.file_path=self.dic_creator.dic.get("save_paths")
        self.df=pd.read_csv(filepath_or_buffer=self.file_path,sep=";")
        self.df["Date"]=pd.to_datetime(self.df["Date"])

    def get_file_path(self,date):
        try:
            if date is None:
                raise Exception
            else:
                self.date=pd.to_datetime(date).normalize()
                self.folder_path=self.df.loc[self.df["Date"]==self.date,"Path"].values[0]
                return self.folder_path
        except Exception as e:
            raise ValueError("Error parsing date: {}".format(e))
    
    def save_folder_path(self,date,folder):
        self.date=pd.to_datetime(date).normalize()
        self.folder_path=folder
        new_row={"Date":self.date,"Path":self.folder_path}
        self.df.loc[len(self.df)]=new_row
        self.df.to_csv(self.file_path,sep=";",index=False)
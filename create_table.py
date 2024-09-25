import pandas as pd
from create_dic import CreateDict
import os
from paths_finder import PathsFinder
from reportlab.pdfgen import canvas 
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.pdfbase import pdfmetrics 
from reportlab.lib import colors
from printing import Printing


class CreateTable:
    def __init__(self):
        pass
  
    def read_productos(self):
        self.df=pd.read_csv(self.Productos_path,sep=";")
        self.df.dropna(axis=1,how="all",inplace=True)
        self.df["Cantidad"]=""
        self.df["Total"]=""
    
    def save_bill(self):
        if os.path.exists(self.file_path):
            os.remove(os.path.abspath(self.file_path))
        self.df.to_csv(self.file_path,index=False,sep=";",na_rep="")

    def get_df(self,date,title):
        self.date=date
        self.dic_creator=CreateDict()
        self.Productos_path=self.dic_creator.dic.get("Productos")

        if self.date!=None:
            path_finder=PathsFinder()
            self.folder_path=path_finder.get_file_path(self.date)
            self.file_path=os.path.join(self.folder_path,"".join([title,".csv"]))
            if os.path.isfile(self.file_path) and os.path.exists(self.file_path):
                self.df=pd.read_csv(self.file_path,sep=";")
            else:
                self.read_productos()
        else:
            self.read_productos()
        
        return self.df.fillna("")
    
    def update_date(self, date,title):
        self.date=date
        path_finder=PathsFinder()
        self.folder_path=path_finder.get_file_path(self.date)
        self.file_path=os.path.join(self.folder_path,"".join([title,".csv"]))
    
    def update_df(self,df):
        self.df=df
    
    def end_day_calc(self,titles):
        d=self.date
        total_df=self.get_df(None,None)
        total_df["Total"]=pd.to_numeric(total_df["Total"],errors='coerce').fillna(0)
        total_df["Cantidad"]=pd.to_numeric(total_df["Cantidad"],errors="coerce").fillna(0)
        
        for i in titles:
            if i!="Total_dia":
                df=self.get_df(d,i)
                df["Total"]=pd.to_numeric(df["Total"],errors="coerce").fillna(0)
                df["Cantidad"]=pd.to_numeric(df["Cantidad"],errors="coerce").fillna(0)
                total_df["Total"]=total_df["Total"]+df["Total"]
                total_df["Cantidad"]=total_df["Cantidad"]+df["Cantidad"]
            else:
                pass
        total_df["Total"]=total_df["Total"].replace(0,"")
        total_df["Cantidad"]=total_df["Cantidad"].replace(0,"")
        
        f_path=os.path.join(self.folder_path,"Total_dia.csv")
        
        if os.path.exists(f_path):
            os.remove(os.path.abspath(f_path))
        total_df.to_csv(f_path,index=False,sep=";",na_rep="")       
    def print_bill(self,tip,delivery_fee):
        self.p=Printing(tip,delivery_fee,self.date,self.df)



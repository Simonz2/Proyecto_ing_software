import pandas as pd
import os
from create_dic import CreateDict

class Printing():
    def __init__(self):#init class
        self.dic_creator=CreateDict()#to get path to image
        self.logo_path=self.dic_creator.get_path("logo")#get path to logo

    
    def new_bill(self,df,tip,delivery_fee):#function to print the bill
        self.df=pd.DataFrame(df)
        self.tip=tip
        self.delivery_fee=delivery_fee


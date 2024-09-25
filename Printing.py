import pandas as pd
from create_dic import CreateDict
import os
from paths_finder import PathsFinder
from reportlab.pdfgen import canvas 
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.pdfbase import pdfmetrics 
from reportlab.lib import colors
from reportlab.lib.units import cm,mm
import os
import aspose.pdf as ap

class Printing:
    def __init__(self,tip,delivery_fee,date:str,df):
        dic_creator=CreateDict()
        tip=tip
        delivery_fee=delivery_fee
        df=df.copy()
        df['Cantidad'] = pd.to_numeric(df['Cantidad'], errors='coerce')
        df["Total"]=pd.to_numeric(df["Total"],errors="coerce")
        df.dropna(subset=['Cantidad'], inplace=True)
        date=date.split("-")
        width=6.7*cm
        valid_rows = df[(df['Cantidad'] > 0) & (~df['Cantidad'].isna())]

        # Get the length of these valid rows
        length=(2+2+0.5+3.5+len(valid_rows))*cm
        subtotal=0
        mes= {1: "January",2: "February",3: "March",4: "April",5: "May",6: "June",
        7: "July",8: "August",9: "September",10: "October",11: "November",12: "December"}
        suptitle=["TELEFONO 3022010677",
                f"{date[2]} de {mes[int(date[1])]} de {date[0]}"]
        filename="data\\temporary.pdf"
        height=2*cm
        if os.path.isfile(filename):
            os.remove(filename)
        
        img=dic_creator.dic.get("logo")
        pdf=canvas.Canvas(filename,pagesize=(width,length))
        pdf.setFillColorRGB(0, 0, 255)
        pdf.setFont("Times-Roman", 10)
        #draw image
        pdf.drawImage(img,x=0,y=length-height,width=width,height=height)
        #draw first and second line
        for i in range(2):
            text_height = length - height - (0.5+0.5*i) * cm  # Adjust the text position below the image
            pdf.drawCentredString(width / 2, text_height, text=suptitle[i])
        #draw 3 line where the bill start
        text_height=length-height-2*cm
        header=f"{'PDTO':<27}{'UDS':<5}{'VALOR':<13}"
        pdf.drawString(1*cm,text_height,text=header)
        
        for idx,line in df.iterrows():
            line=list(line)
            if line[2]<1:
                pass
            else:
                text_height-=0.5*cm
                pdf.drawString(1 * cm, text_height, f"{str(line[0])[:15]:<22}")  # Truncate to 20 characters, pad if shorter
                pdf.drawString(40 * mm, text_height, f"{str(line[2]):<5}")       # Same logic applies to other lines
                pdf.drawString(47 * mm, text_height, f"{str(line[3]):<13}")
                subtotal+=line[3]
        text_height-=1*cm
        pdf.drawString(1 * cm, text_height, "SUBTOTAL")
        pdf.drawString(42*mm,text_height,text=f"$ {subtotal}")
        text_height-=0.5*cm
        pdf.drawString(1 * cm, text_height, "SERVICIO")
        pdf.drawString(42*mm,text_height,text=f"$ {subtotal*tip/100}")
        text_height-=0.5*cm
        pdf.drawString(1 * cm, text_height, "DOMICILIO")
        pdf.drawString(42*mm,text_height,text=f"$ {delivery_fee}")
        text_height-=0.5*cm
        total=subtotal+delivery_fee+subtotal*tip/100
        pdf.drawString(1 * cm, text_height, "TOTAL")
        pdf.drawString(42*mm,text_height,text=f"$ {total}")
        pdf.save()
        self.print_pdf(filename)

    def print_pdf(self,path):
        viewer=ap.facades.PdfViewer()
        viewer.bind_pdf(path)
        viewer.print_document()
        viewer.close()
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

def print_pdf(path):
    viewer=ap.facades.PdfViewer()
    viewer.bind_pdf(path)
    viewer.print_document()
    viewer.close()
    


def print_bill(client,tip,delivery_fee,date:str,df:pd.DataFrame):
    dic_creator=CreateDict()
    client=client
    tip=tip
    delivery_fee=delivery_fee
    date=date.split("-")
    width=6.7*cm
    length=10*cm
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
    print
    for idx,line in df.iterrows():
        line=list(line)
        if line[2]<1:
            pass
        else:
            text_height-=0.5*cm
            pdf.drawString(1 * cm, text_height, f"{line[0]:<20}")
            pdf.drawString(33 * mm, text_height, f"{line[2]:<5}")
            pdf.drawString(42 * mm, text_height, f"{line[3]:<15}")
            subtotal+=int(line[3])
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
    print_pdf(filename)

data = {
    "Product Name": ["H.DA VINCCI 150g+100g CHICHA", "Banana", "Orange", "Blue Grapes"],
    "Price": [1.20, 0.50, 0.80, 2.00],  # Prices in dollars
    "Quantity": [10, 20, 0, 5]  # Quantity of each product
}

# Create the DataFrame
df = pd.DataFrame(data)

# Calculate the total for each product (Price * Quantity)
df["Total"] = df["Price"] * df["Quantity"]
for idx,line in df.iterrows():
    line=list(line)
    if line[2]<1:
        pass
    else:
        print(line)
print_bill("Ana",10,5000,"2024-9-24",df)

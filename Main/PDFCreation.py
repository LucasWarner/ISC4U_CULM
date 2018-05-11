from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4

#https://www.reportlab.com/docs/reportlab-userguide.pdf

width, height = letter

pdfName = "SampleMatchSheet.pdf"

#if os.path.exists(pdfName):
    #os.remove(pdfName)

c = canvas.Canvas(pdfName, pagesize=letter)

c.setStrokeColorRGB(0,0,0)
c.setFillColorRGB(1,1,1)


s = 75
rows = 5
collumns = 7

topPadding = 50

c.translate(width/2-(collumns*s)/2, height-(rows*s)-topPadding)

listX = []
listY = []
for i in range(collumns+1):
    listX.append(s*i)
for i in range(rows+1):
    listY.append(s*i)

c.grid(listX, listY) 

thisMonth = 10
monthDays = [31,29,31,30,31,30,31,31,30,31,30,31]


c.setFillColorRGB(0,0,0)

for i in listX:
    for j in listY:
        if j != rows*s and i != collumns*s:
            if int((rows-(j/s)-1)*7+(i/s)+1) <= monthDays[thisMonth]:
                c.drawString(i + s*(1/10), j + s*(3/4), str(int((rows-(j/s)-1)*7+(i/s)+1)))

try:
    c.save()
except "Errno 13":
    print("Please close the PDF file before generating new")

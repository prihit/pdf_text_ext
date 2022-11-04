from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import PyPDF2
import re
# Create your views here.
def home(request):
    if request.method == 'POST' and request.FILES['upload']:
        # print(request.FILES)
        doc = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(doc.name, doc)
        file_url = "." + fss.url(file)
        # print(doc)
        pdfFileObj = open(file_url, 'rb')
  
        # creating a pdf reader object
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        
        # printing number of pages in pdf file
        # print(pdfReader.numPages)
        
        # creating a page object
        pageObj = pdfReader.getPage(0)
        
        # extracting text from page
        a = pageObj.extractText()

        # print(a)
        # print(a[0:28])
        # print(pageObj.extractText())
        
        # closing the pdf file object
        pdfFileObj.close()

        detail_line = []

        for line in a.split('\n'):
            detail_line.append(line)
        print(detail_line)
        name = detail_line[0]
        vehicle = detail_line[detail_line.index('Ride Details')-1]
        n = len(detail_line)
        # i = 1
        # while i <n:
        #     if detail_line[i][0].isnumeric() or detail_line[i] == "NA":
        #         i+=1
        #     else:
        #         vehicle = detail_line[i]
        #         break
        for i in range(n-1,-1,-1): 
            if detail_line[i] != "" and detail_line[i].isnumeric():
                i4 = i
                break
        # print("grgeg   " + detail_line[i4])
        total_fare = detail_line[i4-1] +" "+ detail_line[i4]
        
        i1 = -1
        i2 = -1
        for line in detail_line:
            if re.search("AM$|PM$",line):
                if i1 == -1:
                    i1 = detail_line.index(line)
                else:
                    i2 = detail_line.index(line)

        if "Base Fare" in detail_line:
            i3 = detail_line.index("Base Fare")
        else:
            i3 = detail_line.index('Your Trip')
        # print(i1,i2,i3)
        pickup = detail_line[i1+1:i2]
        destination = detail_line[i2+1:i3]
        p = ""
        d = ""
        for i in pickup:
            p += i + " "
        for i in destination:
            d += i + " "
        print(name)
        print(vehicle)
        print(total_fare)
        print(p)
        print(d)
        context = {
            'name': name,
            'vehicle': vehicle,
            'total_fare': total_fare,
            'source': p,
            'destination': d,
        }
        return render(request,'home.html',context)
    else:
        return render(request,'home.html')
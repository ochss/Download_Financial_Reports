__author__ = "Samuel Ochs"
__version__ = "1.0"
__email__ = "sam.ochs1@gmail.com"
__date__ = "5/4/2020"

#These are all the packages required for the script
import requests
from bs4 import BeautifulSoup
import os
import pdfkit 
from time import sleep
import re

def download_file(list_of_folders,basedir,path_wkhtmltopdf,config):
    #loops through all of the folders in the directory(Company_Folders)
    for company in list_of_folders:    
        #urls for both 10-k and 20-f files    
        filetypes = ['https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK='+company+'&type=10-k&dateb=&owner=exclude&count=20',
                    'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK='+company+'&type=20-f&dateb=&owner=exclude&count=20']
        for url in filetypes:
            #gets the url
            html = requests.get(url)
            sleep(4)
            soup = BeautifulSoup(html.text,'html.parser')
            try:

                #parses response from the reqest
                tbody = soup.find('table',{'class':'tableFile2'})
                
                #gets all of the fillings on the response page
                trs = tbody.findAll('tr')
                
                #loops through the fillings
                for link10 in trs:

                    #issue with passing the header of the table
                    if link10.find('th') == None:
                        tds = link10.findAll('td')

                        #gets the documents link from the page
                        td = tds[1]

                        #sets the date and title for filename
                        title = tds[0].text.strip()
                        date = tds[3].text.strip()

                        #defines the filename
                        filename = (company+'-'+title+'-'+str(date)+'.pdf').replace('/','')

                        #gets the link for the second url
                        tdhref = td.find('a').get('href')

                        #sets the second url for retrieval 
                        linkpartial = 'https://www.sec.gov'
                        linkto10k = linkpartial+tdhref
                        
                        #retrieves the data with the filename url 
                        htmlsecond = requests.get(linkto10k)
                        soupsecond = BeautifulSoup(htmlsecond.text, 'html.parser')

                        #parse and gets the file url
                        tbodysecond = soupsecond.find('table',{'class':'tableFile'})
                        trssecond = soupsecond.findAll('tr')
                        lasttextsub = len(trssecond)
                        link10second = trssecond[1]
                        reallink = link10second.findAll('td')[2].find('a').get('href')
                        reallinktext = link10second.findAll('td')[2].find('a').text

                        if reallinktext == '':
                            link10secondtext = trssecond[lasttextsub-1]
                            reallink = link10secondtext.findAll('td')[2].find('a').get('href')
                        else:
                            pass

                        #stops the iXBRL from showing up
                        reallink = reallink.replace('ix?doc=/','')
                        filelink = linkpartial+reallink
                        
                        #changes the directory to the folder of the company
                        changedir = basedir + company 
                        os.chdir(changedir)
                        
                        #writes the pdf file
                        pdfkit.from_url(filelink, filename, configuration=config)

                    else:
                        pass
            except:
                pass


if __name__ == "__main__":
    basedir = r'C:/Users/~/Download_10k/Company_Folders/'
    list_of_folders = os.listdir(basedir)

    path_wkhtmltopdf = r'C:/Users/~/Download_10k/wkhtmltopdf.exe'

    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    download_file(list_of_folders,basedir,path_wkhtmltopdf,config)
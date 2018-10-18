################# Web Scraping using html pages from yelp.com and writing to CSV ##########################################################

import requests
from bs4 import BeautifulSoup
import re
import urllib2
import numpy as np
import re
import os
#from pandas import DataFrame
#import urlopen
#import urllib2


        #soup = BeautifulSoup(urllib2.urlopen(url), "html.parser")
        #print soup

def DCGroup (scrapywebsite):
        
        sbizname=""
        sbizphone=""
        sbizaddress=""
        sopenhours=""
        finalxx=""
        linkx=""
        sbizurl=""
        emaillist=""
        emailone=""
        proxyemail=""
        finalemail=""
        stringtowrite=""
        print('Scraping html page from D drive..... '+ scrapywebsite)
        url = scrapywebsite
        #soup = BeautifulSoup(urllib2.urlopen(url), "html.parser")
        #print soup
        soup = BeautifulSoup(open(url), "html.parser")
        #print(soup.prettify())
        html = list(soup.children)[12]
        body = list(html.children)[5]
        div = list(body.children)[7]
        ##############################business name ##################################################
        try:
            sbizname = soup.find('h1', class_="biz-page-title embossed-text-white shortenough").get_text()
        except:
            pass
        
        ############################business phone number####################################
        try:
            sbizphone = soup.find('span',class_="biz-phone").get_text()
        except:
            pass
        
        #############################business address##########################################
        try:
            sbizaddress = soup.find('address').get_text()
        except:
            pass
        #############################opening hours################################################
        soup.find_all('div',class_="ywidget biz-hours")
        fitems = soup.find_all(class_="ywidget biz-hours")
        tt = fitems[0]
        #print(tonight.prettify())
        table = list(tt.children)[3]
        tbody = list(table.children)[1]
        #list(table.children)[1]
        
        ######################## extracting and combine opening hours ###################################################
        counter = 1
        x = 0
        a = np.chararray((10))
        b = np.chararray((10))
        final = ""
        yfinal=""
        xfinal = ""
        for counter in range(0,7):
            try:
                x = list(tbody.children)[counter]
            except:
                pass
            td = tbody.find_all('th')
            row = [i.text for i in td]
            th = tbody.find_all('td')
            rowx = [j.text for j in th]
            
        for i in list(row):
                #print(i.split()[0])
                ay=i.split()[0]
                ay = ay.strip()
                final = str(final) +','+ str(ay)
        for j in list(rowx):
                    #print(j.split('[]')[0])
                    by=j.split('[]')[0]
                    by = by.strip()
                    #print((str(by)))
                    #print(len(str(by)))
                    #if not (by.isspace() ) or by[0] <>' ' or by[0]<>'' or by[0]<>'Closed now' or len(by)<>0:
                    if (len(str(by))<>0):
                        if  str(by)!='Closed now':
                            yfinal = str(yfinal) +','+ str(by)
                        
            
        mfinal = final.split(",")
        nfinal = yfinal.split(",")
        try:
            for t in range(1,8):                
                    xfinal = str(xfinal) + mfinal[t]+':'+nfinal[t]+','
                    sopenhours = xfinal
        except:
            pass
        
        
        #print(str(xfinal))
        
        ########### extracting takes reservations upto gender neutral restrooms###########################
        alist = soup.div
        blist = alist.find_next('div',class_="short-def-list")
        datadic={}
        for z in range(0,25):
            try:
                blist=blist.find_next('dl')
                xx = blist.find_next('dt',class_="attribute-key").get_text()
                xx= xx.encode('utf-8').strip()
                yy = blist.find_next('dd').get_text()
                yy = yy.strip().encode('utf-8').strip()
                blist = blist.find_next('dt',class_="attribute-key")
                datadic[xx]=yy
            except:
                pass

        columnsList = ['Takes Reservations','Delivery','Take-out','Accepts Credit Cards','Accepts Apple Pay','Accepts Android Pay',
                    'Accepts Bitcoin','Good For','Parking','Bike Parking','Good for Kids','Good for Groups','Attire','Ambience',
                    'Noise Level','Alcohol','Outdoor Seating','Wi-Fi','Has TV','Caters','Gender Neutral Restrooms']
        for cols in columnsList:
            x=datadic.get(cols)
            if str(x)!='None':
#                finalxx=finalxx+x+'\t'
                try:
                    finalxx = str(finalxx).encode('utf-8').strip()+'\t'+str(x).encode('utf-8').strip()+'\t'
                except:
                    pass
            else:
                finalxx=finalxx+'None \t'      
        
        ############# extract contact and email id########################################################
        #import re
        #import urlopen
        #import urllib2
        #sbizurl = 'http://katerra.com'
        
        #############################business home page URL#######################################
        
        try:
            sbizurlx = soup.find('span',class_="biz-website js-add-url-tagging")
            sbizurl =  'http://'+sbizurlx.find('a').get_text()
            soupx = BeautifulSoup(urllib2.urlopen(sbizurl), "html.parser")
            links = soupx.find_all("a")
            for link in links:       
                x = re.search(".*CONTACT*.",link.text.upper())
                if str(x) != 'None':
                    linkx=link.get("href")
                    xhttp = re.search("http*.",linkx)
                    if str(xhttp) == 'None':
                        searchx = re.search("/*.",linkx)
                        if str(searchx)== 'None':
                            linkx = '/'+linkx 
                            linkx=sbizurl+linkx
                            break;
                        else:
                            linkx=sbizurl+linkx
                            break;
                                   
                        #print(linkx)
            soupxx = BeautifulSoup(urllib2.urlopen(linkx), "html.parser")
            contactLinks = soupxx.find_all("a")
            for contactLink in contactLinks:
                z = re.search(".*mail*.",contactLink.get("href"))
                if str(z) != 'None':
                    finalemail=contactLink.get("href").replace("mailto:","")

        except:
            pass
        
        try:
            sbizname = re.sub('[^a-zA-Z0-9 \n\.]', '', sbizname)
            sbizname=sbizname.encode('utf-8').strip()
        except:
            pass
        try:
            sbizphone=sbizphone.encode('utf-8').strip()
        except:
            pass
        try:
            sbizurl=sbizurl.encode('utf-8').strip()
        except:
            pass
        try:
            sbizaddress=sbizaddress.encode('utf-8').strip()
        except:
            pass
        try:
            sopenhours=sopenhours.encode('utf-8').strip()
        except:
            pass
        if str(linkx)=='None':
            linkx=""
        stringtowrite = sbizname+'\t'+sbizphone+'\t'+sbizurl+'\t'+sbizaddress+'\t'+sopenhours+'\t'+finalxx+linkx+'\t'+finalemail+'\n'
        print(stringtowrite)
        return stringtowrite;

############ iterate through all downloaded html pages , scrap relevant columns and store in csv########
dcresults = 'I:\CBA\Term1\DC\DCRESULTS_test.csv'
htmldir = 'I:\CBA\Term1\DC\\testPages'
dcstring = ""
headers = 'Business name'+'\tBusiness phone number'+'\tBusiness home page URL'+'\tBusiness address'+'\tOpening hours'+'\tTakes Reservations'+'\tDelivery'+'\tTake-out'+'\tAccepts Credit Cards'+'\tAccepts Apple Pay'+'\tAccepts Android Pay'+'\tAccepts Bitcoin'+'\tGood For'+'\tParking'+'\tBike Parking'+'\tGood for Kids'+'\tGood for Groups'+'\tAttire'+'\tAmbience'+'\tNoise Level'+'\tAlcohol'+'\tOutdoor Seating'+'\tWi-Fi'+'\tHas TV'+'\tCaters'+'\tGender Neutral Restrooms'+'\tContact-us URL for the business'+'\tEmail id for the business\n'
dcf = open(dcresults,'w')
dcf.write(headers)
for root, dirs, filenames in os.walk(htmldir):
    for fl in filenames:
        fpath = os.path.join(htmldir, fl)
        #fpath = 'I:\CBA\Term1\DC\\assignmentData\\124.html'
        dcstring = DCGroup (fpath)
        dcf.write(dcstring)
        print('writing to DCRESULTS.csv in D drive under GroupSubmission folder.... '+htmldir)
dcf.close()
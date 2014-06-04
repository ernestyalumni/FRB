# FRBget.py
# getting data from the Federal Reserve Board, Federal Reserve System
# 
# 20140603
# 
# Fund Science! & Help Ernest finish his Physics Research! : quantum super-A-polynomials - Ernest Yeung
#                                               
# http://igg.me/at/ernestyalumni2014                                                                             
#                                                              
# Facebook     : ernestyalumni  
# github       : ernestyalumni                                                                     
# gmail        : ernestyalumni                                                                     
# linkedin     : ernestyalumni                                                                             
# tumblr       : ernestyalumni                                                               
# twitter      : ernestyalumni                                                             
# youtube      : ernestyalumni                                                                
# indiegogo    : ernestyalumni                                                                        
# 
# Ernest Yeung was supported by Mr. and Mrs. C.W. Yeung, Prof. Robert A. Rosenstone, Michael Drown, Arvid Kingl, Mr. and Mrs. Valerie Cheng, and the Foundation for Polish Sciences, Warsaw University.  
#
#

SCHEME = 'http'
NETLOC = 'www.federalreserve.gov'


import requests
from urlparse import urlparse, urlunparse, parse_qs, parse_qsl
from bs4 import BeautifulSoup
import csv

#
# General functions and stuff 
#

def rqst2BS( url ):
    """
    rqst2BS - requests to BeautifulSoup
    rqst2BS - this function uses requests to get a given, inputted in, url address and returns back a BeautifulSoup of the contents
    NOTE : this function requires one to import requests and BeautifulSoup from bs4
    INPUTS  - url address, as a string; use urlunparse
    OUTPUTS
    """
    rqst = requests.get( url )
    soup = BeautifulSoup( rqst.content )
    rqst.close()
    return soup

def navBS00( searchforwhat, targeturl, find_ele , targetstr ):
    """
    navBS00 - navigate with BeautifulSoup, version 00
    navBS00 is specific to the needs here in FRBget.py, it takes some inputs, all strings, to navigate through a website page
    INPUTS  - scheme, baseaddress, targeturl, findHTMLelementstr, findtargetstr
    """
    soup = rqst2BS( targeturl )
    if searchforwhat == "class":
        pageoptions = soup.find_all(class_=find_ele)
    elif searchforwhat == "tag":
        pageoptions = soup.find_all(find_ele)
    else:
        print "Something wrong with implementing BeautifulSoup's find_all"
        return None

    for tab in pageoptions:
        if tab.text.find(targetstr) >=0:
            return tab 

    return None


#
# Federal Reserve Board (FRB) specific functions and stuff
#

frburl  = urlunparse( ( SCHEME, NETLOC, '' , '' , '' , '' ))
# EY 20140603 following might be specific only to the Federal Reserve
frb_data_lnk = navBS00( "class", frburl , "navItem", "Data" ) # EY 20140603 Board of Governors of the Federal Reserve System navigation menu - I just went to Inspect Web Element in Apple Safari (or one could use that Web Developer, Source Code reader thing in the browser) to find the CSS tag

frbdataurl  = urlunparse( ( SCHEME, NETLOC , frb_data_lnk.find("a").attrs['href'] , '' , '' , '' ) )



#
# This gets one to the Data Releases page from the Economic Research & Data navigation tab
#
#frbdatasoup = rqst2BS( frbdataurl )
#frbdataheadings = frbdatasoup.find_all("h2")
#for headings in frbdataheadings:
#    if headings.text.find("Releases") >= 0:
#        frbdatarelease = headings

frbdatarelease = navBS00("tag", frbdataurl , "h2", "Releases" )
frbdatareleaseurl = urlunparse( ( SCHEME, NETLOC, frbdatarelease.find("a").attrs['href'] , '' , '' , '' ) )

#
# This gets one to the Data Download page from the Data Releases page
#

#frbdatareleasesoup = rqst2BS( frbdatareleaseurl )
#frbdatareleaseheadings = frbdatareleasesoup.find_all("h3")

#for heading in frbdatareleaseheadings:
#    if heading.text.find("Download") >= 0:
#        frbdatadwn = heading 

frbdatadwn = navBS00("tag", frbdatareleaseurl , "h3", "Download")
frbdatadwnurl = urlunparse( ( SCHEME, NETLOC, frbdatadwn.find("a").attrs['href'] , '' , '' , '' ) )

#
# EY : 20140603 Use BeautifulSoup to navigate the Federal Reserve 
# 
ddp   = rqst2BS( frbdatadwnurl )  # ddp   - Data Download Program
ddph2 = ddp.find_all("h2")        # ddph2 - Data Download Program h2 tag, Heading 2

class DDP(object):
    """
    DDP - Data Download Program class
    """
    def __init__(self, url):
        """
        INPUTS  - url - url is a string
        """
        self.ddp   = rqst2BS( url )
        self.ddph2 = self.ddp.find_all("h2")

    def view(self):
        for h2 in ddph2:
            print h2.text

    def choose(self,choice):
        """
        choose  - use view method to see what strings are possible
        INPUTS  - choice, as a string
        """

FRBDDP = DDP( frbdatadwnurl )
FRBDDP.ddph2[0].find_next_sibling()
FRBDDP.ddph2[2].find_next_sibling()
FRBDDP.ddph2[2].find_next_sibling().find_all("a")[0].attrs["href"]

CPurl  = urlunparse( ( SCHEME, NETLOC + urlparse(frbdatadwnurl).path + FRBDDP.ddph2[2].find_next_sibling().find_all("a")[0].attrs["href"] , '' , '' , '' , '' ) )
CPsoup = rqst2BS( CPurl )
CPsoup.find_all(class_="cans")[0]
CPsoup.find_all("option")

CPsoup.find_all("option")[0].attrs["value"]

#
# EY : 20140603 look at page http://www.federalreserve.gov/datadownload/Choose.aspx?rel=CP for B Select a preformatted data package, I tried Inspect Element for Go to download and it lead me to javascript and I don't know javascript that well
# 

DWNLDJS = 'Download.aspx?'
FRBCPDD = frbdatadwnurl + DWNLDJS + CPsoup.find_all("option")[0].attrs["value"]  # Download your package
CPDDsoup = rqst2BS( FRBCPDD)

#
# EY : 20140603 pedagogically, this is a good example showing how regular expressions, the way to match patterns of words in strings, is used in BeautifulSoup
# cf. http://stackoverflow.com/questions/16090324/beautifulsoup-find-element-by-text-using-find-all-no-matter-if-there-are-eleme
# 
import re
reg = re.compile(r'Direct')
for e in CPDDsoup.find_all(True):
    if reg.match(e.text):
        directDele = e  # directDele - direct download elements

directDele.attrs['href']

#
# EY : 20140603 there is an issue with python library requests in that it doesn't handle files to download from the web simply. See the following:
# cf. http://stackoverflow.com/questions/14114729/save-a-file-using-the-python-requests-library
# whereas urllib deals with downloading files simply
#
import urllib
from urllib import urlretrieve, urlencode
import urllib2


f = urllib.urlopen( frbdatadwnurl + directDele.attrs['href'] )

fCPout = f.readlines()
f.close()

#
# EY : 20140603 take a look at how the Fed does csv file retrieval but by specifying dates
CPwitDates = 'http://www.federalreserve.gov/datadownload/Output.aspx?rel=CP&series=593ce926936cbd64b3c79b960a792b85&lastObs=&from=01/01/1998&to=12/31/2014&filetype=csv&label=include&layout=seriescolumn'
CPwitDatesprsd = urlparse(CPwitDates)

CPwitDatesparams = parse_qs(CPwitDatesprsd.query)

CPwitDatesparams.pop("label")
# assume a dictionary for the query

# EY 20140603 I have no idea why parse_qs ends up with a list
for key in CPwitDatesparams: CPwitDatesparams[key] = str( CPwitDatesparams[key][0] )

f2 = urllib2.urlopen( urlunparse( ( CPwitDatesprsd.scheme , CPwitDatesprsd.netloc, CPwitDatesprsd.path , '' , urlencode( CPwitDatesparams ) , '' )  ) )
 
f2out = f2.readlines()

# EY : 20140603 doesn't work, problem with the backslash character in the dates

# cf. http://stackoverflow.com/questions/16283799/how-to-read-a-csv-file-from-a-url-python 
f3 = urllib2.urlopen( CPwitDates )
import csv
f3r = csv.reader( f3 )
f3.close()

#
# EY : 20140603 We've downloaded the data and we should save it into a database for the data to persist
# I use sqlite3
import sqlite3

db_filename = "FRBCP.db"
conn = sqlite3.connect( db_filename )

#
# headings need to be prepared already
# 
# how to store column descriptions?  relational database time!



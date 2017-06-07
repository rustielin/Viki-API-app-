#!/usr/bin/env python 

#Shopstyle internship assignment 
#A script that gathers video data using the Viki API

import hmac, time, requests 
from hashlib import sha1
from time import sleep 

#Viki API authentication and call resources 
SECRET = 'bcb959661b3be4613c1d380b3c29981e8b1ed868762af37d8201f4f9ff73' 
APP  = '100684a'
ENDPOINT = '/v4/videos.json'
URL = 'http://api.viki.io'

#add user agent to prevent viki from blocking our connection 
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

#some useful vars
per_page = '10' 
page_num = 1
more = True 
hd = 0
nonhd = 0


#makes a GET request 
def make_request():
    query = make_query() 
    r = requests.get(URL + query, headers =HEADERS ) 
    return r.json() 




    
#makes the query string, including required SHA1-HMAC required by Viki API
def make_query():
    unix_time = str(int(time.time()))
    msg = ENDPOINT + '?app=' + APP + '&per_page=' + per_page + '&page=' + str(page_num) + '&t=' + unix_time 
    h = hmac.new(bytes(SECRET, 'UTF-8'), bytes(msg, 'UTF-8'), sha1) 
    return msg + '&sig=' + h.hexdigest()
    #The below also works, but Viki API suggests encryption and SHA1-HMAC signature for authentication 
    #return '/v4/videos.json?app=100250a&per_page=10&page=' + str(page_num) 




def count_hd():
    #keep requesting data while there are more pages to load 
    global page_num, hd, nonhd, more

    while more:
        try:
            obj = make_request() 
        except:
            #in the case that Viki API blocks our connection for requesting too much data too quickly, stop for a while 
            sleep(5) 
            
        #parse the JSON response 
        more = obj['more']
        arr = obj['response'] 

        #count the HD and non HD videos 
        for el in arr:
            if el['flags']['hd']:
                hd+=1
            else:
                nonhd+=1 

        page_num += 1

    #print the results 
    print('hd: ', hd) 
    print('nonhd: ', nonhd)          
        
        

#start: print out number of HD and non HD videos on Viki 
count_hd() 

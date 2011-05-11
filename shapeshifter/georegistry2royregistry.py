#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import os,sys, json
from utils import query_georegistry
import pycurl, StringIO

gr_server="http://ni-api.georegistry.org"
gr_user="aviars"
gr_pass="pass"

roys_api_key="BFkc5J7fuqf9JkUUUwcoZQ7h7IuE4erXgk5PbwoK6E6g0cW9TPGszdAOChRMm2yA9YjC644xEHSlotudcEm3hB4BSZtVCDYpQnwnZ8NZ68vNH5GaYx20SKihrkvOJyXoV7w0TYyUp6rvxrdOQmLRwA3chW0bPWfKXZODn63LbeWL2X9BcTsi7gk1ZGK6K8ov4JOWb9QO4Ww5LDVq9FLusfj29G2yYQOZsilBnLDRsiDOn5qBQTL176rRUYnHWFMl"

def fetch_country_data_from_gr(country_code):
    URL="/api/1.0/features/search?country_code=NG&limit=1000"
    r = query_georegistry(URL, gr_server, gr_user, gr_pass)

    return json.loads(r)
def load_roys_georegistry(decocodedjson):
    country={}
    subdivision={}
    level2={}
    stripedfeatures=[]
    countryfeatures=[]
    subdivisionfeatures=[]
    level2features=[]
    
    for i in decocodedjson['features']:
        del i['id']
        stripedfeatures.append(i)
        if i['geometry']['type']=="Polygon":
            i['geometry']['coordinates']=[i['geometry']['coordinates']]
    decocodedjson['features']=stripedfeatures
    
    country.update(decocodedjson)
    subdivision.update(decocodedjson)
    level2.update(decocodedjson)

    for i in country['features']:
        if i['properties']['level']=="0":
            countryfeatures.append(i)
    country['features']=countryfeatures
    print len(country['features'])
    
    for i in subdivision['features']:

        if i['properties']['level']=="1":
            subdivisionfeatures.append(i)
    subdivision['features']=subdivisionfeatures
    print len(subdivision['features'])
    
    for i in level2['features']:
        if i['properties']['level']=="2":
            level2features.append(i)
    level2['features']=level2features
    print len(level2['features'])
    
    r=create_features_in_royregistry(country, "nigeria-country")
    print r
    r=create_features_in_royregistry(subdivision, "nigeria-subdivision")
    print r
    r=create_features_in_royregistry(level2, "nigeria-level2")
    print r
    return None

def georegistry2royregistry(country_code):
    load_roys_georegistry(fetch_country_data_from_gr(country_code))

def create_features_in_royregistry(featuredict, tags,
                                  RR_SERVER="http://maps.georegistry.org",
                                  RR_APIKEY=roys_api_key ):
    """
    
    """
    postdict={}
    postdict['tags']=tags
    postdict['key']=RR_APIKEY
    postdict['public']=1
    postdict['srid']=4326
    print postdict
    del featuredict['status']
    del featuredict['total']
    postdict['featureCollection']=json.dumps(featuredict)
    
    pf=[]
    for i in postdict:
        x=(str(i), str(postdict[i]))
        pf.append(x)
        
    URL= RR_SERVER + "/features"
    print "POST to %s " % (URL)
    c = pycurl.Curl()
    c.setopt(pycurl.URL, URL)
    c.setopt(c.HTTPPOST, pf)
    c.setopt(c.SSL_VERIFYPEER, False)
    b = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.setopt(pycurl.HTTPHEADER, ["Accept:"])
    c.perform()
    json_string= b.getvalue()
    return json_string



if __name__ == "__main__":
    
        try:
            if len(sys.argv)<2:
                print "Usage: georegistry2georegistry.py [country_code]"
                sys.exit(1)
                
            country_code =  sys.argv[1]
            
            georegistry2royregistry(country_code)
                
        except:
            print "Error."
            print sys.exc_info()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import os,sys, json
from utils import create_feature_in_georegistry

GR_SERVER="http://127.0.0.1:8000"
GR_USER="alan"
GR_PASS="pass"


def geojson2georegistry(filename, extra_properties={}):
    txfailed=0
    txsuccess=0
    total=0
    FILE = open(filename,"r")
    # Write all the lines at once:
    gj=FILE.read()
    FILE.close()
    gj=json.loads(gj)
    features=gj['features']
    
    for i in features:
        if i.has_key('type'):
            del i['type']
        if i.has_key('properties'):
            if i['properties'].has_key('Id'):
                del i['properties']['Id']   
        
            for k,v in i['properties'].items():
                i[k]=v
            del i['properties']
        
        i['geometry_type']=i['geometry']['type']
        i['geometry_coordinates']=i['geometry']['coordinates']
        del i['geometry']
        if extra_properties:
            i.update(extra_properties)
        r=create_feature_in_georegistry(i, GR_SERVER,GR_USER, GR_PASS)
        total+=1
        print "Processing record # %s" % (total)
        try:
            r=json.loads(r)
        except:
            FILE = open("out.html","w")
            # Write all the lines at once:
            FILE.writelines(x)
            FILE.close()
            sys.exit(1)
        if r["status"]!="200":
            txfailed+=1
            print r
        else:
            txsuccess+=1
            
    print "Done!  %s records processed. %s Failures." % (txsuccess,txfailed )

    return None


if __name__ == "__main__":
    
        try:
            if len(sys.argv)<2:
                print "Usage: geojsongeoregistry.py [infile.json]"
                sys.exit(1)
                
            filename =  sys.argv[1]
            extra_properties =  sys.argv[2]
            
            extra_properties=json.loads(extra_properties)
            print extra_properties
            
            geojson2georegistry(filename,extra_properties)
                
        except:
            print "Error."
            print sys.exc_info()
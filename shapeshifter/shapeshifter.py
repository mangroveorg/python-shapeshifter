#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import os,sys, csv
from progressbar import ProgressBar
from osgeo import ogr
import json
from utils import query_georegistry
import slugify
import xlwt
from shapely.geometry import Polygon, MultiPolygon
import exceptions
from shapely.wkb import loads


def extract_lev2_data_from_shapfile(shape_path, country_code):
    dbf="%s.dbf" % (shape_path)
    shp="%s.shp" % (shape_path)

    URL="/api/1.0/features/locations?country_code=%s" %(country_code)

    locations=json.loads(query_georegistry(URL))

    if locations=={}:
        print "Warning: This country's heirchy is not in the georegistry."
        states=()
    else:
        country=locations.keys()[0]
        states=locations[country]['children']
    l=[]
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.Open(dbf, 0)
    if ds is None:
        print 'Can not open', ds
        sys.exit(1)
    lyr = ds.GetLayer()
    totfeats = lyr.GetFeatureCount()
    lyr.SetAttributeFilter('')
    print 'Starting extraction of %s of %s features in shapefile %s...' % (lyr.GetFeatureCount(), totfeats, lyr.GetName())
    pbar = ProgressBar(maxval=lyr.GetFeatureCount()).start()
    k=0
    # iterate the features and access its attributes (including geometry) to store them in dict
    feat = lyr.GetNextFeature()
    while feat:
        d={}
        geom = feat.GetGeometryRef()
        g = geom.ExportToJson()
        g=json.loads(g)
        d['geometry_coordinates']= g['coordinates'][0]
        d['geometry_type']=g['type']
        # iterate the feature's fields to get its values and store them in dict
        feat_defn = lyr.GetLayerDefn()
        for i in range(feat_defn.GetFieldCount()):
            value = feat.GetField(i)
            if isinstance(value, str):
                value = unicode(value, 'latin-1')
            field = feat.GetFieldDefnRef(i)
            fieldname = field.GetName()
            d[fieldname] = value
        for i in states:
            if i['name']==d['ADM1NAME']:
                #print i['name'], "MATCH!"
                d['subdivision_code']=i['subdivision_code']
                d['subdivision_slug']=i['slug']
                
        d['subdivision_name']=d['ADM1NAME']   
        if d.has_key('ADM1NAME'):
            del d['ADM1NAME']
        if d.has_key('ISO_Ctry'):
            d['country_code']=d['ISO_Ctry']
            del d['ISO_Ctry']
        
        if d.has_key('Name'):
            d['name']=d['Name']
            del d['Name']
            d['slug']=slugify.slugify(unicode(d['name']))
        
        borders = ds.GetLayerByName(lyr.GetName())
        centroid=loads(feat.GetGeometryRef().ExportToWkb())

        centroidpoint = centroid.representative_point()._get_coords()[0]
        d['geometry_centroid']=list(centroidpoint)
        d['bounds']=list(centroid.bounds)
        l.append(d) 
        feat.Destroy()
        feat = lyr.GetNextFeature()
        k = k + 1
        pbar.update(k)
    pbar.finish()
    return l

def extract_state_data_from_shapfile(shape_path, country_code):
    dbf="%s.dbf" % (shape_path)
    shp="%s.shp" % (shape_path)

    
    URL="/api/1.0/features/locations?country_code=%s" %(country_code)
    locations=json.loads(query_georegistry(URL))

    if locations=={}:
        print "Warning: This country's heirchy is not in the georegistry."
        states=()
    else:

        country=locations.keys()[0]
        states=locations[country]['children']

    l=[]
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.Open(dbf, 0)
    if ds is None:
        print 'Can not open', ds
        sys.exit(1)
    lyr = ds.GetLayer()
    totfeats = lyr.GetFeatureCount()
    lyr.SetAttributeFilter('')
    print 'Starting extraction of %s of %s features in shapefile %s...' % (lyr.GetFeatureCount(), totfeats, lyr.GetName())
    pbar = ProgressBar(maxval=lyr.GetFeatureCount()).start()
    k=0
    # iterate the features and access its attributes (including geometry) in dict
    feat = lyr.GetNextFeature()
    while feat:
        d={}
        geom = feat.GetGeometryRef()
        g = geom.ExportToJson()
        g=json.loads(g)
        d['geometry_coordinates']= g['coordinates'][0]
        d['geometry_type']=g['type']
        # iterate the feature's fields to get its values and store them in dict
        feat_defn = lyr.GetLayerDefn()
        for i in range(feat_defn.GetFieldCount()):
            value = feat.GetField(i)
            if isinstance(value, str):
                value = unicode(value, 'latin-1')
            field = feat.GetFieldDefnRef(i)
            fieldname = field.GetName()
            d[fieldname] = value
        
        for i in states:
            if d['Name']==i['name']:
                d.update(i)
                
        if d.has_key('ISO_Ctry'):
            d['country_code']=d['ISO_Ctry']
            del d['ISO_Ctry']
        
        if d.has_key('Name'):
            d['name']=d['Name']
            del d['Name']
        
        borders = ds.GetLayerByName(lyr.GetName())
        centroid=loads(feat.GetGeometryRef().ExportToWkb())

        centroidpoint = centroid.representative_point()._get_coords()[0]
        d['geometry_centroid']=list(centroidpoint)
        d['bounds']=list(centroid.bounds)
        #print d
        l.append(d) 
        feat.Destroy()
        feat = lyr.GetNextFeature()
        k = k + 1
        pbar.update(k)
    pbar.finish()
    return l

def extract_country_data_from_shapfile(shape_path, country_code):
    dbf="%s.dbf" % (shape_path)
    shp="%s.shp" % (shape_path)
    

    l=[]
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.Open(dbf, 0)
    if ds is None:
        print 'Can not open', ds
        sys.exit(1)
    lyr = ds.GetLayer()
    totfeats = lyr.GetFeatureCount()
    lyr.SetAttributeFilter('')
    

    
    print 'Starting extraction of %s of %s features in shapefile %s...' % (lyr.GetFeatureCount(), totfeats, lyr.GetName())
    pbar = ProgressBar(maxval=lyr.GetFeatureCount()).start()
    k=0
    # iterate the features and access its attributes (including geometry) in dict
    feat = lyr.GetNextFeature()
    while feat:
        d={}
        geom = feat.GetGeometryRef()
        g = geom.ExportToJson()
        g=json.loads(g)
        d['geometry_coordinates']= g['coordinates'][0]
        d['geometry_type']=g['type']
        # iterate the feature's fields to get its values and store them in dict
        feat_defn = lyr.GetLayerDefn()
        for i in range(feat_defn.GetFieldCount()):
            value = feat.GetField(i)
            if isinstance(value, str):
                value = unicode(value, 'latin-1')
            field = feat.GetFieldDefnRef(i)
            fieldname = field.GetName()
            d[fieldname] = value
                
        if d.has_key('ISO_Ctry'):
            d['country_code']=d['ISO_Ctry']
            del d['ISO_Ctry']
        
        if d.has_key('Name'):
            d['name']=d['Name']
            del d['Name']
        
        """Fetch the centroid"""
        borders = ds.GetLayerByName(lyr.GetName())
        centroid=loads(feat.GetGeometryRef().ExportToWkb())
        centroidpoint = centroid.representative_point()._get_coords()[0]
        d['geometry_centroid']=list(centroidpoint)

        d['bounds']=list(centroid.bounds)
        
        #print d
        l.append(d) 
        feat.Destroy()
        feat = lyr.GetNextFeature()
        k = k + 1
        pbar.update(k)
    pbar.finish()
    return l

def convert2csv(l, outfile="out.csv"):
    
    csvWriter = csv.writer(open(outfile, 'wb'), delimiter='|',
                         quotechar='|', quoting=csv.QUOTE_MINIMAL)

    #csvWriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    #csvWriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
    
    """get the keys"""
    keys=l[0].keys()
    keyindex=0
    
    """write the keys to the first row"""
    csvWriter.writerow(keys)
    for i in l:
        values=i.values()
        csvWriter.writerow(values)

def convert2json(l, outfile="out.json"):
    FILE = open(outfile,"w")
    # Write all the lines at once:
    FILE.writelines(json.dumps(l, indent=4))
    FILE.close()

def convert2geojson(l, outfile="GeoJSON-out.json", extra_properties=(),
                    file_or_print="file"):
    
    property_index=0
    #make sure the extra properties list and the shape list are the same size
    if extra_properties:
        if len(l)!=len(extra_properties):
            print "FATAL ERROR: Extra properties list and shape list must be the same length!"
            sys.exit(1)
    
    """create a feature collection boilerplate"""
    feature_collection_boiler={"type": "FeatureCollection", "features":[]}
    
    """create a feature biolerplate"""
    feature_boiler={"type": "Feature",
       "geometry":{"type": None,
                   "coordinates": []},
       "properties":{}  
      }
    
    #iterate over our list of shapes
    for i in l:
        #create a new feature from our boilerplate
        f=feature_boiler
        #build the geometry
        f["geometry"]["type"]=i["geometry_type"]
        f["geometry"]["coordinates"]=i["geometry_coordinates"]
        # erase the geometry from out shape dict and stuff everything else
        # in the properties
        del i["geometry_type"]
        del i["geometry_coordinates"]
        f["properties"]=i
        #Add extra properties if they exist.
        if extra_properties:
            f["properties"].update(extra_properties[property_index])
        
        #append the feature to the feature collection
        feature_collection_boiler["features"].append(f)
        #increment the extra property index
        property_index+=1
    if file_or_print=="file":
        FILE = open(outfile,"w")
        # Write all the lines at once:
        FILE.writelines(json.dumps(feature_collection_boiler, indent=4))
        FILE.close()
    else:
        print json.dumps(feature_collection_boiler, indent=4)
    return feature_collection_boiler

def convert2xls(l, outfile="out.xls"):
    datatruncated=False
    """create the spreadsheet"""
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1')
    """get the keys"""
    keys=l[0].keys()
    keyindex=0
    
    """write the keys to the first row"""
    for i in keys:
        sheet.write(0,keyindex,i)
        keyindex+=1
    """Write the rows"""
    rowindex=1
    
    for i in l:
        columnindex=0
        values=i.values()
        #print values
        for j in values:
            if len(str(j))>65535:
                j=str(j)[0:65535]
                datatruncated=True
            sheet.write(rowindex,columnindex,str(j))
            columnindex+=1
        rowindex+=1
    
    wbk.save(outfile)
    if datatruncated==True:
        print "!!! WARNING !!! - Some data was truncated because it was too long!"

if __name__ == "__main__":
    
        try:
            if len(sys.argv)<4:
                print "Usage: shapeshifter.py shapefile.dbf country_code level[0|1|2] <xls|csv|json> <outfile>"
                sys.exit(1)
                
            filename =  sys.argv[1]
            country_code =  sys.argv[2]
            level= sys.argv[3]
            if len(sys.argv)>=4:    
                
                if level=="2":
                    l=extract_lev2_data_from_shapfile(filename, country_code)
                elif level=="1":
                    l=extract_state_data_from_shapfile(filename, country_code)
                    
                elif level=="0":
                    l=extract_country_data_from_shapfile(filename, country_code)
                else:
                    print "Usage: python shapeshifter.py shapefile country_code level[0|1|2] <xls|csv|json|geojson> <outfile>"
                    sys.exit(1)
            else:
                print "Usage: python shapeshifter.py shapefile country_code level[0|1|2] <xls|csv|json|geojson> <outfile>"
                sys.exit(1)
                
            if len(sys.argv)>=5:  
                if sys.argv[4]=="xls":
                    print "Building xls file...."
                    if len(sys.argv)>=6:
                        convert2xls(l, sys.argv[5])
                    else:
                        convert2xls(l)
                
                elif sys.argv[4]=="csv":
                    print "Building pipe delimeted csv file....."
                    if len(sys.argv)>=6:
                        convert2csv(l, sys.argv[5])
                    else:
                        convert2csv(l)
                
                elif sys.argv[4]=="json":
                    print "Building JSON fixture file....."
                    if len(sys.argv)>=6:
                        convert2json(l, sys.argv[5])
                    else:
                        convert2json(l)
                        
                elif sys.argv[4]=="geojson":
                    print "Building GeoJSON fixture file....."
                    if len(sys.argv)>=6:
                        convert2geojson(l, sys.argv[5])
                    else:
                        convert2geojson(l)
                else:
                    print "Usage: python shapeshifter.py shapefile country_code level[0|1|2] <xls|csv|json|geojson> <outfile>"
                    sys.exit(1)
            else:
                print "No output format specified so dumping results to stdout as json...."
                convert2geojson(l, file_or_print="print")
                
        except:
            print "Error."
            print sys.exc_info()

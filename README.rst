python-shapeshifter - by Alan Viars 2011
version 0.0.1

Homepage:
=========
http://gitbub.com/mangroveorg/python-shapeshifter

Description:
============
ShapeShifter is a tool for bu‎ilding Python objects and spreadsheets form data in ESRI Shapefiles. Use this library when you want to pull out data in shape file into a CSV, Excel spreadsheet, Google spreadsheet, or into a list of Python dicts.

Dependencies:
=============
* osgeo
* progressbar
* slugify
* json
* xlrd
* xlwt
* gdata
* pycurl
* shapely

Installation:
=============

After dependencies are satisfied you can install with easy_install or pip. First download the package.
::
	$ wget https://github.com/mangroveorg/python-shapeshifter/tarball/master --no-check-certificate -o python-shapeshifter.tar.gz

Install with easy_install
::
	$ (sudo) easy_install python-shapeshifter.tar.gz

An "Old school" install
::
	$ tar zxvf python-shapeshifter.tar.gz
	$ cd python-shapeshifer
	$ (sudo) python setup.py installl

Command line Utility Usage:
===========================

This is the basic usage of the command line utility.
::
$shapeshift [shapefile] [country_code] [level[0|1|2] <xls|csv|json> <outfile>

Note that you pass the shapefile name with a file extension.  There should be at
least two file with the same name and extensions .dbf and .shp in the same
directory. 

The level indicates wheather the shapfile you are reading is country level (level 0),
statelevel (i.e.subdivision / level 1) or county level (i.e. level 2).

The output format options are "xls" for Excel, "csv" for comma seperated value
(we use pipes instead of commas), "json" for a flat json output matching the csv,
or "geojson" to output a FeatureCollection in GeoJSON format.

The outfile is the name of the file the output is written.  If not specified,
the file name out.[json|csv|xls] is used.

If you do not specify an output format (or file), then the result is dumped to
stdout in json.

An example converting a state(level 0) shapefile to a CSV file
::
    $ shapeshift nigeria_country_boundary NG 1 csv nigeria_states.csv


An example converting a state(level 1) shapefile to a CSV file
::
    $ shapeshifter nigeria_states NG 1 csv nigeria_states.csv

An example converting a county(level 2) shapefile to a JSON file
::
    $ shapeshift nigeria_lev2 NG 2 json nigeria_lev2.json
    
    
API Usage:
==========

How to import the shapeshifter library:
::
  >>> import shapeshifter  

The package defines the following methods.

* extract_lev2_data_from_shapfile(shape_path, country_code)
* extract_state_data_from_shapfile(shape_path, country_code)
* extract_country_data_from_shapfile(shape_path, country_code)
* convert2csv(l, outfile="out.csv")
* convert2json(l, outfile="out.json")
* convert2geojson(l, outfile="GeoJSON-out.json", extra_properties=(), file_or_print="file")         
* convert2xls(l, outfile="out.xls"):


Detailed documentation for each function is inside each function.

Below is the code for shapeshift which illustrates how these functions are used.
::
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    # vim: ai ts=4 sts=4 et sw=4
    import os,sys,json
    from  shapeshifter.shapeshifter import extract_lev2_data_from_shapfile
    from  shapeshifter.shapeshifter import extract_state_data_from_shapfile
    from  shapeshifter.shapeshifter import extract_country_data_from_shapfile
    from  shapeshifter.shapeshifter import convert2xls,  convert2csv, convert2json
    
    
    if __name__ == "__main__":
        
            try:
                if len(sys.argv)<4:
                    print "Usage: shapeshift shapefile country_code level[0|1|2] <xls|csv|json> <outfile>"
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
                        print "Usage: shapeshift shapefile country_code level[0|1|2] <xls|csv|json|geojson> <outfile>"
                        sys.exit(1)
                else:
                    print "Usage: shapeshift shapefile country_code level[0|1|2] <xls|csv|json|geojson> <outfile>"
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
                        print "Usage: shapeshift shapefile country_code level[0|1|2] <xls|csv|json|geojson> <outfile>"
                        sys.exit(1)
                else:
                    print "No output format specified so dumping results to stdout as json...."
                    convert2geojson(l, file_or_print="print")
            except:
                print sys.exc_info()

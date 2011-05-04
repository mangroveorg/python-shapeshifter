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

Usage:
======

This is the basic usage of the command line utility.
::
$shapeshift [shapefile] [country_code] [level[0|1|2] <xls|csv|json> <outfile>

Note that you pass the shapefile name with a file extension.  There should be at
least two file with the same name and extensions .dbf and .shp in the same
directory. 

The level indicates wheather the shapfile you are reading is country level (level 0),
statelevel (i.e.subdivision / level 1) or county level (i.e. level 2).

The output format options are "xls" for Excel, "csv" for comma seperated value
(we use pipes instead of commas), or json for json output.

The outfile is the name of the file the output is written.  If not specified,
the file name out.[json|csv|xls] is used.

If you do not specify an output format (or file), then the result is dumped to
stdout in json.

An example converting a state(level 1) shapefile to a CSV file
::
    $ shapeshift nigeria_country_boundary NG 1 csv nigeria_states.csv


An example converting a state(level 1) shapefile to a CSV file
::
    $ shapeshifter nigeria_states NG 1 csv nigeria_states.csv

An example converting a county(level 2) shapefile to a JSON file
::
    $ shapeshift nigeria_lev2 NG 2 json nigeria_lev2.json
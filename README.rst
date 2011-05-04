python-shapeshifter - by Alan Viars 2011
version 0.0.1
========================================

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
	$ wget http://github.com/mangroveorg/python-shapeshifter/tarball/master


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
shapeshifter.py shapefile.dbf country_code level[1|2] <xls|csv|json> <outfile>

The level indocates wheather the shapfile you are reading is statelevel (i.e.
subdivision / level 1) or county level (i.e. level 2).

The output format options are "xls" for Excel, "csv" for comma seperated value
(we use pipes instead of commas), or json for json output.

The outfile is the name of the file the output is written.  If not specified,
the file name out.[json|csv|xls] is used.

If you do not specify an output format (or file), then the result is dumped to
stdout in json.

An example converting a state(level 1) shapefile to a CSV file
::
    $ python shapeshifter.py nigeria_states.dbf NG 1 csv nigeria_states.csv

An example converting a county(level 2) shapefile to a JSON file
::
    $ python shapeshifter.py nigeria_lev2.dbf NG 2 json nigeria_lev2.json
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import pycurl, StringIO

def query_georegistry(URL,
                  GR_SERVER="http://api.georegistry.org",
                  USERNAME="user",
                  PASSWORD="pass"):
    """Query GR"""
    response_dict={}
    user_and_pass="%s:%s" % (USERNAME, PASSWORD)
    URL= GR_SERVER + str(URL)
    c = pycurl.Curl()
    c.setopt(pycurl.URL, URL)
    c.setopt(c.SSL_VERIFYPEER, False)
    b = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.setopt(pycurl.HTTPHEADER, ["Accept:"])
    c.setopt(pycurl.USERPWD, user_and_pass)
    c.perform()
    try:
        json_string= b.getvalue()
    except:
        json_string=None
    return json_string
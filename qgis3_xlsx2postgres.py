#!/usr/local/bin/python
# -*- coding: utf-8 -*-

## This script takes a .xlsx file and loads it into a postgresql database, from witihn QGis.  It doesn't use the pandas module
## because it might not be installed (by default, QGis doesn't); it uses xlrd instead of pandas, and psycopg2 for the connection to the server.
## It can be stored as a layer action or run from the python console.  And maybe as a processing toolbox script.

## Since it is supposed to work from within QGis, it is asumed that there is already a live connection to postgresql with stored
## parameters, and we use here the QSettings to find them and retrieve the login and password without storing them in the script.

__author__ = 'didier'
__version__ = '0.6'

import os, sys, psycopg2, csv, xlrd
from PyQt5 import Qt
from qgis.gui import QgsMessageBar
from PyQt5.QtWidgets import QFileDialog
from qgis.core import *
from qgis.utils import iface

## Function to retrieve the login and password from a stored PostGIS connection 
def get_postgres_conn_info(selected):
    """ Read PostgreSQL connection details from QSettings stored by QGIS
    """
    settings = QSettings()
    settings.beginGroup(u"/PostgreSQL/connections/" + selected)
    if not settings.contains("database"): # non-existent entry?
        return {}

    conn_info = dict()
    conn_info["host"] = settings.value("host", "", type=str)

    # password and username
    username = ''
    password = ''
    authconf = settings.value('authcfg', '')
    if authconf :
        # password encrypted in AuthManager
        auth_manager = QgsApplication.authManager()
        conf = QgsAuthMethodConfig()
        auth_manager.loadAuthenticationConfig(authconf, conf, True)
        if conf.id():
            username = conf.config('username', '')
            password = conf.config('password', '')
    else:
        # basic (plain-text) settings
        username = settings.value('username', '', type=str)
        password = settings.value('password', '', type=str)
    
    return username, password

## dialog to select the excel file
file, _filter = QFileDialog.getOpenFileName(None, "Open Data File", '.', "(*.xlsx)")
if file == "":
   errmsg_xl = 'Selection canceled'
   iface.messageBar().pushMessage("Error", errmsg_xl, level=Qgis.Warning, duration=6)
   raise

## initiating a csv file at the same place than the excel file
csvfile = file.replace(".xlsx", ".csv")

## function to populate the csv
## takes 2 arguments: the xlsx file name and the csv name (+ path)
def csv_from_excel(arg_xlsx, arg_csv):
    wb = xlrd.open_workbook(arg_xlsx)
    sh = wb.sheet_by_index(0)
    nblines = sh.nrows - 1 # counting the lines

    to_csv_file = open(arg_csv, 'w', newline='')
    wr = csv.writer(to_csv_file, delimiter =';', quoting=csv.QUOTE_NONE)
    ## next step removes the '.0' from the numbers because excel doesnt make any difference between number types;
    ## this would cause the integers to become decimal numbers, which could be a problem afterward when uploading the data to
    ## a table where integers are expected
    for rownum in range(0, sh.nrows):
        newrow=[]
        if rownum == 0:
            wr.writerow(sh.row_values(rownum))
        else:
            for x, col in enumerate(sh.row_values(rownum)):
                if str(col).endswith('.0'):
                    newcol=str(col).replace(".0", "")
                else:
                    newcol=col
                newrow.append(newcol)
            wr.writerow(newrow)
    return nblines
    to_csv_file.close()

## connexion to the server
myname, mypass = get_postgres_conn_info("connection_name")  # provide here a stored connection name
try:
    conn = psycopg2.connect(host="xxx.xxx.xxx.xxx", port="5432", dbname="xxxxxxxxxx", user = myname, password = mypass) 
    cur = conn.cursor()
except (Exception, psycopg2.Error) as error :
    errmsg = 'The connection failed.' # \( ' + error + ' \)'
    iface.messageBar().pushMessage("Error", errmsg, level=Qgis.Critical, duration=10)
    raise

del mypass. ## deleting the password

## creating the csv
nblin = csv_from_excel(file, csvfile)

## uploading the csv to an existing table (table_in) in the server.
## This steps uses the psycopg2 cur.copy_from() method because it is much faster than inserts,
## and this is the reason to convert the xlsx file into a csv
try:
    with open(csvfile, 'r') as f:
        next(f)  # Skip the header row.
        cur.copy_from(f, table_in, sep=';')
except (Exception, psycopg2.Error) as error :
    errmsg_im = 'Error while loading' #
    iface.messageBar().pushMessage("Error", errmsg_im, level=Qgis.Critical, duration=10)
    raise

## closing database connection.
if(conn):
    cur.close()
    conn.commit()
    conn.close()

## cleaning up
os.remove(csvfile)

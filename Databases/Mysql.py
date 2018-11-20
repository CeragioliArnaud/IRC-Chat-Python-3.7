#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector 

conn = mysql.connector.connect(host="localhost",user="root",password="Pythonisso2017", database="test")
cursor = conn.cursor()

x = conn.cursor()

#// INSERT INTO

try:
   x.execute("""INSERT INTO cafe (NOM_CAFE, FO_ID, PRIX, VENTES) VALUES (%s,%s,%s,%s)""",('Maroc', 122,5.99, 200))
   conn.commit()
except:
   conn.rollback()

#// SELECT FROM DB

cursor.execute("""SELECT NOM_CAFE, FO_ID, PRIX FROM cafe WHERE NOM_CAFE = %s""", ("Espresso", ))
rows = cursor.fetchall()
for row in rows:
    print('{0} : {1} | {2}'.format(row[0], row[1], row[2]))

conn.close()
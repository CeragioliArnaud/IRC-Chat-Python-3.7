#!/usr/bin/python3
# -*- coding: utf-8 -*

import cgi 
import cgitb

form = cgi.FieldStorage()
print("Content-type: text/html; charset=utf-8\n")

print(form.getvalue("name"))

html = """<!DOCTYPE html>
<head>
    <title>Mon programme</title>
</head>
<body>
    <form action="/index.py" method="post">
        <input type="text" name="name" placeholder="Votre nom" />
        <input type="submit" name="send" value="Envoyer l'information au serveur">
    </form> 
</body>
</html>
"""
print(html)

#cgitb.enable() //erreurs rencontrées debug
#cgi.test() // affiche toute les infos du serveur web.
import sqlite3
import urllib
import re

conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS Counts''')

cur.execute('''CREATE TABLE Counts (org TEXT, count INTEGER)''')

fname = 'mbox.txt'

fh = open(fname)

for line in fh:
    if not line.startswith('From: ') : continue
    pieces = line.split()
    mail = pieces[1]
    
    email = mail.split("@")[-1]  
    email = email.rstrip( )
         
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (email, ))
    row = cur.fetchone()
    if row  is None:
        cur.execute('''INSERT INTO Counts (org, count) VALUES ( ?, 1 )''', ( email, ) )
       
    else : 
         cur.execute('UPDATE Counts SET count=count+1 WHERE org = ?', (email, ))
    # This statement commits outstanding changes to disk each 
    # time through the loop - the program can be made faster 
    # by moving the commit so it runs only after the loop completes
    
conn.commit()

# https://www.sqlite.org/lang_select.html
sqlstr = ('SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10')

for row in cur.execute(sqlstr) :
    print str(row[0]), row[1]

cur.close()
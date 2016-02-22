import sqlite3
import urllib
import re

conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS Counts''')

cur.execute('''CREATE TABLE Counts (email TEXT, count INTEGER)''')

fname = 'mbox.txt'

fh = open(fname)

for line in fh:
    if not line.startswith('From: ') : continue
    pieces = line.split()
    mail = pieces[1]
    
    email = "@"+ mail.split("@")[-1]  
         
    cur.execute('SELECT count FROM Counts WHERE email = ? ', (email, ))
    
    try:
        count = cur.fetchone()[0]
        cur.execute('UPDATE Counts SET count=count+1 WHERE email = ?', (email, ))
        
    except : 
        cur.execute('''INSERT INTO Counts (email, count) VALUES ( ?, 1 )''', ( email, ) )
    # This statement commits outstanding changes to disk each 
    # time through the loop - the program can be made faster 
    # by moving the commit so it runs only after the loop completes
    
conn.commit()

# https://www.sqlite.org/lang_select.html
sqlstr = ('SELECT email, count FROM Counts ORDER BY count DESC LIMIT 10')

for row in cur.execute(sqlstr) :
    print str(row[0]), row[1]

cur.close()

import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()

#Make the tables
cur.execute('''CREATE TABLE IF NOT EXISTS Artist(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
    ) ''')

cur.execute('''CREATE TABLE IF NOT EXISTS Genre(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
    ) ''')
	
cur.execute('''CREATE TABLE IF NOT EXISTS Album(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id INTEGER,
    title TEXT UNIQUE
    ) ''')
	
cur.execute('''CREATE TABLE IF NOT EXISTS Track(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE,
    album_id INTEGER,
    genre_id INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
    ) ''')
	


fname = 'Library.xml'

fh = open(fname)


def lookup(entry, key):
    found = False
    for child in entry:
        if found: return child.text
        if child.tag == 'key' and child.text == key:
            found = True
    return None
		
stuff = ET.parse(fname)
all = stuff.findall('dict/dict/dict')

#print 'Dict count:', len(all)
#print all

trackid = None
name = None
artist = None
album = None
genre = None
count = None
rating = None
length = None
 
for entry in all:
    for child in entry:
        if trackid is None: trackid = lookup(entry, 'Track ID')
        if name is None: name = lookup(entry, 'Name')
        if artist is None: artist = lookup(entry, 'Artist')
        if genre is None: genre = lookup(entry, 'Genre')
        if album is None: album = lookup(entry, "Album")
        if count is None: count = lookup(entry, 'Play Count')
        if rating is None: rating = lookup(entry, 'Rating')
        if length is None: length = lookup(entry, 'Total Time')
	
    if name is None or artist is None or album is None or count is None or rating is None or length is None: continue
    print name, artist, album, count, rating, length
    cur.execute('''INSERT OR IGNORE INTO Artist (name) VALUES (?)''', (artist, ))
    cur.execute('SELECT id FROM Artist WHERE name = ?', (artist, ))
    artist_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id) VALUES (?, ?)''', (album, artist_id))
    cur.execute('SELECT id FROM Album WHERE title = ?', (album, ))
    album_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Genre (name) VALUES ( ? )''', ( genre, ) )
    cur.execute('SELECT id FROM Genre WHERE name = ? ', (genre, ))
    genre_id = cur.fetchone()[0]
    
    cur.execute('''INSERT OR REPLACE INTO Track (title, album_id, len, rating, count) VALUES (?,?,?,?,?)''', 
    (name, album_id, length, rating, count ))
    print entry
    conn.commit()
    #reset the variables so they can be set for next group
    trackid = None
    name = None
    artist = None
    genre = None
    album = None
    count = None
    rating = None
    length = None

	
print name, artist, album, count, rating, length

import sqlite3

# use the database in the app, store the database in this file
conn = sqlite3.connect('orgdb.sqlite')
# connection object
cur = conn.cursor()

# create a table: 'Counts', drop the table every time run this program, and create it again
# SQL commends
cur.execute('''
DROP TABLE IF EXISTS Counts''')

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

fname = input('Enter file name: ')
if ( len(fname) < 1 ) : fname = 'mbox.txt'
fh = open(fname)
for line in fh:
    # accept the lines with 'From'
    if not line.startswith('From: ') : continue
    pieces = line.split()
    # the element after 'From:'
    org = pieces[1][pieces[1].index('@')+1:]
    # (email, ) is a 'one' tuple, the first thing in the tuple will be substitute for the '?'
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org, ))
    # if there is a row
    try:
        # brings one row into memory, as a list (only one thing in the list)
        row = cur.fetchone()[0]
        cur.execute('UPDATE Counts SET count=count+1 WHERE org = ?', (org, ))
    # add a new row into the table
    except:
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES ( ?, 1 )''', (org, ))

    # This statement commits outstanding changes to disk each
    # time through the loop - the program can be made faster
    # by moving the commit so it runs only after the loop completes
    conn.commit()

# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()

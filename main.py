import sqlite3
import sys

import bobcatModule


### hash value to sql int
### this will convert a tuble of 3 ints to a string of fixed size
def hash_to_str(h):
    res = format(h[2], '04x') + format(h[1], '04x') + format(h[2], '04x') 
    return res

#connect to database table 
db = sqlite3.connect('test.db')

cursor = db.cursor()

db.execute("DROP TABLE IF EXISTS Hashes")
db.commit()

try:
    db.execute("CREATE TABLE Hashes(ID TEXT PRIMARY KEY NOT NULL, Message TEXT NOT NULL);")
    db.commit()
except sqlite3.OperationalError:
    print("Table Coudn't be created")


db.execute("INSERT INTO Hashes (ID, Message) VALUES ('0xffffffffffff', 'Banas')")
db.commit()



###viewing data
try:
    result = cursor.execute("SELECT ID, Message  FROM Hashes")
    for row in result:
        print("ID :", row[0])
        print("Message :", row[1])
except:
    print("coudn't retrieve data")



##generate hashes

